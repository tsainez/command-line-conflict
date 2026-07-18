"""Fetch open pull requests and their changed files from the GitHub REST API.

Network access is confined to :func:`fetch_open_pull_requests`. The parsing of
API payloads into :class:`~pr_merge_optimizer.models.PullRequest` objects lives in
pure helpers so it can be unit tested without hitting the network.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Sequence

from .models import PullRequest

_API_ROOT = "https://api.github.com"


def pull_request_from_payload(pr_payload: Dict[str, Any], files: Sequence[str]) -> PullRequest:
    """Build a :class:`PullRequest` from a ``/pulls`` item and its file list."""

    head = pr_payload.get("head") or {}
    base = pr_payload.get("base") or {}
    return PullRequest(
        number=int(pr_payload["number"]),
        files=set(files),
        title=str(pr_payload.get("title", "")),
        branch=str(head.get("ref", "") or ""),
        base_ref=str(base.get("ref", "main") or "main"),
    )


def files_from_payload(files_payload: Sequence[Dict[str, Any]]) -> List[str]:
    """Extract the list of changed file paths from a ``/pulls/{n}/files`` payload."""

    return [str(entry["filename"]) for entry in files_payload if "filename" in entry]


class GitHubClient:
    """Minimal GitHub REST client using only the Python standard library.

    Args:
        repo: Repository in ``owner/name`` form.
        token: Personal access token; falls back to the ``GITHUB_TOKEN`` env var.
        api_root: API base URL (overridable for GitHub Enterprise).
    """

    def __init__(self, repo: str, token: Optional[str] = None, api_root: str = _API_ROOT) -> None:
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_root = api_root.rstrip("/")

    def _get(self, path: str) -> Any:
        url = f"{self.api_root}{path}"
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(request) as response:  # noqa: S310 - fixed https api root
            return json.loads(response.read().decode("utf-8"))

    def _get_changed_files(self, number: int) -> List[str]:
        collected: List[str] = []
        page = 1
        while True:
            payload = self._get(f"/repos/{self.repo}/pulls/{number}/files?per_page=100&page={page}")
            if not payload:
                break
            collected.extend(files_from_payload(payload))
            if len(payload) < 100:
                break
            page += 1
        return collected

    def fetch_open_pull_requests(self, base: Optional[str] = None) -> List[PullRequest]:
        """Return all open pull requests (optionally filtered by ``base`` branch)."""

        pull_requests: List[PullRequest] = []
        page = 1
        while True:
            path = f"/repos/{self.repo}/pulls?state=open&per_page=100&page={page}"
            if base:
                path += f"&base={base}"
            payload = self._get(path)
            if not payload:
                break
            for item in payload:
                files = self._get_changed_files(int(item["number"]))
                pull_requests.append(pull_request_from_payload(item, files))
            if len(payload) < 100:
                break
            page += 1
        return pull_requests


def fetch_open_pull_requests(repo: str, token: Optional[str] = None, base: Optional[str] = None) -> List[PullRequest]:
    """Convenience wrapper: fetch open pull requests for ``repo`` from GitHub."""

    return GitHubClient(repo, token=token).fetch_open_pull_requests(base=base)
