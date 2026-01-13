#!/usr/bin/env python3
"""
Generates a CHANGELOG.md based on git history.
Uses Conventional Commits logic to categorize changes.
"""

import datetime
import re
import subprocess


def get_git_commits():
    """Retrieves git commits."""
    # Try to get commits from the last tag, or all if no tags exist.
    try:
        last_tag = (
            subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
        )
        log_range = f"{last_tag}..HEAD"
    except subprocess.CalledProcessError:
        log_range = "HEAD"
        print("No tags found. Generating changelog for all commits.")

    # Format: hash|author|date|subject
    cmd = ["git", "log", log_range, "--pretty=format:%h|%an|%ad|%s", "--date=short"]
    try:
        output = subprocess.check_output(cmd).decode("utf-8")
        return output.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        return []


def parse_commits(lines):
    """Parses commit lines into categories."""
    categories = {
        "feat": [],
        "fix": [],
        "docs": [],
        "style": [],
        "refactor": [],
        "perf": [],
        "test": [],
        "chore": [],
        "other": [],
    }

    # Regex for conventional commits: type(scope)!: subject
    cc_regex = re.compile(r"^(\w+)(?:\(([^)]+)\))?(!)?: (.+)$")

    for line in lines:
        parts = line.split("|")
        if len(parts) < 4:
            continue

        commit_hash, author, _, subject = parts[0], parts[1], parts[2], parts[3]

        match = cc_regex.match(subject)
        if match:
            c_type = match.group(1).lower()
            c_scope = match.group(2)
            c_breaking = match.group(3)
            c_desc = match.group(4)

            # Map conventional types to our categories
            if c_type in categories:
                key = c_type
            else:
                key = "other"

            entry = f"- {c_desc} ({commit_hash}) - *{author}*"
            if c_scope:
                entry = f"- **{c_scope}**: {c_desc} ({commit_hash}) - *{author}*"
            if c_breaking:
                entry = f"⚠️ {entry}"

            categories[key].append(entry)
        else:
            categories["other"].append(f"- {subject} ({commit_hash}) - *{author}*")

    return categories


def generate_markdown(categories):
    """Generates Markdown content."""
    today = datetime.date.today().isoformat()
    md = f"# Changelog\n\n## Unreleased ({today})\n\n"

    mapping = {
        "feat": "Features",
        "fix": "Bug Fixes",
        "perf": "Performance Improvements",
        "docs": "Documentation",
        "refactor": "Refactoring",
        "test": "Testing",
        "style": "Styles",
        "chore": "Chores",
        "other": "Other Changes",
    }

    for key, title in mapping.items():
        if categories[key]:
            md += f"### {title}\n"
            for item in categories[key]:
                md += f"{item}\n"
            md += "\n"

    return md


def main():
    commits = get_git_commits()
    if not commits:
        print("No commits found.")
        return

    categories = parse_commits(commits)
    new_content = generate_markdown(categories)

    filename = "CHANGELOG.md"

    # Read existing changelog if it exists to append/prepend
    existing_content = ""
    try:
        with open(filename, "r") as f:
            existing_content = f.read()
    except FileNotFoundError:
        pass

    # Simple strategy: If "Unreleased" section exists in file, replace it?
    # Or just prepend the new stuff?
    # For this simple script, we will just prepend the new unreleased section
    # assuming this runs before a release.

    # However, to avoid duplicating "Unreleased" if run multiple times,
    # we might want to just overwrite or warn.
    # Let's just write to stdout or a new file for now, or overwrite if requested.

    print("--- Generated Changelog Content ---")
    print(new_content)

    # Write to file
    with open(filename, "w") as f:
        f.write(new_content)
        if existing_content:
            # If existing content has a header, skip it?
            # This is a basic implementation.
            f.write("\n\n" + existing_content)

    print(f"Updated {filename}")


if __name__ == "__main__":
    main()
