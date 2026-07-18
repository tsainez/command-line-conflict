"""Tests for the batch pull request merge optimizer (scripts/pr_merge_optimizer)."""

import itertools
import json
import random

import pytest

from scripts.pr_merge_optimizer import (
    MergePlan,
    PRMergeOptimizer,
    PullRequest,
    build_conflict_graph,
    cli,
    edges_from_graph,
    graph_from_edges,
    is_binary_path,
    is_engine_scene_path,
    is_hard_conflict_overlap,
    is_lfs_tracked,
    maximum_independent_set,
    parse_lfs_patterns,
)
from scripts.pr_merge_optimizer.github_client import files_from_payload, pull_request_from_payload

# --------------------------------------------------------------------------- #
# File classification
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "path, expected",
    [
        ("assets/soldier.fbx", True),
        ("art/logo.PNG", True),
        ("audio/theme.wav", True),
        ("command_line_conflict/engine.py", False),
        ("README.md", False),
    ],
)
def test_is_binary_path(path, expected):
    assert is_binary_path(path) is expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Scenes/Level1.unity", True),
        ("Prefabs/Soldier.prefab", True),
        ("world.tscn", True),
        ("src/main.py", False),
    ],
)
def test_is_engine_scene_path(path, expected):
    assert is_engine_scene_path(path) is expected


def test_parse_lfs_patterns_ignores_comments_and_non_lfs_lines():
    text = "\n".join(
        [
            "# LFS config",
            "*.psd filter=lfs diff=lfs merge=lfs -text",
            "*.fbx filter=lfs diff=lfs merge=lfs -text",
            "*.txt text",
            "",
        ]
    )
    assert parse_lfs_patterns(text) == ["*.psd", "*.fbx"]


def test_is_lfs_tracked_matches_basename_and_full_path():
    patterns = ["*.psd", "art/**"]
    assert is_lfs_tracked("art/logo.psd", patterns) is True
    assert is_lfs_tracked("nested/logo.psd", patterns) is True
    assert is_lfs_tracked("src/main.py", patterns) is False


# --------------------------------------------------------------------------- #
# PullRequest model
# --------------------------------------------------------------------------- #


def test_pull_request_from_dict_defaults():
    pr = PullRequest.from_dict({"number": "7", "files": ["a.py", "b.py"]})
    assert pr.number == 7
    assert pr.files == {"a.py", "b.py"}
    assert pr.base_ref == "main"
    assert pr.branch == ""


def test_pull_request_from_dict_handles_missing_files():
    pr = PullRequest.from_dict({"number": 3})
    assert pr.files == set()


# --------------------------------------------------------------------------- #
# Maximum Independent Set solver
# --------------------------------------------------------------------------- #


def _is_independent(graph, chosen):
    chosen = set(chosen)
    for node in chosen:
        if set(graph.get(node, set())) & (chosen - {node}):
            return False
    return True


def _brute_force_mis_size(graph):
    nodes = list(graph)
    best = 0
    for size in range(len(nodes), -1, -1):
        if size <= best:
            break
        for combo in itertools.combinations(nodes, size):
            if _is_independent(graph, combo):
                best = max(best, size)
                break
    return best


def test_mis_empty_graph():
    assert maximum_independent_set({}) == set()


def test_mis_single_node():
    assert maximum_independent_set({1: set()}) == {1}


def test_mis_simple_pair():
    result = maximum_independent_set({1: {2}, 2: {1}})
    assert len(result) == 1


def test_mis_triangle():
    graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}}
    assert len(maximum_independent_set(graph)) == 1


def test_mis_star_picks_leaves():
    # A star: centre 0 connected to leaves 1..4; MIS is the four leaves.
    graph = {0: {1, 2, 3, 4}, 1: {0}, 2: {0}, 3: {0}, 4: {0}}
    result = maximum_independent_set(graph)
    assert result == {1, 2, 3, 4}


def test_mis_disconnected_isolated_nodes_all_included():
    graph = {1: set(), 2: set(), 3: {4}, 4: {3}}
    result = maximum_independent_set(graph)
    assert {1, 2}.issubset(result)
    assert len(result) == 3


