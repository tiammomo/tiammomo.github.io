#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]


def request_json(url: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "tiammomo-portfolio-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API failed with {exc.code}: {url}\n{detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API request failed: {url}\n{exc}") from exc


def fetch_public_repos(owner: str, token: str | None) -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        query = urlencode({"per_page": 100, "page": page, "type": "owner", "sort": "full_name"})
        data = request_json(f"https://api.github.com/users/{owner}/repos?{query}", token)
        if not isinstance(data, list):
            raise RuntimeError("GitHub repos response was not a list")
        repos.extend(repo for repo in data if isinstance(repo, dict) and not repo.get("private"))
        if len(data) < 100:
            break
        page += 1
    return repos


def fetch_authored_public_pr_count(owner: str, token: str | None) -> int:
    query = urlencode({"q": f"author:{owner} type:pr is:public", "per_page": 1})
    data = request_json(f"https://api.github.com/search/issues?{query}", token)
    if not isinstance(data, dict) or "total_count" not in data:
        raise RuntimeError("GitHub PR search response did not include total_count")
    return int(data["total_count"])


def read_project_count(path: Path) -> int:
    projects = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(projects, list):
        raise RuntimeError(f"{path} must contain a JSON list")
    return sum(
        1
        for project in projects
        if isinstance(project, dict) and project.get("featured", True) is not False
    )


def build_stats(owner: str, projects_path: Path, token: str | None) -> dict:
    user = request_json(f"https://api.github.com/users/{owner}", token)
    if not isinstance(user, dict):
        raise RuntimeError("GitHub user response was not an object")

    repos = fetch_public_repos(owner, token)
    return {
        "owner": owner,
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "sources": {
            "githubUser": f"https://api.github.com/users/{owner}",
            "githubRepos": f"https://api.github.com/users/{owner}/repos",
            "githubPullRequests": f"https://api.github.com/search/issues?q=author:{owner}+type:pr+is:public",
            "projects": str(projects_path.relative_to(ROOT)),
        },
        "stats": {
            "publicRepos": int(user.get("public_repos", len(repos))),
            "selectedProjects": read_project_count(projects_path),
            "totalStars": sum(int(repo.get("stargazers_count") or 0) for repo in repos),
            "authoredPublicPullRequests": fetch_authored_public_pr_count(owner, token),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Update portfolio homepage profile stats.")
    parser.add_argument("--owner", default="tiammomo", help="GitHub owner login")
    parser.add_argument("--projects", type=Path, default=ROOT / "data" / "projects.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "profile-stats.json")
    args = parser.parse_args()

    projects_path = args.projects if args.projects.is_absolute() else ROOT / args.projects
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    token = os.environ.get("GITHUB_TOKEN")

    payload = build_stats(args.owner, projects_path, token)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    stats = payload["stats"]
    print(
        "updated "
        f"{output_path.relative_to(ROOT)}: "
        f"{stats['publicRepos']} repos, "
        f"{stats['selectedProjects']} selected projects, "
        f"{stats['totalStars']} stars, "
        f"{stats['authoredPublicPullRequests']} PRs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
