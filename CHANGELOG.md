# Changelog


## 2026-07-03
- update journals (b5e8d51) - *Tony Sainez*
- Fix authorization bypass in side-switching feature (#451) (fb19ea6) - *Tony Sainez*
- Add rapid pagination to FileDialog with Page Up/Down (#453) (2a998d0) - *Tony Sainez*
- ⚡ Bolt: Replace loop accumulations with early returns (#452) (314e349) - *Tony Sainez*
- ⚡ Bolt: Add early returns to win/loss conditions (#455) (3cd596c) - *Tony Sainez*
- Optimize check_win_condition and check_loss_condition loops with early return (#449) (8d56b87) - *Tony Sainez*
- 🎨 Palette: Add keyboard pagination to FileDialog (#442) (eae3c6a) - *Tony Sainez*
- ⚡ Bolt: [performance improvement] Early exit in win/loss loops (#441) (97ac85e) - *Tony Sainez*

## 2026-06-29
- Fix case collision for .jules directory on macOS (452025c) - *Tony Sainez*

## 2026-06-28
- 🎨 Palette: [UX improvement] Add rapid pagination to scrollable UI (#440) (7c76414) - *Tony Sainez*
- ⚡ Bolt: [performance improvement] Early return in win/loss checks (#459) (9e91d9b) - *Tony Sainez*
- 🎨 Palette: [UX improvement] Add rapid pagination to FileDialog (#464) (4092054) - *Tony Sainez*
- ⚡ Bolt: [performance improvement] Early return in win/loss condition checks (#465) (c7a3fb8) - *Tony Sainez*
- 🎨 Palette: Add Page Up/Page Down keyboard navigation (#466) (a62de49) - *Tony Sainez*
- ⚡ Bolt: Optimize win/loss checks with early return (#472) (c538aa5) - *Tony Sainez*
- Add PageUp and PageDown support for faster navigation in FileDialog (#426) (4255830) - *Tony Sainez*
- chore(deps): bump actions/checkout from 6 to 7 (#457) (9001d73) - *dependabot[bot]*
- ⚡ Bolt: Optimize win/loss checks with early return (#469) (8c5b944) - *Tony Sainez*
- chore(deps): update mkdocstrings-python requirement (#461) (fbc4d84) - *dependabot[bot]*
- chore(deps): bump actions/cache from 5 to 6 (#477) (ce6ca6d) - *dependabot[bot]*
- 🛡️ Sentinel: [CRITICAL] Fix TOCTOU vulnerability in Map loading (#423) (566f2ef) - *Tony Sainez*
- 🎨 Palette: Add PageUp/PageDown keyboard navigation to FileDialog (#432) (d3d1bea) - *Tony Sainez*
- 🎨 Palette: Add PAGEUP and PAGEDOWN support for rapid FileDialog pagination (#422) (5b0dea4) - *Tony Sainez*
- 🎨 Palette: Add keyboard pagination to FileDialog (#418) (86ac760) - *Tony Sainez*
- 🎨 Palette: [UX improvement] Add pagination support to FileDialog (#420) (697547a) - *Tony Sainez*
- 🛡️ Sentinel: [MEDIUM] Fix unhandled TypeError DoS in Steam achievement unlocking (#402) (3cf94cf) - *Tony Sainez*
- 🛡️ Sentinel: [HIGH] Fix side-switching authorization bypass (#474) (e3fb6a3) - *Tony Sainez*
- Optimize production system to use O(M) spatial hash lookup (#475) (5f8c8cc) - *Tony Sainez*
- Add tooltip for disabled Save/Load button in FileDialog (#476) (edd6958) - *Tony Sainez*
- 🎨 Palette: Add PAGEUP and PAGEDOWN keyboard navigation to FileDialog (#409) (120cfcd) - *Tony Sainez*
- 🛡️ Sentinel: [CRITICAL] Fix unhandled TypeError in Steam API integration (#399) (eafb463) - *Tony Sainez*

## 2026-06-27
- Optimize game win/loss ECS queries with early returns (#447) (26a94dc) - *Tony Sainez*
- 🎨 Palette: Add rapid pagination to FileDialog (#448) (77bd1fd) - *Tony Sainez*

## 2026-06-22
- 🛡️ Sentinel: [CRITICAL] Fix TypeError vulnerability in steam integration (#393) (096a0e4) - *Tony Sainez*

## 2026-06-13
- Optimize distance calculations and vector math (#411) (69d1a5d) - *Tony Sainez*
- 🛡️ Sentinel: [HIGH] Fix TOCTOU vulnerability in map file loading (#413) (de01564) - *Tony Sainez*

## 2026-06-02
- feat: add helper text to MenuScene for improved UX (#388) (0df48d4) - *Tony Sainez*
- Fix TypeErrors in Steam Integration achievement unlocking (#387) (5b6a4c0) - *Tony Sainez*

## 2026-05-23
- UX: Fix Victory/Defeat cursor state and add Escape key navigation (#386) (fb0b297) - *Tony Sainez*
- Fix tooltip background width calculation to accurately fit text. (#384) (40855f2) - *Tony Sainez*
- Optimize RenderingSystem dictionary sorting (#383) (4f189bc) - *Tony Sainez*
- 🛡️ Sentinel: [SECURITY] Add input validation to Steam integration (#382) (85c1fb6) - *Tony Sainez*
- UX: Fix cursor state and add Escape key support to Victory/Defeat scenes (#381) (6e782d8) - *Tony Sainez*
- 🛡️ Sentinel: [MEDIUM] Add input validation to steamworks achievement names (#378) (23758fa) - *Tony Sainez*
- UX: Improve defeat and victory scene interactions (#375) (97cc554) - *Tony Sainez*
- ⚡ Bolt: A* Pathfinding Inner Loop Array Optimization (#374) (6f7e976) - *Tony Sainez*

## 2026-05-17
- 🎨 Palette: Add Escape Key Navigation (#373) (6f35a18) - *Tony Sainez*
- ⚡ Bolt: Optimize visible keys filtering with list comprehension (#372) (bec76c1) - *Tony Sainez*

## 2026-05-16
- feat(ui): add audio feedback to settings menu interactions (#371) (a092acc) - *Tony Sainez*
- 🎨 Palette: Update pause message to include Space key instruction (#370) (87a1b44) - *Tony Sainez*
- Fix persistent cursor states when switching scenes (#368) (9a67e4d) - *Tony Sainez*
- ⚡ Bolt: Optimize A* pathfinding inner loop (#367) (19b2b94) - *Tony Sainez*

## 2026-05-13
- ⚡ Bolt: optimize distance calculations with math.sqrt (#365) (18a1104) - *Tony Sainez*
- 🎨 Palette: Add interactivity cues to Victory and Defeat scenes (#364) (8e196da) - *Tony Sainez*
- ⚡ Bolt: Optimize system entity iteration (#363) (6c58907) - *Tony Sainez*

## 2026-05-11
- 🛡️ Sentinel: [HIGH] Fix Unauthorized Access to Cheats in Production (#358) (a2cb541) - *Tony Sainez*
- 🎨 Palette: Add mouse click support to end screens (#359) (5b2aef1) - *Tony Sainez*
- ⚡ Bolt: Optimize distance calculations by replacing exponentiation with multiplication (#361) (d5c0985) - *Tony Sainez*
- feat(ui): add blinking cursor focus indicator to file dialog input\n\n- Added a blinking cursor to `FileDialog`'s custom text input in Pygame.\n- Improves UX/accessibility by clearly showing focus and cursor position.\n- Created `.Jules/palette.md` to document Pygame custom input UX learnings. (#362) (2311cad) - *Tony Sainez*

## 2026-05-09
- Fix unit AI to match the design: chassis dumb, immortal self-preserves (#357) (a2f9ac2) - *Tony Sainez*
- ⚡ Bolt: Replace O(N) ECS loops with O(K) component queries (#355) (589e1c2) - *Tony Sainez*

## 2026-05-08
- Close out FactoryBattleMap TODO (#354) (39f3533) - *Tony Sainez*

## 2026-05-07
- ⚡ Bolt: Optimize `Map.draw` by hoisting invariant rendering operations (#353) (fcc8fa1) - *Tony Sainez*
- Add developer console and performance profiler (#350) (3f024cb) - *Tony Sainez*
- docs: Add C++ optimization strategy and Pathfinder example (#349) (ce607cb) - *Tony Sainez*
- docs: Provide architectural review and proposed structure (#348) (8694fb7) - *Tony Sainez*
- chore(deps): update mkdocstrings-python requirement (#346) (a59ceff) - *dependabot[bot]*
- chore(deps): update mkdocstrings requirement from >=0.24.0 to >=1.0.4 (#345) (148db11) - *dependabot[bot]*
- chore(deps): bump softprops/action-gh-release from 2 to 3 (#344) (eb48c36) - *dependabot[bot]*
- chore: add privacy protections to .gitignore and fix .Jules/ casing (#347) (32290c3) - *Tony Sainez*

## 2026-03-16
- chore(deps): bump actions/upload-artifact from 6 to 7 (#342) (54d8442) - *dependabot[bot]*
- chore(deps): bump actions/download-artifact from 7 to 8 (#343) (36cbe20) - *dependabot[bot]*

## 2026-02-01
- chore(deps): bump actions/download-artifact from 4 to 7 (#334) (a0aceb0) - *dependabot[bot]*
- chore(deps): bump actions/checkout from 4 to 6 (#336) (5180a75) - *dependabot[bot]*
- chore(deps): bump actions/labeler from 5 to 6 (#337) (dd60e27) - *dependabot[bot]*
- chore(deps): bump actions/upload-artifact from 4 to 6 (#338) (7ad7467) - *dependabot[bot]*
- feat(perf): optimize targeting loop for sparse maps (#301) (4b541a7) - *google-labs-jules[bot]*
- feat(ux): Add floating damage numbers to combat (#299) (b2e46d8) - *google-labs-jules[bot]*
- chore(deps): bump actions/stale from 5 to 10 (#335) (0fb7498) - *dependabot[bot]*
- 🛡️ Sentinel: [HIGH] Restrict map saves to user data directory (#341) (b2a9035) - *Tony Sainez*

## 2026-01-27
- chore(deps): bump softprops/action-gh-release from 1 to 2 (#291) (41fed3e) - *dependabot[bot]*
- chore(deps): bump actions/setup-python from 4 to 6 (#290) (6f4b8c0) - *dependabot[bot]*
- perf: optimize SelectionSystem to use spatial hashing and component indexing (#288) (1bfe393) - *google-labs-jules[bot]*
- chore(deps): bump actions/cache from 4 to 5 (#292) (793a17a) - *dependabot[bot]*
- Configure testing and enhance documentation (#298) (94b71f2) - *google-labs-jules[bot]*
- Optimize rendering loop by hoisting tile_size calculation (#297) (441a35e) - *google-labs-jules[bot]*
- feat: Add blinking cursor to File Dialog for better UX (#296) (3d30697) - *google-labs-jules[bot]*
- 🛡️ Sentinel: Fix potential DoS in campaign loading (#295) (ac0bb63) - *google-labs-jules[bot]*
- chore(deps): bump actions/download-artifact from 4 to 7 (#294) (04f67ac) - *dependabot[bot]*
- chore(deps): bump actions/checkout from 4 to 6 (#293) (3e1d51c) - *dependabot[bot]*

## 2026-01-21
- feat(ui): display full unit names in info panel (#270) (5535e20) - *google-labs-jules[bot]*
- chore: enhance testing config, ci caching, and docs (#285) (a4a0d17) - *google-labs-jules[bot]*

## 2026-01-17
- feat: add pulse animation and help text to settings menu (#262) (e06c17b) - *google-labs-jules[bot]*
- ⚡ Bolt: Hybrid rendering iteration for sparse maps (#263) (2bb4471) - *google-labs-jules[bot]*
- feat(ux): unify pulse effect in settings scene (#274) (167059e) - *google-labs-jules[bot]*
- feat(security): Validate map input data to prevent crashes (#261) (6ecd3b9) - *google-labs-jules[bot]*
- feat: Add right-click to attack context sensitivity (#265) (c190bc1) - *google-labs-jules[bot]*
- feat(security): implement atomic file saving to prevent data corruption (#273) (84f8f30) - *google-labs-jules[bot]*
- Add comprehensive unit tests for GameScene to improve coverage. (#260) (3dacb45) - *google-labs-jules[bot]*
- security: enforce .json extension in Map.save_to_file (#257) (ae2f7b1) - *google-labs-jules[bot]*
- perf: Optimize ECS system iterations using component index (#255) (7022d1b) - *google-labs-jules[bot]*
- Fix: Enforce MAX_ENTITIES limit to prevent DoS (#254) (7ee1d87) - *google-labs-jules[bot]*
- chore: configure testing, docs, and ci stability (#264) (d8df3cf) - *google-labs-jules[bot]*
- feat(ui): Add hover tooltips for game units (#253) (bd79bf8) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize Fog of War update loop (#252) (2d8d3db) - *google-labs-jules[bot]*

## 2026-01-11
- 🎨 Add visual health bar to UI panel (#246) (ae9c1e7) - *google-labs-jules[bot]*
- Fix TOCTOU vulnerability in Map.load_from_file (#247) (7506f4e) - *google-labs-jules[bot]*
- 🎨 Palette: Add visual scrollbar to FileDialog (#250) (1889ad6) - *google-labs-jules[bot]*
- Sentinel: [HIGH] Fix path traversal in MusicManager (#243) (b1697c6) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize collision detection with zero-alloc check (#244) (ded5d0f) - *google-labs-jules[bot]*
- Add cursor feedback and coordinate tooltip to Map Editor. (#242) (8e01c9a) - *google-labs-jules[bot]*

## 2026-01-08
- Update ISSUES.md to remove implemented task (#241) (7320d24) - *google-labs-jules[bot]*
- Optimize enemy targeting search in Targeting.find_closest_enemy (#239) (6c00c20) - *google-labs-jules[bot]*
- Chore: Infrastructure and Release Workflow Improvements (#236) (d68b642) - *google-labs-jules[bot]*
- perf: Hoist calculations in RenderingSystem (#231) (66340ff) - *google-labs-jules[bot]*
- Fix TOCTOU vulnerability in CampaignManager file loading (#230) (00425a8) - *google-labs-jules[bot]*
- Fix incorrect assignment in GameScene and remove stale TODO (#225) (4c3270a) - *google-labs-jules[bot]*
- Docs: Mark 'Fix F-string in Editor Scene' as completed in ISSUES.md (#224) (cefc1f5) - *google-labs-jules[bot]*
- 🛡️ Sentinel: Fix path traversal in map loading (#223) (3efdd1e) - *google-labs-jules[bot]*
- Potential fix for code scanning alert no. 4: Workflow does not contain permissions (#240) (93beb5f) - *Tony Sainez*
- Add double-confirmation to Quit option in Main Menu (#222) (ea83587) - *google-labs-jules[bot]*
- Housekeeping: Update status of completed tasks and cleanup code (#221) (c752a29) - *google-labs-jules[bot]*
- feat: Throttle pathfinding retries (#202) (c772c86) - *google-labs-jules[bot]*
- Potential fix for code scanning alert no. 5: Workflow does not contain permissions (#238) (939d83e) - *Tony Sainez*
- docs: add Windows 11 build instructions and script for PyInstaller (1618061) - *Tony Sainez*
- Merge branch 'main' of https://github.com/tsainez/command-line-conflict (b69fce8) - *Tony Sainez*
- chore: clean up unused imports in game.py (98bbc66) - *Tony Sainez*

## 2026-01-07
- refactor: replace direct entity deletion with remove_entity method in ConfettiSystem (e5e397c) - *tsainez*
- style: clean up formatting in file dialog and test files (e4a97df) - *tsainez*

## 2026-01-04
- Fix TOCTOU vulnerability in Map.save_to_file (#215) (fae0e6b) - *google-labs-jules[bot]*
- feat: improve file dialog UX with empty state and input clipping (#216) (d8286c3) - *google-labs-jules[bot]*
- ⚡ Optimize UI range indicator rendering (#217) (7661612) - *google-labs-jules[bot]*
- 🎨 Palette: Add keyboard navigation to FileDialog (#219) (876e4d2) - *google-labs-jules[bot]*

## 2026-01-03
- ⚡ Bolt: Optimize UI text rendering with LRU cache (#213) (e911129) - *google-labs-jules[bot]*

## 2026-01-02
- Fix component access in GameScene and improve SelectionSystem coverage (#210) (e67aba6) - *google-labs-jules[bot]*
- Add context-aware cursors to GameScene (#211) (4b193d7) - *google-labs-jules[bot]*
- Fix symlink directory traversal in Map.save_to_file (#212) (a43cc4e) - *google-labs-jules[bot]*

## 2026-01-01
- ⚡ Bolt: Optimize UI text rendering with caching (#205) (bb3e14a) - *google-labs-jules[bot]*
- Fix path traversal vulnerability in Map.save_to_file (#207) (fbe40f4) - *google-labs-jules[bot]*
- Implement cursor feedback in Menu, Settings, and FileDialog (#208) (c5ce49b) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize AISystem and Targeting logic (#209) (41340e9) - *google-labs-jules[bot]*

## 2025-12-29
- feat: Add pulsing effect to selected menu option (#194) (a52eaed) - *google-labs-jules[bot]*
- Fix path traversal vulnerability in SoundSystem (#195) (eff9c49) - *google-labs-jules[bot]*
- Improve file dialog guidance and lint stability (#198) (ba3ce0b) - *Tony Sainez*
- Perf: Optimize entity iteration in CombatSystem (#199) (8fffcfd) - *google-labs-jules[bot]*
- chore: enhance stability, testing configuration, and documentation (#193) (9e827a0) - *google-labs-jules[bot]*

## 2025-12-28
- Implement fog of war smoothing for better visual transitions. (#192) (952aa73) - *google-labs-jules[bot]*
- Implement sound effect hooks and improve audio file support (#191) (b35018c) - *google-labs-jules[bot]*
- Implement FactoryBattleMap for factory battle scenarios (#189) (97fa01d) - *google-labs-jules[bot]*
- Implement Narrative Log System using ChatSystem (#188) (0ca4a4f) - *google-labs-jules[bot]*
- perf: optimize CombatSystem to iterate only over attackers (#187) (664972e) - *google-labs-jules[bot]*
- 🎨 Palette: Add context-aware construction hints (#186) (1d864c5) - *google-labs-jules[bot]*
- Update project structure documentation (#185) (1701078) - *google-labs-jules[bot]*
- ⚡ Bolt: Add Component Indexing to GameState (#184) (0e2de43) - *google-labs-jules[bot]*
- 🎨 Palette: Enhance Settings Menu UX (#183) (5322230) - *google-labs-jules[bot]*

## 2025-12-27
- feat: Optimize CombatSystem using squared distance check (#181) (7da6300) - *google-labs-jules[bot]*
- Maintain stability and update documentation (#182) (6298e75) - *google-labs-jules[bot]*

## 2025-12-26
- Fix: prevent DoS via special file loading in Map (#180) (c5b6f28) - *google-labs-jules[bot]*
- feat: Add auditory feedback to menu navigation (#179) (547a49e) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize confetti rendering loop (#177) (40d1630) - *google-labs-jules[bot]*
- chore: configure testing, docs deployment and pr templates (#178) (f4ddda4) - *google-labs-jules[bot]*

## 2025-12-25
- Add visual indicators and 'Continue Campaign' option to main menu (#175) (087cf26) - *google-labs-jules[bot]*
- Clean up RenderingSystem and improve test coverage (#176) (c9b9870) - *google-labs-jules[bot]*
- 🛡️ Sentinel: Fix unbounded filename input in FileDialog (#174) (9c93b91) - *google-labs-jules[bot]*
- Enhance documentation and GitHub integration (#173) (cc84012) - *google-labs-jules[bot]*
- Cache text surfaces in ChatSystem to optimize rendering (#172) (5be4127) - *google-labs-jules[bot]*
- feat: Add mouse interaction to Settings scene (#171) (c06ef41) - *google-labs-jules[bot]*

## 2025-12-24
- Configure GitHub Integration, testing and Docs (#170) (2021504) - *google-labs-jules[bot]*

## 2025-12-23
- 🎨 Palette: Add hover states to FileDialog (#166) (4b0c8bd) - *google-labs-jules[bot]*
- Sentinel: [CRITICAL/MEDIUM] Hardening against DoS attacks (#167) (a463c2c) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize Fog of War update for stationary units (#164) (f13c98a) - *google-labs-jules[bot]*
- Add chat feedback for hidden commands (Hold Position, Cheats) (#163) (6bf1fc2) - *google-labs-jules[bot]*
- Fix DoS vulnerability in CampaignManager save loading (#162) (d40f33b) - *google-labs-jules[bot]*
- Enable CI linting and update contributing docs (#161) (cdedca1) - *google-labs-jules[bot]*

## 2025-12-21
- Fix CI/CD pipeline and resolve linting/testing errors (#160) (327117a) - *google-labs-jules[bot]*
- feat(perf): Optimize FogOfWar rendering and updates (#159) (849b807) - *google-labs-jules[bot]*
- feat(ui): add mouse support to main menu (#158) (7c501f4) - *google-labs-jules[bot]*
- feat(security): Enforce file size limit in map loading (#157) (06b875b) - *google-labs-jules[bot]*
- Implement sound effects for selection, spawning, and game outcome (#156) (344949e) - *google-labs-jules[bot]*
- Update project structure doc (#138) (e7f7e66) - *Tony Sainez*
- Merge branch 'main' of https://github.com/tsainez/command-line-conflict (7b7e7ec) - *Tony Sainez*
- Add spacing after README checks block (#141) (9399fd8) - *Tony Sainez*
- ⚡ Bolt: Zero-copy pathfinding obstacles (#142) (a0b2a41) - *google-labs-jules[bot]*
- Remove redundant O(N) loop in RenderingSystem.draw (#146) (c614cb9) - *google-labs-jules[bot]*
- Remove obsolete TODO in editor.py (#151) (1cf8355) - *google-labs-jules[bot]*
- Implement in-game file dialog for loading/saving maps (#152) (94cedf1) - *google-labs-jules[bot]*
- 🛡️ Sentinel: [MEDIUM] Secure log file location and rotation (#145) (0c152d6) - *google-labs-jules[bot]*
- Remove unused variable in rendering system (#153) (724962f) - *google-labs-jules[bot]*
- Add test to skip reload when same track already playing (#139) (ea6eaef) - *Tony Sainez*
- Add SFX files (446751d) - *Tony Sainez*
- Simplify logger test env cleanup (#140) (b3e12d2) - *Tony Sainez*
- Format test_chat_dos with black (#150) (ba010e9) - *Tony Sainez*
- Remove unused import in engine.py and update ISSUES.md (#154) (5e034c7) - *google-labs-jules[bot]*
- Update ci.yml (cd62837) - *Tony Sainez*
- Fix: Resolve all Pylint errors causing CI build failures (#149) (a0c3ec2) - *google-labs-jules[bot]*
- feat: Add pre-commit script and GitHub templates (#143) (ef9b1eb) - *google-labs-jules[bot]*

## 2025-12-19
- 🛡️ Sentinel: [MEDIUM] Add input length limit to ChatSystem (#136) (ea169f1) - *google-labs-jules[bot]*
- Chore: Improve configuration, documentation, and CI/CD (#135) (fe12d1b) - *google-labs-jules[bot]*

## 2025-12-18
- Create stale.yml (65a002d) - *Tony Sainez*
- Create SECURITY.md (4594677) - *Tony Sainez*
- Fix pylint CI failure by installing deps and adding configuration (#134) (49783ef) - *google-labs-jules[bot]*
- feat: optimize FogOfWar update and render loops (#132) (69978a6) - *google-labs-jules[bot]*
- 🛡️ Sentinel: [MEDIUM] Fix CPU exhaustion in map loading (#131) (a7180cd) - *google-labs-jules[bot]*
- Identify code quality issues and create TODOs and Issue references. (#129) (ade8d1c) - *google-labs-jules[bot]*
- ⚡ Bolt: Implement Frustum Culling in RenderingSystem (#127) (79112c1) - *google-labs-jules[bot]*

## 2025-12-17
- Add Pylint workflow for Python code analysis (#128) (6609ff0) - *Tony Sainez*
- feat(ux): add visual ripple feedback for move commands (#126) (767f075) - *google-labs-jules[bot]*
- Add TODO_ISSUES.md to track pending tasks (#124) (f0489c1) - *google-labs-jules[bot]*
- Sentinel: [MEDIUM] Prevent DoS via map dimension limits (#122) (605459b) - *google-labs-jules[bot]*
- feat(ux): enhance health bar visuals and accessibility (#121) (9447cd0) - *google-labs-jules[bot]*
- chore: create ISSUES.md with instructions for pending TODOs (#120) (259d3d3) - *google-labs-jules[bot]*
- ⚡ Bolt: Optimize MovementSystem obstacle collection (#119) (02df7bd) - *google-labs-jules[bot]*

## 2025-12-15
- 🛡️ Sentinel: [MEDIUM] Gate cheat codes behind debug mode and disable debug by default (#118) (b6e2dff) - *google-labs-jules[bot]*
- Log movement issues and pathfinding failures (#114) (b932878) - *google-labs-jules[bot]*
- Add MkDocs configuration for documentation website (#116) (3e2d7e0) - *google-labs-jules[bot]*
- Add build script for PyInstaller executable and custom icon generation (#115) (e00eed5) - *google-labs-jules[bot]*

## 2025-12-14
- ⚡ Bolt: Optimize targeting with spatial hashing (#107) (990a918) - *google-labs-jules[bot]*
- feat: Relocate save files to user data directory for Steam Cloud support (#108) (c0af06f) - *google-labs-jules[bot]*
- Add audio volume controls to SettingsScene (#110) (ddf972f) - *google-labs-jules[bot]*
- Add Steamworks integration and achievements. (#111) (0d7f93e) - *google-labs-jules[bot]*
- Expand HealthSystem logging in debug mode (#106) (0f5be40) - *google-labs-jules[bot]*
- Expand logger usage in engine.py for better debugging (#103) (54d936b) - *google-labs-jules[bot]*
- Update Mission 1 initial units: 3 Chassis vs 1 Rover at center (#100) (920764e) - *google-labs-jules[bot]*
- Improve in-game controls help and add Space to pause (#83) (8b1088d) - *google-labs-jules[bot]*
- feat(ui): add dimmed overlay and instructions to pause screen (#101) (25f06fe) - *google-labs-jules[bot]*
- 🛡️ Sentinel: Fix path traversal in Map Editor console fallback (#102) (cbe1ecb) - *google-labs-jules[bot]*

## 2025-12-13
- ⚡ Bolt: Spatial Hashing for Collision Detection (#82) (8e5082e) - *google-labs-jules[bot]*
- Integrate logger in factories for debug mode (#99) (cf471ed) - *google-labs-jules[bot]*
- Integrate logger into Camera class for debug mode (#90) (6641079) - *google-labs-jules[bot]*
- Integrate logger into GameState for debug mode (#87) (1ed8d0b) - *google-labs-jules[bot]*
- Integrate logger into CorpseRemovalSystem for debug tracking (#91) (e9bab90) - *google-labs-jules[bot]*
- Integrate logger into UISystem for debug mode (#98) (10b3494) - *google-labs-jules[bot]*
- Integrate logger into Targeting utility (#95) (cd83551) - *google-labs-jules[bot]*
- feat: improve combat logging with entity names (#92) (ceee63c) - *google-labs-jules[bot]*
- Integrate logger into MovementSystem (#97) (88ce941) - *google-labs-jules[bot]*
- Integrate logger into RenderingSystem (#89) (f139743) - *google-labs-jules[bot]*
- Integrate logger into SelectionSystem (#88) (99722c6) - *google-labs-jules[bot]*
- Enable daily updates for pip in dependabot.yml (cfe443a) - *Tony Sainez*
- Integrate logger into FleeSystem (#93) (054b9a0) - *google-labs-jules[bot]*
- Integrate logger into AISystem for target acquisition (#94) (3559a42) - *google-labs-jules[bot]*
- Integrate logger into GameState and respect config.DEBUG (#86) (17c63e3) - *google-labs-jules[bot]*
- Add logging to CorpseRemovalSystem for debugging purposes. (#85) (2b74904) - *google-labs-jules[bot]*
- Integrate logger into FogOfWar (#84) (c0a4118) - *google-labs-jules[bot]*

## 2025-12-09
- Map Editor Feature (#80) (630f99d) - *google-labs-jules[bot]*

## 2025-12-06
- Add cross-platform environment setup instructions to README.md (#77) (f47c410) - *google-labs-jules[bot]*
- Log cheat commands in DEBUG mode and fix UI system syntax error (#78) (562628e) - *google-labs-jules[bot]*
- Fix intelligent units clipping through obstacles when target set directly. (#79) (0c9ef44) - *google-labs-jules[bot]*
- Implement Win/Loss Conditions (#74) (45763d4) - *google-labs-jules[bot]*
- Merge branch 'main' of https://github.com/tsainez/command-line-conflict (644e3f1) - *tsainez*
- Add ranged attack sound effect (a08a481) - *tsainez*

## 2025-12-04
- Add save_game.json to .gitignore (f0de6a1) - *tsainez*
- Refactor camera controls to use Arrow Keys and Middle Mouse Drag (#75) (9e61379) - *google-labs-jules[bot]*
- Fix Fog of War rendering and integration (#70) (257f502) - *google-labs-jules[bot]*
- Add in-game chat system (#56) (a7f94c4) - *google-labs-jules[bot]*
- Add cheat codes for testing (#63) (da31fac) - *google-labs-jules[bot]*
- Add ability to switch sides for manual testing (#69) (f5080c2) - *google-labs-jules[bot]*

## 2025-12-03
- Refactor RenderingSystem to cache text surfaces for performance. (#67) (05676d9) - *google-labs-jules[bot]*
- Implement campaign tech tree and unit production system (#55) (74a9661) - *google-labs-jules[bot]*
- Add AGENTS.md with 100 autonomous coding tasks (#54) (61b9360) - *google-labs-jules[bot]*
- Improve test coverage for core systems and engine (#53) (0a5efa7) - *google-labs-jules[bot]*
- Add unit health indicators. (#60) (2045d9e) - *google-labs-jules[bot]*
- Implement 'Hold Position' command (Key: H) (#59) (353aa38) - *google-labs-jules[bot]*
- Merge pull request #58 from tsainez/feature/background-music (6ce8ae7) - *Tony Sainez*
- Merge branch 'main' into feature/background-music (7b7e3a5) - *Tony Sainez*
- Merge pull request #57 from tsainez/neutral-creeps (fddd72f) - *Tony Sainez*
- Merge branch 'main' into neutral-creeps (86ea7b4) - *Tony Sainez*
- chore: Initialize VSCode settings for Python testing configuration (c338885) - *tsainez*
- Merge pull request #66 from tsainez/accel-tests-xdist (9778b66) - *Tony Sainez*
- linting (b6931f6) - *tsainez*

## 2025-12-04
- Add sound effects system and combat sounds (0b5d481) - *google-labs-jules[bot]*
- Add background music support (3ae9115) - *google-labs-jules[bot]*
- Accelerate test suite with parallel execution (e273d4a) - *google-labs-jules[bot]*
- Add background music support (c275531) - *google-labs-jules[bot]*
- Add neutral wildlife creeps and wandering behavior (42e3934) - *google-labs-jules[bot]*

## 2025-09-26
- Merge pull request #52 from tsainez/confetti-effect (eb2e608) - *Tony Sainez*

## 2025-09-24
- test: Add test for interrupting attacks with move commands (b50f068) - *google-labs-jules[bot]*
- feat: Allow move commands to interrupt attacks (50fe155) - *google-labs-jules[bot]*
- test: Add logging and tests for confetti effect (cf08391) - *google-labs-jules[bot]*
- fix: Address feedback on confetti visibility and AI behavior (5e824f5) - *google-labs-jules[bot]*
- refactor: Remove requirements-dev.txt and update CI (4dc0c2e) - *google-labs-jules[bot]*
- fix: Create empty requirements-dev.txt to fix CI (d007ee9) - *google-labs-jules[bot]*

## 2025-09-18
- feat: Add confetti effect for ranged attacks (6383cc8) - *google-labs-jules[bot]*

## 2025-09-17
- Merge pull request #51 from tsainez/fix/additive-drag-selection (149ee0d) - *Tony Sainez*

## 2025-09-18
- feat(selection): Implement additive drag-selection with Shift key (2ddada1) - *google-labs-jules[bot]*

## 2025-09-17
- Linting & docs (76fdc9d) - *tsainez*
- Merge pull request #50 from tsainez/feature/unit-collision-avoidance (7f9bb8d) - *Tony Sainez*
- Implement unit collision avoidance and intelligent pathfinding. (e96dfa8) - *google-labs-jules[bot]*
- Merge pull request #48 from tsainez/fix/attack-range-display (edd289f) - *Tony Sainez*
- Feat: Add detection range and snap health bar to grid (a3939f9) - *google-labs-jules[bot]*
- Fix: Correct test assertions for UI system (0aadd71) - *google-labs-jules[bot]*
- Fix failing tests for UI system (048332c) - *google-labs-jules[bot]*
- Refactor: Use aggregate attack range display for single units (8ae418e) - *google-labs-jules[bot]*
- Merge pull request #47 from tsainez/fix/attack-range-display (22d19ec) - *Tony Sainez*
- Fix attack range display and add aggregate view (f081dd4) - *google-labs-jules[bot]*
- Merge pull request #46 from tsainez/feature/update-debug-system (7582ad0) - *Tony Sainez*
- Feat: Update debug system to be more useful (0c6fc21) - *google-labs-jules[bot]*

## 2025-09-16
- Merge pull request #45 from tsainez/fix-grid-and-ai (f9c4cf5) - *Tony Sainez*
- Fix FleeSystem crash and centralize targeting logic (ada52ee) - *google-labs-jules[bot]*
- Fix grid rendering and implement enemy AI (d06d716) - *google-labs-jules[bot]*
- Merge pull request #44 from tsainez/feature/camera-controls (c1d5f4a) - *Tony Sainez*

## 2025-09-14
- Implement camera movement and zoom controls (c990c7c) - *google-labs-jules[bot]*
- Merge pull request #41 from tsainez/feat/camera-tests (cf32f05) - *Tony Sainez*
- Merge branch 'main' into feat/camera-tests (911df0d) - *Tony Sainez*
- fix(camera): Correct mouse coordinates and selection visuals (12fc361) - *google-labs-jules[bot]*
- fix(camera): Correct mouse coordinates for camera offset (094f2ab) - *google-labs-jules[bot]*
- Merge pull request #42 from tsainez/fix-game-crashes (5a8e215) - *Tony Sainez*
- Fix game crash and visual bugs (aec4336) - *google-labs-jules[bot]*
- feat(camera): Add more tests for camera rendering (6499ffe) - *google-labs-jules[bot]*
- Merge pull request #39 from tsainez/feature/player-system (40fcb11) - *Tony Sainez*
- feat: Create a player system with color-coded units (e309d52) - *google-labs-jules[bot]*

## 2025-09-13
- Implement camera view (b75e8f0) - *Tony Sainez*
- Merge pull request #36 from tsainez/feature/in-game-ui (1ecf1a7) - *Tony Sainez*
- Merge branch 'main' into feature/in-game-ui (d33cff2) - *Tony Sainez*
- feat: Add pause message and various UI fixes (ff04771) - *google-labs-jules[bot]*
- Merge pull request #34 from tsainez/add-comprehensive-documentation (2a5f03f) - *Tony Sainez*
- Merge pull request #35 from tsainez/feature/improve-test-coverage (c3ee0e9) - *Tony Sainez*
- feat: Add pause and fix UI bugs (a2f3e08) - *google-labs-jules[bot]*
- feat: Improve test coverage for components and systems (e944b25) - *google-labs-jules[bot]*
- Add comprehensive documentation to the entire repository (ac6ded0) - *google-labs-jules[bot]*
- fix: Correct UI layout and add dead state (bc5f439) - *google-labs-jules[bot]*

## 2025-09-12
- Merge pull request #29 from tsainez/feature/in-game-ui (e6d7f99) - *Tony Sainez*
- feat: Implement dead state and fix UI bugs (9b6efcf) - *google-labs-jules[bot]*

## 2025-09-11
- Merge pull request #32 from tsainez/add-ci-and-observer-test (ca148ae) - *Tony Sainez*

## 2025-09-12
- feat: Add observer retreat test and CI (704a071) - *google-labs-jules[bot]*
- feat: Implement in-game user interface (e6b1aa4) - *google-labs-jules[bot]*
- feat: Implement in-game user interface (e1b4155) - *google-labs-jules[bot]*

## 2025-09-11
- Merge pull request #26 from tsainez/feature/menu-system (ae213a5) - *Tony Sainez*
- Linting & reformatting (3eb40e3) - *tsainez*

## 2025-09-12
- feat: Implement menu system (a5ca82e) - *google-labs-jules[bot]*

## 2025-09-11
- Merge pull request #24 from tsainez/fix/pytest-mocker-fixture (082e687) - *Tony Sainez*
- fix(deps): add pytest-mock to dev requirements (6a4d0ec) - *google-labs-jules[bot]*
- Merge pull request #22 from tsainez/feature/improve-testing-and-logging (dad45c1) - *Tony Sainez*
- Stop tracking game.log (5961d2e) - *tsainez*
- Delete game.log (a2bb045) - *tsainez*
- feat: Improve testing and logging systems (b98f285) - *google-labs-jules[bot]*

## 2025-09-10
- Update .gitignore (4d7d24d) - *tsainez*
- Merge pull request #21 from tsainez/feature/right-click-movement (18cec53) - *Tony Sainez*
- Remove output logs, add comments (b9cf0f1) - *tsainez*
- fix: Correct right-click movement and add logging (ef618ee) - *google-labs-jules[bot]*

## 2025-09-06
- feat: Implement click-to-select and right-click movement (f05ab0a) - *google-labs-jules[bot]*

## 2025-09-05
- feat: Complete rewrite to ECS architecture (80d5c61) - *google-labs-jules[bot]*

## 2025-08-03
- Merge pull request #19 from tsainez/feature/combat-and-fleeing (7548479) - *Tony Sainez*

## 2025-08-04
- feat: Implement combat and fleeing mechanics (73c3dd4) - *google-labs-jules[bot]*

## 2025-08-03
- Elaborated docstrings (84ad311) - *tsainez*
- Merge pull request #18 from tsainez/add-testing-suite (00c9c09) - *Tony Sainez*
- feat: Add testing suite for the game (f1136eb) - *google-labs-jules[bot]*
- Merge pull request #17 from tsainez/feature/unit-overhaul (49b631c) - *Tony Sainez*
- feat: Overhaul unit system, add hotkeys, and fix bugs (2674cfa) - *google-labs-jules[bot]*

## 2025-07-31
- feat: Overhaul unit system and add spawn hotkeys (f7d0929) - *google-labs-jules[bot]*
- feat: Overhaul unit system with AI-based design (dfe5ba1) - *google-labs-jules[bot]*
- Fix unit collision by implementing path recalculation (#16) (341dbd0) - *google-labs-jules[bot]*
- Merge pull request #15 from tsainez/feature/unit-collision (949691e) - *Tony Sainez*
- feat: Implement unit collision avoidance (1378a9e) - *google-labs-jules[bot]*

## 2025-07-30
- Merge pull request #14 from tsainez/add-windows-install-docs (e4c9c8e) - *Tony Sainez*

## 2025-07-31
- I've corrected the git clone URL in the Windows installation guide. (35b3bdf) - *google-labs-jules[bot]*
- docs: Create Windows installation guide (030437f) - *google-labs-jules[bot]*

## 2025-07-29
- Merge pull request #12 from tsainez/feature/update-readme-and-add-docs (f5538d8) - *Tony Sainez*
- Merge pull request #13 from tsainez/feature/unit-properties (55296fc) - *Tony Sainez*
- Add health, attack range, and speed to units (9750d6c) - *google-labs-jules[bot]*
- feat: Update README and add detailed documentation (ea8ada7) - *google-labs-jules[bot]*
- Merge pull request #11 from tsainez/refactor-unit-structure (cbe04ff) - *Tony Sainez*
- Refactor unit file structure (fd8d889) - *google-labs-jules[bot]*

## 2025-07-04
- Merge pull request #10 from tsainez/codex/fix-bug-with-unit-paths-not-displaying (40324b3) - *Tony Sainez*
- Improve path visualization for units (a26bb04) - *Tony Sainez*

## 2025-06-29
- Merge pull request #9 from tsainez/codex/update-ui-graphics-with-custom-font-support (c9a8a81) - *Tony Sainez*
- Load bundled font and add ASCII fallback (e7b7515) - *Tony Sainez*
- Add fonts for prettier graphics (19abd42) - *tsainez*
- Merge pull request #8 from tsainez/codex/fix-unit-path-rendering-bug (5cf88fe) - *Tony Sainez*
- Improve font fallback (cfce966) - *Tony Sainez*
- Merge pull request #7 from tsainez/codex/overhaul-unit-movement-ui-and-fix-selection-bug (3255760) - *Tony Sainez*
- Use arrow lines for move path (0ad3dc1) - *Tony Sainez*
- Merge pull request #6 from tsainez/codex/overhaul-unit-movement-ui-and-fix-selection-bug (149df21) - *Tony Sainez*
- Show move paths and fix single-tile selection (61a7307) - *Tony Sainez*
- Add instructions for linting (cff2254) - *tsainez*
- Merge pull request #5 from tsainez/codex/implement-walls-and-pathfinding-for-ground-units (edd59a3) - *Tony Sainez*
- Add wall pathfinding and air/ground unit types (482e3fc) - *Tony Sainez*

## 2025-06-26
- Highlight selected units (4c9cf69) - *tsainez*
- Ignore all __pycache__ directories and compiled Python files (ee3e621) - *tsainez*
- Merge pull request #4 from tsainez/codex/refactor-repository-for-future-expansion (5c723a5) - *Tony Sainez*
- Add map system and runtime unit spawning (5d72241) - *Tony Sainez*
- Merge pull request #3 from tsainez/codex/refactor-repository-for-future-expansion (23586bc) - *Tony Sainez*
- Refactor into package with units submodule (4874a90) - *Tony Sainez*

## 2025-06-25
- Undo mistake (0b6b116) - *tsainez*
- Create pylint.yml (c905311) - *Tony Sainez*
- Add requirements (fec65bd) - *tsainez*
- Merge pull request #2 from tsainez/codex/implement-pixel-per-second-movement (3c6513d) - *Tony Sainez*
- Implement delta-time movement (7031f7a) - *Tony Sainez*
- Remove CI pre-conditions (0720f05) - *tsainez*
- Add project configuration files (ffa2606) - *tsainez*
- Merge pull request #1 from tsainez/codex/initialize-basic-rts-game-prototype (a8ff078) - *Tony Sainez*
- Add Python RTS prototype (5a3f498) - *Tony Sainez*
- Create README.md (f1580b1) - *Tony Sainez*