def test_mis_matches_brute_force_on_random_graphs():
    rng = random.Random(1234)
    for _ in range(60):
        n = rng.randint(1, 12)
        graph = {i: set() for i in range(n)}
        for a, b in itertools.combinations(range(n), 2):
            if rng.random() < 0.35:
                graph[a].add(b)
                graph[b].add(a)
        result = maximum_independent_set(graph)
        assert _is_independent(graph, result)
        assert len(result) == _brute_force_mis_size(graph)


def test_mis_tolerates_asymmetric_and_self_loops():
    # Directed-looking input with a self loop; solver normalizes it.
    graph = {1: {2, 1}, 2: set(), 3: {1}}
    result = maximum_independent_set(graph)
    assert _is_independent({1: {2, 3}, 2: {1}, 3: {1}}, result)
    assert len(result) == 2


# --------------------------------------------------------------------------- #
# Conflict graph construction
# --------------------------------------------------------------------------- #


def _pr(number, files, branch=""):
    return PullRequest(number=number, files=set(files), branch=branch)


def test_build_graph_no_overlap_no_edges():
    prs = [_pr(1, ["a.py"]), _pr(2, ["b.py"])]
    graph = build_conflict_graph(prs)
    assert edges_from_graph(graph) == []


def test_build_graph_overlap_conservative_default_adds_edge():
    prs = [_pr(1, ["a.py"]), _pr(2, ["a.py"])]
    graph = build_conflict_graph(prs)
    assert edges_from_graph(graph) == [(1, 2)]


def test_build_graph_overlap_allowed_when_unverified_overlaps_permitted():
    prs = [_pr(1, ["a.py"]), _pr(2, ["a.py"])]
    graph = build_conflict_graph(prs, assume_overlap_conflicts=False)
    assert edges_from_graph(graph) == []


def test_build_graph_uses_merge_tester_for_overlaps():
    prs = [_pr(1, ["a.py"]), _pr(2, ["a.py"]), _pr(3, ["a.py"])]

    def tester(a, b):
        # Only 1 and 2 truly conflict.
        return {a.number, b.number} == {1, 2}

    graph = build_conflict_graph(prs, merge_tester=tester)
    assert edges_from_graph(graph) == [(1, 2)]


def test_build_graph_binary_overlap_is_hard_conflict_even_with_clean_tester():
    prs = [_pr(1, ["hero.fbx"]), _pr(2, ["hero.fbx"])]

    def clean_tester(a, b):
        return False  # git thinks it merges, but binary can't be merged

    graph = build_conflict_graph(prs, merge_tester=clean_tester)
    assert edges_from_graph(graph) == [(1, 2)]


def test_build_graph_engine_scene_overlap_hard_by_default_but_toggleable():
    prs = [_pr(1, ["Level.unity"]), _pr(2, ["Level.unity"])]

    hard = build_conflict_graph(prs, merge_tester=lambda a, b: False)
    assert edges_from_graph(hard) == [(1, 2)]

    soft = build_conflict_graph(prs, merge_tester=lambda a, b: False, treat_engine_scenes_as_hard=False)
    assert edges_from_graph(soft) == []


def test_build_graph_lfs_overlap_is_hard_conflict():
    prs = [_pr(1, ["data/model.dat"]), _pr(2, ["data/model.dat"])]
    graph = build_conflict_graph(prs, merge_tester=lambda a, b: False, lfs_patterns=["*.dat"])
    assert edges_from_graph(graph) == [(1, 2)]


def test_is_hard_conflict_overlap_pure():
    assert is_hard_conflict_overlap(["a.png"]) is True
    assert is_hard_conflict_overlap(["a.py"]) is False
    assert is_hard_conflict_overlap(["a.unity"], treat_engine_scenes_as_hard=False) is False


# --------------------------------------------------------------------------- #
# Graph helpers
# --------------------------------------------------------------------------- #


def test_graph_from_edges_and_edges_round_trip():
    graph = graph_from_edges([1, 2, 3, 4], [(1, 2), (2, 3), (1, 1), (9, 10)])
    # self loop and out-of-range edge are dropped
    assert edges_from_graph(graph) == [(1, 2), (2, 3)]
    assert graph[4] == set()


