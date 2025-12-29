#!/usr/bin/env python3
"""
Generates a CHANGELOG.md file from git history.
"""
import subprocess


def get_git_log():
    try:
        # Get log in format: hash|date|author|message
        cmd = ["git", "log", "--pretty=format:%h|%ad|%an|%s", "--date=short"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git not installed.")
        return []


def parse_log(log_lines):
    changes = []
    for line in log_lines:
        parts = line.split("|")
        if len(parts) >= 4:
            changes.append({"hash": parts[0], "date": parts[1], "author": parts[2], "message": "|".join(parts[3:])})
    return changes


def generate_markdown(changes):
    if not changes:
        return "# Changelog\n\nNo changes found or not a git repository."

    output = ["# Changelog\n"]

    # Group by date (descending)
    current_date = None

    for change in changes:
        if change["date"] != current_date:
            current_date = change["date"]
            output.append(f"\n## {current_date}")

        output.append(f"- {change['message']} ({change['hash']}) - *{change['author']}*")

    return "\n".join(output)


def main():
    print("Generating CHANGELOG.md...")
    log_lines = get_git_log()
    changes = parse_log(log_lines)
    markdown = generate_markdown(changes)

    with open("CHANGELOG.md", "w") as f:
        f.write(markdown)

    print(f"CHANGELOG.md generated with {len(changes)} entries.")


if __name__ == "__main__":
    main()
