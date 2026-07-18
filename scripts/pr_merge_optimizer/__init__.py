"""AI-powered batch pull request merge optimizer.

This package models pull-request merge planning as a Maximum Independent Set
problem on a conflict graph and computes the largest set of pull requests that
can be merged together without conflicts. See ``docs/PRMergeOptimizer.md`` for
the full design.

Public API:

* :class:`PullRequest`, :class:`MergePlan` -- data models
* :func:`maximum_independent_set` -- the MIS solver
* :func:`build_conflict_graph` -- pairwise conflict graph construction
* :class:`PRMergeOptimizer`, :func:`plan_from_graph` -- orchestration
"""

from .conflict_graph import build_conflict_graph, is_hard_conflict_overlap, overlapping_files
from .mis import maximum_independent_set
from .models import (
    DEFAULT_BINARY_EXTENSIONS,
    DEFAULT_ENGINE_SCENE_EXTENSIONS,
    MergePlan,
    PullRequest,
    edges_from_graph,
    graph_from_edges,
    is_binary_path,
    is_engine_scene_path,
    is_lfs_tracked,
    parse_lfs_patterns,
)
from .optimizer import PRMergeOptimizer, plan_from_graph

__all__ = [
    "DEFAULT_BINARY_EXTENSIONS",
    "DEFAULT_ENGINE_SCENE_EXTENSIONS",
    "MergePlan",
    "PRMergeOptimizer",
    "PullRequest",
    "build_conflict_graph",
    "edges_from_graph",
    "graph_from_edges",
    "is_binary_path",
    "is_engine_scene_path",
    "is_hard_conflict_overlap",
    "is_lfs_tracked",
    "maximum_independent_set",
    "overlapping_files",
    "parse_lfs_patterns",
    "plan_from_graph",
]
