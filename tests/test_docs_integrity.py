import os
import yaml
import pytest

def get_markdown_files_from_nav(nav):
    """Recursively extract markdown file paths from mkdocs nav."""
    files = []
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    files.extend(get_markdown_files_from_nav(value))
                elif isinstance(value, str):
                    files.append(value)
        elif isinstance(item, str):
            files.append(item)
    return files

def test_mkdocs_nav_files_exist():
    """Verify that all files referenced in mkdocs.yml navigation exist."""
    mkdocs_path = 'mkdocs.yml'

    # Check if mkdocs.yml exists
    assert os.path.exists(mkdocs_path), "mkdocs.yml not found"

    with open(mkdocs_path, 'r') as f:
        config = yaml.safe_load(f)

    nav = config.get('nav', [])
    docs_dir = 'docs'

    files = get_markdown_files_from_nav(nav)

    missing_files = []
    for file_path in files:
        # mkdocs file paths are relative to docs_dir
        full_path = os.path.join(docs_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(full_path)

    assert not missing_files, f"The following documentation files referenced in mkdocs.yml are missing: {missing_files}"
