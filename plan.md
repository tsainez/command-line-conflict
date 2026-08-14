1. **Fix `ui_system.py` tooltips:**
   - Modify `command_line_conflict/systems/ui_system.py` to replace `identity.name.title()` with `identity.name.replace("_", " ").title()`.
2. **Fix `movement_system.py` stuck notifications:**
   - Modify `command_line_conflict/systems/movement_system.py` to replace `identity.name.capitalize()` with `identity.name.replace("_", " ").title()`.
3. **Run tests & verification:**
   - `python3 -m pytest -q`
   - `black --check .`
4. **Pre-commit checks**
   - Run `pre_commit_instructions` as standard practice.
5. **Create Pull Request:**
   - Submit the changes using the `create_pull_request` format with the appropriate persona.
