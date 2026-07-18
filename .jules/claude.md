# Claude — Tooling & Automation Journal

## 2026-07-18 - PR Merge Optimizer (batch merge planner)
**Context:** Implemented the "AI-Powered Batch Pull Request Merger" design as a
standalone tool under `scripts/pr_merge_optimizer/`. The tool models a batch of
open pull requests as a conflict graph and computes the largest conflict-free
batch via Maximum Independent Set (MIS); leftover PRs are flagged for manual /
agentic resolution.

**Design decisions:**
- **Placed the tool under `scripts/`, not `command_line_conflict/`.** The
  optimizer operates on git/GitHub metadata, not the game engine, so it belongs
  with the other maintenance scripts. This also keeps it out of the game
  package's `--cov-fail-under=80` gate, which is scoped to `command_line_conflict`
  only — the network/subprocess layers (GitHub REST, `git merge-tree`) would
  otherwise be impossible to cover without live integration tests.
- **Made `scripts/` a real package (`scripts/__init__.py`).** Without it, `mypy .`
  discovers `pr_merge_optimizer` under two module names and errors "found twice";
  the `__init__.py` also enables `python -m scripts.pr_merge_optimizer`.
- **Separated pure logic from I/O.** MIS solving, conflict-graph construction, and
  file classification are pure and unit-tested (including an MIS oracle: the
  branch-and-bound solver is checked against a brute-force MIS on 60 random
  graphs). Network (`github_client`) and subprocess (`git_simulator`) code is
  isolated behind thin, injectable seams, with their *parsing* helpers tested
  offline.
- **Game/RTS adaptation baked into classification.** Overlaps on binary assets,
  Git LFS files, and engine scene/prefab formats (`.unity`, `.prefab`, `.tscn`,
  `.uasset`, …) are treated as hard, unmergeable conflicts, since the default git
  text driver corrupts them. Engine-scene hardness is toggleable for repos that
  configure a smart merge driver.

**Learning:** For an exact MIS on small, sparse graphs, two classic reductions
carry almost all the weight: (1) always include vertices with no remaining
neighbours instead of branching on them, and (2) branch on the highest-degree
vertex, exploring the "include" side first so the incumbent `best` rises quickly
and prunes the "exclude" subtree. An upper-bound cutoff
(`len(chosen) + len(candidates) <= len(best)`) makes the 47-PR case instant.
Always validate a hand-rolled combinatorial solver against a brute-force oracle
in tests — size, not the specific set, is the invariant to assert since multiple
maxima can exist.
