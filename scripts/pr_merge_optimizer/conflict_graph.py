"""Construction of the pairwise conflict graph from a set of pull requests.

Two phases, following the design document:

1. **File-overlap pre-filter (fast).** If two pull requests touch no common
   files they cannot textually conflict, so no edge is added.
2. **Precise check.** For overlapping pull requests, either a supplied
   ``merge_tester`` (e.g. a real git merge simulation) decides whether the pair
   conflicts, or -- when no tester is available -- the overlap is treated
   conservatively as a conflict.

Overlaps that touch binary assets, engine scene/prefab formats, or Git LFS
tracked files are always hard conflicts and short-circuit the precise check.
"""

from __future__ import annotations

from itertools import combinations
from typing import Callable, Dict, Iterable, Optional, Sequence, Set

from .models import (
    DEFAULT_BINARY_EXTENSIONS,
    DEFAULT_ENGINE_SCENE_EXTENSIONS,
    PullRequest,
    is_binary_path,
    is_engine_scene_path,
    is_lfs_tracked,
)

# A conflict tester returns ``True`` when merging the two pull requests conflicts.
ConflictTester = Callable[[PullRequest, PullRequest], bool]


def overlapping_files(a: PullRequest, b: PullRequest) -> Set[str]:
    """Return the set of files modified by both pull requests."""

    return set(a.files) & set(b.files)


def is_hard_conflict_overlap(
    overlap: Iterable[str],
    *,
    binary_extensions: Iterable[str] = DEFAULT_BINARY_EXTENSIONS,
    engine_scene_extensions: Iterable[str] = DEFAULT_ENGINE_SCENE_EXTENSIONS,
    lfs_patterns: Iterable[str] = (),
    treat_engine_scenes_as_hard: bool = True,
) -> bool:
    """Return ``True`` if any overlapping file cannot be textually merged.

    Binary assets and Git LFS tracked files are always hard conflicts. Engine
    scene/prefab formats are hard conflicts unless the caller has configured a
    specialised merge driver and disables ``treat_engine_scenes_as_hard``.
    """

    binary = set(binary_extensions)
    engine = set(engine_scene_extensions)
    patterns = tuple(lfs_patterns)
    for path in overlap:
        if is_binary_path(path, binary):
            return True
        if is_lfs_tracked(path, patterns):
            return True
        if treat_engine_scenes_as_hard and is_engine_scene_path(path, engine):
            return True
    return False


def build_conflict_graph(
    pull_requests: Sequence[PullRequest],
    *,
    merge_tester: Optional[ConflictTester] = None,
    binary_extensions: Iterable[str] = DEFAULT_BINARY_EXTENSIONS,
    engine_scene_extensions: Iterable[str] = DEFAULT_ENGINE_SCENE_EXTENSIONS,
    lfs_patterns: Iterable[str] = (),
    treat_engine_scenes_as_hard: bool = True,
    assume_overlap_conflicts: bool = True,
) -> Dict[int, Set[int]]:
    """Build the conflict graph for ``pull_requests``.

    Args:
        pull_requests: The candidate pull requests (nodes of the graph).
        merge_tester: Optional precise conflict check for overlapping pairs; it
            returns ``True`` when the pair genuinely conflicts. When ``None``,
            ``assume_overlap_conflicts`` governs how overlaps are treated.
        binary_extensions: File extensions treated as non-mergeable binary assets.
        engine_scene_extensions: Engine scene/prefab extensions.
        lfs_patterns: Git LFS path patterns (see :func:`models.parse_lfs_patterns`).
        treat_engine_scenes_as_hard: Whether engine scene overlaps are hard conflicts.
        assume_overlap_conflicts: When no ``merge_tester`` is supplied, whether a
            plain textual overlap should be recorded as a conflict edge. Defaults
            to ``True`` (conservative: never batch-merge unverified overlaps).

    Returns:
        An adjacency map ``{pr_number: {conflicting_pr_number, ...}}``.
    """

    binary = set(binary_extensions)
    engine = set(engine_scene_extensions)
    patterns = tuple(lfs_patterns)

    graph: Dict[int, Set[int]] = {pr.number: set() for pr in pull_requests}

    for a, b in combinations(pull_requests, 2):
        overlap = overlapping_files(a, b)
        if not overlap:
            continue

        if is_hard_conflict_overlap(
            overlap,
            binary_extensions=binary,
            engine_scene_extensions=engine,
            lfs_patterns=patterns,
            treat_engine_scenes_as_hard=treat_engine_scenes_as_hard,
        ):
            _add_edge(graph, a.number, b.number)
            continue

        if merge_tester is not None:
            conflict = merge_tester(a, b)
        else:
            conflict = assume_overlap_conflicts

        if conflict:
            _add_edge(graph, a.number, b.number)

    return graph


def _add_edge(graph: Dict[int, Set[int]], a: int, b: int) -> None:
    """Record an undirected conflict edge between nodes ``a`` and ``b``."""

    if a == b:
        return
    graph[a].add(b)
    graph[b].add(a)
