"""Command line interface for the PR merge optimizer.

Two input modes:

* ``--input FILE`` (or stdin): a JSON document describing the pull requests, and
  optionally a precomputed list of conflict edges. Fully offline and deterministic.
* ``--repo owner/name``: fetch open pull requests live from the GitHub REST API
  (requires network access and, for private repos, a ``GITHUB_TOKEN``).

Example JSON input::

    {
      "prs": [
        {"number": 1, "title": "Add minimap", "branch": "minimap", "files": ["hud.py"]},
        {"number": 2, "title": "Refactor HUD", "branch": "hud", "files": ["hud.py"]},
        {"number": 3, "title": "New map", "files": ["maps/desert.py"]}
      ],
      "conflicts": [[1, 2]]
    }

Run with ``python -m scripts.pr_merge_optimizer --input plan.json``.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple, cast

from .models import MergePlan, PullRequest, parse_lfs_patterns
from .optimizer import PRMergeOptimizer


def _load_input(path: Optional[str]) -> Dict[str, Any]:
    if path is None or path == "-":
        return cast(Dict[str, Any], json.load(sys.stdin))
    with open(path, "r", encoding="utf-8") as handle:
        return cast(Dict[str, Any], json.load(handle))


def _parse_pull_requests(data: Dict[str, Any]) -> List[PullRequest]:
    raw_prs = data.get("prs") or data.get("pull_requests") or []
    return [PullRequest.from_dict(item) for item in raw_prs]


def _parse_conflicts(data: Dict[str, Any]) -> Optional[List[Tuple[int, int]]]:
    raw = data.get("conflicts")
    if raw is None:
        return None
    return [(int(a), int(b)) for a, b in raw]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pr_merge_optimizer",
        description="Compute the largest conflict-free batch of pull requests to merge.",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--input", "-i", help="Path to a JSON file describing pull requests ('-' for stdin).")
    source.add_argument("--repo", help="GitHub repository 'owner/name' to fetch open pull requests from.")
    parser.add_argument("--base", help="Only consider pull requests targeting this base branch.")
    parser.add_argument("--gitattributes", help="Path to a .gitattributes file to load Git LFS patterns from.")
    parser.add_argument(
        "--simulate-git",
        metavar="REPO_DIR",
        help="Run real 'git merge-tree' simulations in REPO_DIR for overlapping pull requests.",
    )
    parser.add_argument(
        "--no-engine-hard-conflict",
        action="store_true",
        help="Do not treat engine scene/prefab overlaps as automatic hard conflicts.",
    )
    parser.add_argument(
        "--allow-unverified-overlaps",
        action="store_true",
        help="Treat plain file overlaps as mergeable when no git simulation is available.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format.")
    parser.add_argument("--output", "-o", help="Write the report to this file instead of stdout.")
    return parser


def _resolve_pull_requests(args: argparse.Namespace, data: Dict[str, Any]) -> List[PullRequest]:
    if args.repo:
        from .github_client import fetch_open_pull_requests

        return fetch_open_pull_requests(args.repo, base=args.base)
    return _parse_pull_requests(data)


def _resolve_merge_tester(args: argparse.Namespace, base: str) -> Optional[Any]:
    if not args.simulate_git:
        return None
    from .git_simulator import make_merge_tester

    simulator = make_merge_tester(repo_dir=args.simulate_git, base_ref=base)
    if simulator is None:
        print("warning: git is not available; skipping merge simulation", file=sys.stderr)
        return None
    return simulator.has_conflict


def _render(plan: MergePlan, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(plan.to_dict(), indent=2)
    return plan.summary()


def run(args: argparse.Namespace) -> MergePlan:
    """Execute the optimizer for parsed ``args`` and return the resulting plan."""

    data: Dict[str, Any] = {} if args.repo else _load_input(args.input)
    pull_requests = _resolve_pull_requests(args, data)

    lfs_patterns: List[str] = []
    if args.gitattributes:
        with open(args.gitattributes, "r", encoding="utf-8") as handle:
            lfs_patterns = parse_lfs_patterns(handle.read())

    base = args.base or "main"
    merge_tester = _resolve_merge_tester(args, base)
    explicit_conflicts = None if args.repo else _parse_conflicts(data)

    optimizer = PRMergeOptimizer(
        lfs_patterns=lfs_patterns,
        treat_engine_scenes_as_hard=not args.no_engine_hard_conflict,
        assume_overlap_conflicts=not args.allow_unverified_overlaps,
    )
    return optimizer.plan(
        pull_requests,
        merge_tester=merge_tester,
        explicit_conflicts=explicit_conflicts,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point: parse ``argv``, run the optimizer, and print the report."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.repo and args.input is None:
        # Default to stdin, but only if data was actually piped in.
        if sys.stdin.isatty():
            parser.error("no input: provide --input FILE, pipe JSON to stdin, or use --repo")

    plan = run(args)
    report = _render(plan, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(report + "\n")
    else:
        print(report)
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised via __main__.py
    raise SystemExit(main())
