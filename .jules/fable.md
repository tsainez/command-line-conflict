# Fable — Repository Analysis & Stabilization Journal

## 2026-07-04 - Gameplay-loop audit after the scrap-economy merge
**Context:** Reviewed the repository state right after the resource-management
commit (71b3554) that wired scrap harvesting, factory construction costs, and
hotkey training into `GameScene`. Goal: fix urgent bugs immediately, and mark
broader design drift with in-code instructions rather than unilateral rewrites.

**Bugs fixed:**
- **Campaign deadlock:** `rover` was only unlockable by completing mission_1,
  but mission_1 (FactoryBattleMap) starts the player with three melee Chassis
  against ranged Rovers/Arachnotrons and gates the whole loop behind
  `is_unit_unlocked("rover")`. A fresh install could neither build a Rover
  Factory nor plausibly win, so the unlock could never be earned. `rover` is
  now in `DEFAULT_UNLOCKED_UNITS` (campaign_manager.py); mission_1's reward is
  redundant until the rewards table is re-purposed.
- **Free-upgrade exploit via spawn fallback:** `_train_chassis_at_factory` and
  `_train_rover_at_factory` fell back to spawning ON the factory's tile when
  all 8 neighbors were blocked; `ProductionSystem` then instantly transformed
  the paid unit into the next tier at zero cost (chassis→rover, and worse,
  rover→arachnotron bypassing the adjacent-rover rule). Training now refuses
  (no charge) when there is no free adjacent tile (`_find_free_adjacent_tile`).
- **R/A hotkey double-fire:** one keypress could both build a factory from a
  selected chassis AND train at a selected Arachnotron Factory (double spend).
  `_handle_construction` now consumes the keypress whenever a chassis is
  selected.
- **HUD overprint:** the chat log grew upward from `SCREEN_HEIGHT-120` straight
  through the Construction/Factory Production hint panels anchored at
  `SCREEN_HEIGHT-160`, interleaving both into garbage text whenever a factory
  was selected. Chat is now anchored at `SCREEN_HEIGHT-170`, above the hint
  band.
- **Phantom persistence:** in-match Arachnotron research called
  `save_progress()`, which does not persist `unlocked_units` at all (only
  completed_missions) — a misleading disk write. Removed; research is now
  explicitly documented as session-scoped.
- Removed committed test junk `tmp_test/` (leftover from PR #371's run of the
  security suite) and gitignored the directory; deduplicated the double
  `FogOfWar` construction in `GameScene.__init__`; the Arachnotron Factory
  panel now advertises the already-functional `C: Train Chassis` hotkey.

**Design drift flagged with in-code DESIGN NOTES (not changed):**
- `ProductionSystem`: free walk-in transformation coexists with paid hotkey
  training, making every scrap price bypassable by right-clicking a unit onto
  the factory tile. Options laid out in the class docstring (charge walk-ins /
  remove walk-ins / remove paid training).
- `campaign_manager.MISSION_REWARDS`: two competing tech systems (persistent
  campaign rewards vs session-scoped in-match research) — reconciliation
  guidance sits above the table.
- `ResourceSystem`: wildlife-kill drip is the only income and does not scale
  with player investment; the default-unlocked `extractor` unit has no
  economic role despite its name.

**Learning:** When autonomous agents bolt a new economy onto an ECS game, the
old free paths rarely get retired — they linger as invisible discounts. Audit
every legacy system that produces the same output the new economy sells, and
make spawn-position fallbacks fail closed (refuse) rather than fail onto a
semantically loaded tile like a factory.
**Model:** Claude (via Claude Code)
