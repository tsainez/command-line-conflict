# Running on Windows 11 Home

This guide provides step-by-step instructions for setting up and running the game on a Windows 11 Home PC from scratch.

## 1. Install Python

The easiest way to install Python on Windows is through the Microsoft Store.

1.  Open the **Microsoft Store** app.
2.  Search for "Python".
3.  Select the latest version of Python (e.g., Python 3.11) and click **Install**.

Alternatively, you can download the official Python installer from the [python.org website](https://www.python.org/downloads/windows/). If you use the installer, make sure to check the box that says **"Add Python to PATH"** during installation.

## 2. Get the Game Files

You'll need `git` to download the game files. If you don't have it, you can download it from [git-scm.com](https://git-scm.com/download/win).

1.  Open **Command Prompt** or **PowerShell**. You can find these by searching in the Start Menu.
2.  Clone the repository using the following command:
    ```
    git clone https://github.com/tsainez/command-line-conflict.git
    ```
3.  Navigate into the newly created directory:
    ```
    cd command-line-conflict
    ```

## 3. Set Up a Virtual Environment

A virtual environment is a self-contained directory that contains a specific version of Python and any additional packages you install. This is the recommended way to manage project dependencies.

1.  From the `command-line-conflict` directory in your terminal, create a virtual environment named `.venv`:
    ```
    python -m venv .venv
    ```
2.  Activate the virtual environment:
    ```
    .venv\\Scripts\\activate
    ```
    Your command prompt should now have a `(.venv)` prefix, indicating that the virtual environment is active.

## 4. Install Dependencies

Install the necessary Python packages using `pip`, the Python package installer.

1.  Upgrade `pip` to the latest version:
    ```
    pip install --upgrade pip
    ```
2.  Install the game's dependencies from the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

## 5. Run the Game

You are now ready to run the game!

1.  Make sure your virtual environment is still active.
2.  Run the `main.py` script:
    ```
    python main.py
    ```
The game should now launch in a new window.

## (Optional) Create a Standalone Executable

If you want to run the game without using the command line every time, you can bundle it into a single `.exe` file using `PyInstaller`.

1.  Install `PyInstaller`:
    ```
    pip install pyinstaller
    ```
2.  Run the following command to create the executable:
    ```
    pyinstaller --onefile main.py
    ```
3.  The standalone executable will be located in the `dist` directory. You can run `dist/main.exe` to play the game.