# --------------------------------------------------------------------------- #
# Optimizer orchestration
# --------------------------------------------------------------------------- #


def test_optimizer_plan_with_explicit_conflicts():
    prs = [_pr(1, ["a.py"]), _pr(2, ["a.py"]), _pr(3, ["a.py"])]
    optimizer = PRMergeOptimizer()
    plan = optimizer.plan(prs, explicit_conflicts=[(1, 2)])
    assert plan.total == 3
    assert set(plan.batch) | set(plan.deferred) == {1, 2, 3}
    assert len(plan.batch) == 2
    assert plan.conflict_edges == [(1, 2)]


def test_optimizer_plan_derives_conflicts_and_maximizes_batch():
    prs = [
        _pr(1, ["ui.py"]),
        _pr(2, ["ui.py"]),
        _pr(3, ["maps/desert.py"]),
        _pr(4, ["hero.fbx"]),
        _pr(5, ["hero.fbx"]),
        _pr(6, ["README.md"]),
    ]
    plan = PRMergeOptimizer().plan(prs)
    assert len(plan.batch) == 4
    assert set(plan.conflict_edges) == {(1, 2), (4, 5)}
    # Exactly one PR from each conflicting pair is deferred.
    assert len(plan.deferred) == 2


def test_merge_plan_summary_and_to_dict():
    plan = MergePlan(batch=[1, 3], deferred=[2], conflict_edges=[(1, 2)])
    summary = plan.summary()
    assert "#1" in summary and "#3" in summary
    payload = plan.to_dict()
    assert payload["batch"] == [1, 3]
    assert payload["batch_size"] == 2
    assert payload["conflict_edges"] == [[1, 2]]


# --------------------------------------------------------------------------- #
# GitHub payload parsing (no network)
# --------------------------------------------------------------------------- #


def test_files_from_payload():
    payload = [{"filename": "a.py"}, {"filename": "b.py"}, {"status": "removed"}]
    assert files_from_payload(payload) == ["a.py", "b.py"]


def test_pull_request_from_payload():
    payload = {
        "number": 42,
        "title": "Add feature",
        "head": {"ref": "feature-branch"},
        "base": {"ref": "develop"},
    }
    pr = pull_request_from_payload(payload, ["x.py", "y.py"])
    assert pr.number == 42
    assert pr.branch == "feature-branch"
    assert pr.base_ref == "develop"
    assert pr.files == {"x.py", "y.py"}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def _write_json(tmp_path, payload):
    path = tmp_path / "prs.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def test_cli_text_output(tmp_path, capsys):
    payload = {
        "prs": [
            {"number": 1, "files": ["a.py"]},
            {"number": 2, "files": ["a.py"]},
            {"number": 3, "files": ["b.py"]},
        ]
    }
    exit_code = cli.main(["--input", _write_json(tmp_path, payload)])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Pull requests analyzed : 3" in out
    assert "Conflict-free batch    : 2" in out


def test_cli_json_output_to_file(tmp_path):
    payload = {
        "prs": [
            {"number": 1, "files": ["a.py"]},
            {"number": 2, "files": ["a.py"]},
        ],
        "conflicts": [[1, 2]],
    }
    out_path = tmp_path / "report.json"
    exit_code = cli.main(["--input", _write_json(tmp_path, payload), "--format", "json", "--output", str(out_path)])
    assert exit_code == 0
    report = json.loads(out_path.read_text(encoding="utf-8"))
    assert report["total"] == 2
    assert report["batch_size"] == 1
    assert report["conflict_edges"] == [[1, 2]]


def test_cli_gitattributes_makes_overlap_hard(tmp_path, capsys):
    attrs = tmp_path / ".gitattributes"
    attrs.write_text("*.dat filter=lfs diff=lfs merge=lfs -text\n", encoding="utf-8")
    payload = {
        "prs": [
            {"number": 1, "files": ["blob.dat"]},
            {"number": 2, "files": ["blob.dat"]},
        ]
    }
    exit_code = cli.main(["--input", _write_json(tmp_path, payload), "--gitattributes", str(attrs), "--format", "json"])
    assert exit_code == 0
    report = json.loads(capsys.readouterr().out)
    assert report["conflict_edges"] == [[1, 2]]
