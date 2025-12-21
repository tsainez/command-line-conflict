import os
import subprocess
import sys

import PyInstaller.__main__


def build():
    # 1. Generate Icon
    if not os.path.exists("icon.ico"):
        print("Icon not found. Generating default icon...")
        script_path = os.path.join("scripts", "generate_icon.py")
        if os.path.exists(script_path):
            subprocess.check_call([sys.executable, script_path])
        else:
            print(f"Error: {script_path} not found.")
            sys.exit(1)

    if not os.path.exists("icon.ico"):
        print("Error: Failed to generate icon.ico")
        sys.exit(1)

    # 2. Configure PyInstaller
    sep = ";" if sys.platform.startswith("win") else ":"

    datas = [
        f"command_line_conflict/fonts{sep}command_line_conflict/fonts",
        f"command_line_conflict/sounds{sep}command_line_conflict/sounds",
    ]

    args = [
        "main.py",
        "--name=Command Line Conflict",
        "--onefile",
        "--windowed",
        f"--icon=icon.ico",
        "--clean",
        "--log-level=INFO",
    ]

    for data in datas:
        args.append(f"--add-data={data}")

    print(f"Building executable with args: {args}")

    # 3. Run Build
    PyInstaller.__main__.run(args)

    print("\nBuild complete.")
    dist_folder = "dist"
    executable_name = "Command Line Conflict" + (".exe" if sys.platform.startswith("win") else "")
    executable_path = os.path.join(dist_folder, executable_name)

    if os.path.exists(executable_path):
        print(f"Executable created at: {executable_path}")
    else:
        print("Error: Executable not found after build.")
        sys.exit(1)


if __name__ == "__main__":
    build()
