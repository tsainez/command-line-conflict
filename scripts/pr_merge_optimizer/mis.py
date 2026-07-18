"""Maximum Independent Set (MIS) solver for the conflict graph.

Determining how many pull requests can be merged concurrently is modelled as a
Maximum Independent Set problem on the conflict graph ``G = (V, E)`` where an
edge means "these two pull requests conflict". The largest set of mutually
non-conflicting pull requests is the largest batch that can be merged at once.

MIS is NP-hard in general, but the conflict graphs produced here are small (tens
of nodes) and typically sparse, so an exact branch-and-bound solver with a few
classic reductions solves them effectively instantly.
"""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Set


def _normalize(graph: Mapping[int, Iterable[int]]) -> Dict[int, Set[int]]:
    """Return a symmetric adjacency map with self-loops and dangling edges removed."""

    adjacency: Dict[int, Set[int]] = {node: set() for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor == node or neighbor not in adjacency:
                continue
            adjacency[node].add(neighbor)
            adjacency[neighbor].add(node)
    return adjacency


def maximum_independent_set(graph: Mapping[int, Iterable[int]]) -> Set[int]:
    """Return a maximum independent set of ``graph`` as a set of node ids.

    ``graph`` is an adjacency mapping ``{node: neighbors}``. The returned set is
    guaranteed to be of maximum possible size; when several maxima exist, the one
    found first by the deterministic branching order is returned.

    >>> sorted(maximum_independent_set({1: {2}, 2: {1}, 3: set()}))
    [1, 3]
    >>> len(maximum_independent_set({}))
    0
    """

    adjacency = _normalize(graph)
    # Deterministic tie-break: prefer branching on the lowest node id among ties.
    order = {node: index for index, node in enumerate(sorted(adjacency))}
    best: Set[int] = set()

    def degree_in(node: int, candidates: Set[int]) -> int:
        return len(adjacency[node] & candidates)

    def solve(candidates: Set[int], chosen: Set[int]) -> None:
        nonlocal best

        # Upper bound: even taking every remaining candidate cannot beat best.
        if len(chosen) + len(candidates) <= len(best):
            return

        if not candidates:
            if len(chosen) > len(best):
                best = set(chosen)
            return

        # Reduction: vertices with no remaining neighbours are always safe to
        # include (they can never conflict with anything left), so include them
        # all at once instead of branching.
        isolated = {node for node in candidates if not adjacency[node] & candidates}
        if isolated:
            solve(candidates - isolated, chosen | isolated)
            return

        # Branch on the highest-degree vertex; exploring "include" first tends to
        # raise ``best`` quickly and prune the "exclude" branch.
        pivot = max(candidates, key=lambda node: (degree_in(node, candidates), -order[node]))

        # Branch 1: include the pivot, dropping all of its neighbours.
        solve(candidates - {pivot} - adjacency[pivot], chosen | {pivot})
        # Branch 2: exclude the pivot.
        solve(candidates - {pivot}, chosen)

    solve(set(adjacency), set())
    return best
