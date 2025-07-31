# command-line-conflict

A fast-paced, open-source RTS game inspired by Starcraft, rendered entirely in charming ASCII art and designed for cross-platform play.

## Getting Started

> **Note for Windows users:** For detailed, step-by-step instructions, please see our [Windows Installation Guide](docs/WindowsInstallation.md).

This project uses **Python** and `pygame` for its simple and readable implementation. To run the prototype:

1) From your repo root, create & activate a venv
```
python3 -m venv .venv           # or “python -m venv .venv”
source .venv/bin/activate
```

2) Upgrade pip and install requirements
```
pip install --upgrade pip
pip install -r requirements.txt
```

3) (Optional) Run linters/tests
```
pip install black isort pytest  # needed for optional linting/tests

black --check .
isort --check-only .
pytest -q
```

4) Launch the game
`python main.py`

5) (Optional) Bundle into a single executable with PyInstaller
```
pip install pyinstaller
pyinstaller --onefile main.py
# → dist/main  is your standalone binary
```

## Documentation

For more detailed documentation, please see the following files in the `docs` directory:

*   [Windows Installation](docs/WindowsInstallation.md)
*   [Project Structure](docs/ProjectStructure.md)
*   [Maps](docs/Maps.md)
*   [Unit Types](docs/UnitTypes.md)
*   [Controls](docs/Controls.md)
*   [Contributing](docs/Contributing.md)
