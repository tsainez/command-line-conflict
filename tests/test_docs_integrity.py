import os
import re
from pathlib import Path

import pytest
import yaml  # type: ignore

DOCS_DIR = Path("docs")
MKDOCS_FILE = Path("mkdocs.yml")
PROJECT_ROOT = Path(".")


def get_mkdocs_nav_files(nav_entry):
    """Recursively extract file paths from mkdocs nav."""
    files = []
    if isinstance(nav_entry, list):
        for item in nav_entry:
            files.extend(get_mkdocs_nav_files(item))
    elif isinstance(nav_entry, dict):
        for key, value in nav_entry.items():
            files.extend(get_mkdocs_nav_files(value))
    elif isinstance(nav_entry, str):
        files.append(nav_entry)
    return files


def test_mkdocs_nav_files_exist():
    """Verify that all files referenced in mkdocs.yml exist."""
    if not MKDOCS_FILE.exists():
        pytest.fail("mkdocs.yml not found")

    with open(MKDOCS_FILE, "r") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_files = get_mkdocs_nav_files(nav)

    for file_path in nav_files:
        # mkdocs paths are relative to docs_dir (default: docs)
        full_path = DOCS_DIR / file_path
        assert full_path.exists(), f"File referenced in mkdocs.yml not found: {full_path}"


def test_no_orphaned_docs():
    """Verify that all markdown files in docs/ are referenced in mkdocs.yml."""
    if not MKDOCS_FILE.exists():
        pytest.fail("mkdocs.yml not found")

    with open(MKDOCS_FILE, "r") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_files = set(get_mkdocs_nav_files(nav))

    # Normalize mkdocs paths to handle potential inconsistent slashes (though usually forward)
    nav_files = {str(Path(p)).replace("\\", "/") for p in nav_files}

    # Collect all markdown files in docs/
    actual_files = set()
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                rel_path = Path(root).relative_to(DOCS_DIR) / file
                # Normalize path separators
                str_path = str(rel_path).replace("\\", "/")
                actual_files.add(str_path)

    orphans = actual_files - nav_files

    assert not orphans, f"Orphaned documentation files found: {orphans}"


def test_internal_links():
    """Check for broken relative links in markdown files."""
    link_pattern = re.compile(r"\[.*?\]\((.*?)\)")

    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                links = link_pattern.findall(content)
                for link in links:
                    # Ignore external links
                    if link.startswith("http") or link.startswith("mailto:"):
                        continue

                    # Ignore anchor links
                    if link.startswith("#"):
                        continue

                    # Handle anchors in links (file.md#anchor)
                    link_target = link.split("#")[0]

                    # If link was just "#anchor", link_target is empty string
                    if not link_target:
                        continue

                    # Handle absolute paths (relative to docs root in some contexts, but let's assume relative to file)
                    # If it starts with /, it might be relative to project root or docs root.
                    # MkDocs usually treats / as relative to docs root.
                    if link_target.startswith("/"):
                        target_candidate = DOCS_DIR / link_target.lstrip("/")
                    else:
                        target_candidate = Path(root) / link_target

                    assert target_candidate.exists(), f"Broken link in {file_path}: {link}"


def test_project_structure_matches_code():
    """Verify ProjectStructure.md lists all systems and components."""
    structure_file = DOCS_DIR / "ProjectStructure.md"
    assert structure_file.exists()

    with open(structure_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check Systems
    systems_dir = PROJECT_ROOT / "command_line_conflict" / "systems"
    if systems_dir.exists():
        for file in systems_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            assert file.name in content, f"System {file.name} is missing from ProjectStructure.md"

    # Check Components
    components_dir = PROJECT_ROOT / "command_line_conflict" / "components"
    if components_dir.exists():
        for file in components_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            assert file.name in content, f"Component {file.name} is missing from ProjectStructure.md"
