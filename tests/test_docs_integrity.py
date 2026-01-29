import os
import re

import pytest
import yaml  # type: ignore


def get_mkdocs_nav_files(nav):
    """Recursively extract file paths from mkdocs nav."""
    files = []
    for item in nav:
        if isinstance(item, str):
            files.append(item)
        elif isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    files.extend(get_mkdocs_nav_files(value))
                else:
                    files.append(value)
    return files


def test_mkdocs_integrity():
    """Verify that all files referenced in mkdocs.yml exist."""
    if not os.path.exists("mkdocs.yml"):
        pytest.skip("mkdocs.yml not found")

    with open("mkdocs.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav_files = get_mkdocs_nav_files(config.get("nav", []))

    # MkDocs defaults to 'docs' directory if not specified
    docs_dir = config.get("docs_dir", "docs")

    for file_path in nav_files:
        # mkdocs file paths are relative to docs_dir
        full_path = os.path.join(docs_dir, file_path)
        assert os.path.exists(full_path), f"File referenced in mkdocs.yml not found: {full_path}"


def test_no_orphaned_docs():
    """Verify that all markdown files in docs/ are referenced in mkdocs.yml."""
    if not os.path.exists("mkdocs.yml"):
        pytest.skip("mkdocs.yml not found")

    with open("mkdocs.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav_files = set(get_mkdocs_nav_files(config.get("nav", [])))
    docs_dir = config.get("docs_dir", "docs")

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                # Get path relative to docs_dir
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
                # Normalize path separators for Windows
                rel_path = rel_path.replace("\\", "/")

                assert rel_path in nav_files, f"Orphaned document found: {rel_path} is not in mkdocs.yml"


def test_wrapper_files_integrity():
    """Verify that wrapper files (using {% include ... %}) point to existing files."""
    if not os.path.exists("mkdocs.yml"):
        pytest.skip("mkdocs.yml not found")

    with open("mkdocs.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    docs_dir = config.get("docs_dir", "docs")

    include_pattern = re.compile(r'{%\s*include\s+"([^"]+)"\s*%}')

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                matches = include_pattern.findall(content)
                for included_file in matches:
                    # included_file is relative to the file containing the include
                    # Resolve it
                    included_full_path = os.path.normpath(os.path.join(os.path.dirname(full_path), included_file))
                    assert os.path.exists(
                        included_full_path
                    ), f"Broken include in {file}: {included_file} (resolves to {included_full_path})"
