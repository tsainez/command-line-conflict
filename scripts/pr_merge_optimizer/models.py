"""Data models and file classification for the PR merge optimizer.

This module holds the pure-data pieces of the optimizer: the :class:`PullRequest`
value object, the :class:`MergePlan` result, and helpers that decide whether an
overlapping file can be textually merged at all.

The classification helpers implement the "Adaptations for Game Development & RTS
Workspaces" section of the design document: binary assets, engine scene/prefab
formats, and Git LFS tracked files can never be merged with the default textual
driver, so any overlap in those files is treated as a hard conflict.
"""

from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Iterable, List, Sequence, Set, Tuple

# Extensions that cannot be textually merged. Overlap on any of these files is a
# hard, unresolvable conflict (design doc section 6A).
DEFAULT_BINARY_EXTENSIONS: FrozenSet[str] = frozenset(
    {
        # Images / textures
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tga",
        ".dds",
        ".psd",
        ".ico",
        # 3D models
        ".fbx",
        ".obj",
        ".blend",
        ".gltf",
        ".glb",
        ".3ds",
        ".dae",
        # Audio
        ".wav",
        ".mp3",
        ".ogg",
        ".flac",
        ".aiff",
        # Fonts
        ".ttf",
        ".otf",
        ".woff",
        ".woff2",
        # Archives / binaries
        ".zip",
        ".gz",
        ".7z",
        ".rar",
        ".pdf",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".bin",
    }
)

# Engine scene / prefab formats. These are technically text (YAML/JSON), but the
# default git merge driver corrupts them, so overlap is treated as a hard
# conflict unless a specialised merge driver is configured (design doc 6B).
DEFAULT_ENGINE_SCENE_EXTENSIONS: FrozenSet[str] = frozenset(
    {
        # Unity
        ".unity",
        ".prefab",
        ".asset",
        ".mat",
        ".anim",
        ".controller",
        ".meta",
        # Godot
        ".tscn",
        ".tres",
        ".scene",
        # Unreal
        ".uasset",
        ".umap",
    }
)


def _extension(path: str) -> str:
    """Return the lower-cased file extension for ``path`` (including the dot)."""

    return os.path.splitext(path)[1].lower()


def is_binary_path(path: str, extensions: Iterable[str] = DEFAULT_BINARY_EXTENSIONS) -> bool:
    """Return ``True`` if ``path`` looks like a non-mergeable binary asset.

    >>> is_binary_path("assets/soldier_mesh.fbx")
    True
    >>> is_binary_path("command_line_conflict/engine.py")
    False
    """

    return _extension(path) in set(extensions)


def is_engine_scene_path(path: str, extensions: Iterable[str] = DEFAULT_ENGINE_SCENE_EXTENSIONS) -> bool:
    """Return ``True`` if ``path`` is an engine scene/prefab format.

    >>> is_engine_scene_path("Scenes/Level1.unity")
    True
    >>> is_engine_scene_path("src/main.py")
    False
    """

    return _extension(path) in set(extensions)


def parse_lfs_patterns(gitattributes_text: str) -> List[str]:
    """Extract Git LFS tracked path patterns from ``.gitattributes`` content.

    Only lines that route a pattern through the ``lfs`` filter are returned.

    >>> parse_lfs_patterns("*.psd filter=lfs diff=lfs merge=lfs -text\\n# comment")
    ['*.psd']
    """

    patterns: List[str] = []
    for raw_line in gitattributes_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "filter=lfs" not in line:
            continue
        pattern = line.split()[0]
        if pattern:
            patterns.append(pattern)
    return patterns


def is_lfs_tracked(path: str, patterns: Iterable[str]) -> bool:
    """Return ``True`` if ``path`` matches any Git LFS pattern.

    Matching mirrors ``.gitattributes`` semantics closely enough for conflict
    detection: a bare pattern such as ``*.psd`` matches on the basename too.

    >>> is_lfs_tracked("art/logo.psd", ["*.psd"])
    True
    >>> is_lfs_tracked("src/main.py", ["*.psd"])
    False
    """

    basename = os.path.basename(path)
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(basename, pattern):
            return True
    return False


@dataclass
class PullRequest:
    """A single open pull request considered for batch merging.

    Attributes:
        number: The GitHub pull request number, used as the conflict-graph node id.
        files: The set of repository paths the pull request modifies.
        title: Human readable title (optional, used for reporting).
        branch: The head branch/ref, used by the git merge simulator.
        base_ref: The branch the pull request targets.
    """

    number: int
    files: Set[str] = field(default_factory=set)
    title: str = ""
    branch: str = ""
    base_ref: str = "main"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PullRequest":
        """Build a :class:`PullRequest` from a plain dictionary (e.g. parsed JSON)."""

        number = int(data["number"])
        raw_files = data.get("files") or []
        files = {str(path) for path in raw_files}
        title = str(data.get("title", ""))
        branch = str(data.get("branch", "") or "")
        base_ref = str(data.get("base_ref", "main") or "main")
        return cls(number=number, files=files, title=title, branch=branch, base_ref=base_ref)


@dataclass
class MergePlan:
    """The result of optimizing a set of pull requests for batch merging.

    Attributes:
        batch: Pull request numbers forming the maximum conflict-free batch.
        deferred: Pull request numbers left for agentic conflict resolution.
        conflict_edges: Pairs ``(a, b)`` of pull requests that conflict.
    """

    batch: List[int]
    deferred: List[int]
    conflict_edges: List[Tuple[int, int]]

    @property
    def total(self) -> int:
        """Total number of pull requests considered."""

        return len(self.batch) + len(self.deferred)

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serializable representation of the plan."""

        return {
            "batch": list(self.batch),
            "deferred": list(self.deferred),
            "conflict_edges": [list(edge) for edge in self.conflict_edges],
            "total": self.total,
            "batch_size": len(self.batch),
        }

    def summary(self) -> str:
        """Return a human readable, multi-line summary of the plan."""

        lines = [
            f"Pull requests analyzed : {self.total}",
            f"Conflict-free batch    : {len(self.batch)} "
            f"({', '.join('#' + str(n) for n in self.batch) if self.batch else 'none'})",
            f"Deferred for AI resolve: {len(self.deferred)} "
            f"({', '.join('#' + str(n) for n in self.deferred) if self.deferred else 'none'})",
            f"Conflict edges         : {len(self.conflict_edges)}",
        ]
        return "\n".join(lines)


def edges_from_graph(graph: Dict[int, Set[int]]) -> List[Tuple[int, int]]:
    """Return the sorted, de-duplicated undirected edges of a conflict graph."""

    seen: Set[Tuple[int, int]] = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            seen.add((node, neighbor) if node <= neighbor else (neighbor, node))
    return sorted(seen)


def graph_from_edges(nodes: Sequence[int], edges: Iterable[Tuple[int, int]]) -> Dict[int, Set[int]]:
    """Build an undirected conflict graph from explicit ``nodes`` and ``edges``."""

    graph: Dict[int, Set[int]] = {node: set() for node in nodes}
    for a, b in edges:
        if a == b:
            continue
        if a in graph and b in graph:
            graph[a].add(b)
            graph[b].add(a)
    return graph
