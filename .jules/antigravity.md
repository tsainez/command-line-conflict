## 2026-07-03 - Neutral Unit Resource Harvesting & Factory Building
**Changes:**
- Created `ResourceDeposit` component to track scrap value of entities.
- Implemented `create_scrap` factory function to spawn gold `$` scrap entities.
- Created `ResourceSystem` to handle player units walking over scrap, incrementing resources, showing `+50 Scrap` floating text, and playing sound.
- Integrated `ResourceSystem` and initialized player resource pools in `GameState`.
- Configured neutral unit death in `HealthSystem` to drop scrap.
- Enforced scrap costs when constructing factories in `scenes/game.py` (100 for Rover, 150 for Arachnotron) and displaying chat warning log if resources are insufficient.
- Enabled right-click targeting to allow attacking of neutral player units.
- Updated HUD to render current scrap count, display costs in construction hints, and render scrap amount in tooltips.
- Fixed coordinate collision detection and A* pathfinding to ignore dead units and resource/scrap deposits so player units can walk over and collect them.
- Added `C` hotkey to selected factories (Rover and Arachnotron factories) to train a builder unit (`chassis`) for 50 Scrap. Units spawn at an adjacent non-blocking tile, facilitating a complete gameplay loop.
- Added `T` hotkey to selected Rover Factories to research Arachnotron tech. Research requires having at least 6 Chassis units alive on the map and costs 100 Scrap.
- Added `R` hotkey to selected Arachnotron Factories to train a `rover` directly for 80 Scrap.
- Added `A` hotkey to selected Arachnotron Factories to train an `arachnotron` for 120 Scrap. This requires and consumes a friendly `rover` standing in an adjacent tile.
- Reduced the starting Chassis count for human players to exactly 3 (and removed the starting Rover) in `maps/factory_battle_map.py` to create the desired early game progression.
- Added a "Mute Audio" option in the settings options menu that toggles all background music and sound effects.
- Added unit tests in `tests/unit/test_resources.py` and `tests/unit/systems/test_ui_system_unit_info.py` verifying the factory training mechanics, research unlock requirement logic, Arachnotron adjacent-rover consumption training, and the Settings scene mute logic, keeping test coverage above the 80% project threshold.

**Learning:** Decoupling gameplay events (like resource drops on unit death or overlap collection) into specialized ECS components (`ResourceDeposit`) and dedicated systems (`ResourceSystem`) ensures that logic checks remain highly performant, testable, and isolated. Additionally, ensuring that decorative or collectible items do not register as blocking obstacles in spatial map queries is critical for smooth unit movement and pathing.
**Model:** Gemini 3.5 Flash (High)
