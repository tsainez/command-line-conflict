"""High-level orchestration of the batch pull request merge optimizer.

Given a set of pull requests, the optimizer builds the conflict graph (Phase 2),
solves the Maximum Independent Set on it (Phase 3) to find the largest
conflict-free batch, and returns a :class:`~pr_merge_optimizer.models.MergePlan`
that also lists the pull requests deferred for agentic conflict resolution
(Phase 4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .conflict_graph import ConflictTester, build_conflict_graph
from .mis import maximum_independent_set
from .models import (
    DEFAULT_BINARY_EXTENSIONS,
    DEFAULT_ENGINE_SCENE_EXTENSIONS,
    MergePlan,
    PullRequest,
    edges_from_graph,
    graph_from_edges,
)


@dataclass
class PRMergeOptimizer:
    """Plan the largest conflict-free batch merge for a set of pull requests.

    The classification knobs mirror :func:`conflict_graph.build_conflict_graph`
    and let the same optimizer serve a plain service repo or a game/RTS workspace
    with binary assets and engine scene files.
    """

    binary_extensions: Iterable[str] = field(default_factory=lambda: set(DEFAULT_BINARY_EXTENSIONS))
    engine_scene_extensions: Iterable[str] = field(default_factory=lambda: set(DEFAULT_ENGINE_SCENE_EXTENSIONS))
    lfs_patterns: Iterable[str] = field(default_factory=tuple)
    treat_engine_scenes_as_hard: bool = True
    assume_overlap_conflicts: bool = True

    def build_graph(
        self,
        pull_requests: Sequence[PullRequest],
        *,
        merge_tester: Optional[ConflictTester] = None,
        explicit_conflicts: Optional[Iterable[Tuple[int, int]]] = None,
    ) -> Dict[int, Set[int]]:
        """Return the conflict graph, using explicit edges when provided."""

        if explicit_conflicts is not None:
            return graph_from_edges([pr.number for pr in pull_requests], explicit_conflicts)
        return build_conflict_graph(
            pull_requests,
            merge_tester=merge_tester,
            binary_extensions=self.binary_extensions,
            engine_scene_extensions=self.engine_scene_extensions,
            lfs_patterns=self.lfs_patterns,
            treat_engine_scenes_as_hard=self.treat_engine_scenes_as_hard,
            assume_overlap_conflicts=self.assume_overlap_conflicts,
        )

    def plan(
        self,
        pull_requests: Sequence[PullRequest],
        *,
        merge_tester: Optional[ConflictTester] = None,
        explicit_conflicts: Optional[Iterable[Tuple[int, int]]] = None,
    ) -> MergePlan:
        """Compute the optimal :class:`MergePlan` for ``pull_requests``."""

        graph = self.build_graph(
            pull_requests,
            merge_tester=merge_tester,
            explicit_conflicts=explicit_conflicts,
        )
        return plan_from_graph(graph)


def plan_from_graph(graph: Dict[int, Set[int]]) -> MergePlan:
    """Solve the MIS on ``graph`` and package the result as a :class:`MergePlan`."""

    batch: Set[int] = maximum_independent_set(graph)
    deferred: List[int] = sorted(set(graph) - batch)
    edges = edges_from_graph(graph)
    return MergePlan(batch=sorted(batch), deferred=deferred, conflict_edges=edges)
