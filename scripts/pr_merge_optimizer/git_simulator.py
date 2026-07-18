"""Local git merge simulation used as the precise pairwise conflict check.

The design document describes checking out the base branch and merging two pull
request branches to see whether the second merge fails. Modern git offers a
cleaner, side-effect-free way to do exactly this: ``git merge-tree`` performs the
three-way merge entirely in memory and reports conflicts without touching the
working tree or index.

This module is thin, subprocess-based glue; it is exercised against a real
repository rather than in unit tests, so it is intentionally defensive about
git availability and version differences.
"""

from __future__ import annotations

import subprocess
from typing import List, Optional

from .models import PullRequest


class GitMergeSimulator:
    """Pairwise conflict tester backed by ``git merge-tree``.

    Args:
        repo_dir: Path to the git working directory to run commands in.
        base_ref: The integration branch both pull requests target.
        git_executable: The git binary to invoke (overridable for testing).
    """

    def __init__(self, repo_dir: str = ".", base_ref: str = "main", git_executable: str = "git") -> None:
        self.repo_dir = repo_dir
        self.base_ref = base_ref
        self.git_executable = git_executable

    def _run(self, args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.git_executable, "-C", self.repo_dir, *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def _ref_for(self, pr: PullRequest) -> str:
        """Return the git ref to merge for ``pr`` (branch if set, else FETCH ref)."""

        if pr.branch:
            return pr.branch
        return f"refs/pull/{pr.number}/head"

    def has_conflict(self, a: PullRequest, b: PullRequest) -> bool:
        """Return ``True`` if merging both pull requests produces a conflict.

        Uses ``git merge-tree --write-tree --merge-base <base> <a> <b>``; a
        non-zero exit code indicates a conflicting three-way merge. If git is too
        old to support that form, the call fails closed (returns ``True``) so a
        potentially conflicting pair is never batched by mistake.
        """

        base = a.base_ref or self.base_ref
        result = self._run(
            [
                "merge-tree",
                "--write-tree",
                "--merge-base",
                base,
                self._ref_for(a),
                self._ref_for(b),
            ]
        )
        # git merge-tree exits 0 on a clean merge and 1 when there are conflicts.
        # Any other exit code (bad refs, unsupported flag) is treated as a
        # conflict so the pair is deferred to manual/agentic resolution.
        return result.returncode != 0

    def available(self) -> bool:
        """Return ``True`` if the configured git executable can be invoked."""

        try:
            result = self._run(["--version"])
        except (OSError, ValueError):
            return False
        return result.returncode == 0


def make_merge_tester(repo_dir: str = ".", base_ref: str = "main") -> Optional[GitMergeSimulator]:
    """Return a :class:`GitMergeSimulator` if git is available, else ``None``."""

    simulator = GitMergeSimulator(repo_dir=repo_dir, base_ref=base_ref)
    return simulator if simulator.available() else None
