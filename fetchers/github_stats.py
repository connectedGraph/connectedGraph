"""Fetch GitHub profile statistics for the README stats cards.

Everything comes from a single GraphQL endpoint: profile counters, the
contribution calendar, star counts and language sizes. Standard library only,
so the GitHub Actions job needs no pip install.

Token is read from GH_STATS_TOKEN, falling back to GITHUB_TOKEN.

Run standalone to refresh data/github_stats.json:
    python -m fetchers.github_stats
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

LOGIN = "connectedGraph"
API_URL = "https://api.github.com/graphql"
DATA_PATH = os.path.join("data", "github_stats.json")

# The profile owns more than 100 repositories; walk a few pages of the cursor.
MAX_REPO_PAGES = 5
REPOS_PER_PAGE = 100
TOP_LANGUAGES = 6


class FetchError(Exception):
    """Any failure that means we must keep the previously written data."""


PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    publicRepos: repositories(privacy: PUBLIC, ownerAffiliations: OWNER, first: 1) {
      totalCount
    }
    nonForkRepos: repositories(privacy: PUBLIC, isFork: false, ownerAffiliations: OWNER, first: 1) {
      totalCount
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

REPOS_QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(
      privacy: PUBLIC
      isFork: false
      ownerAffiliations: OWNER
      first: %d
      after: $cursor
    ) {
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first: %d, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
  }
}
""" % (REPOS_PER_PAGE, TOP_LANGUAGES)


def _graphql(query, variables, token):
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": "bearer %s" % token,
            "Content-Type": "application/json",
            "User-Agent": "connectedGraph-profile-stats",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise FetchError("HTTP %s from GitHub API: %s" % (exc.code, detail))
    except urllib.error.URLError as exc:
        raise FetchError("Could not reach GitHub API: %s" % exc.reason)

    # GraphQL reports problems in a 200 response, so check the body too.
    if body.get("errors"):
        messages = "; ".join(e.get("message", "?") for e in body["errors"])
        raise FetchError("GraphQL errors: %s" % messages)
    if not body.get("data"):
        raise FetchError("GraphQL response carried no data")

    return body["data"]


def _flatten_calendar(user):
    calendar = (user.get("contributionsCollection") or {}).get("contributionCalendar") or {}
    days = []
    for week in calendar.get("weeks") or []:
        for day in week.get("contributionDays") or []:
            days.append({"date": day["date"], "count": day["contributionCount"]})

    if not days:
        raise FetchError("Contribution calendar came back empty")

    days.sort(key=lambda d: d["date"])
    return days, calendar.get("totalContributions", 0)


def _streaks(days):
    """Return (current, longest) run of consecutive days with a contribution.

    The last day in the calendar is today. A zero there does not break the
    streak yet, because the day is still in progress.
    """
    counts = [day["count"] for day in days]

    longest = 0
    run = 0
    for count in counts:
        run = run + 1 if count > 0 else 0
        longest = max(longest, run)

    index = len(counts) - 1
    if index >= 0 and counts[index] == 0:
        index -= 1

    current = 0
    while index >= 0 and counts[index] > 0:
        current += 1
        index -= 1

    return current, longest


def _collect_repos(token):
    """Walk every public non-fork repository and total up stars and languages."""
    nodes = []
    cursor = None
    pages = 0

    while pages < MAX_REPO_PAGES:
        data = _graphql(REPOS_QUERY, {"login": LOGIN, "cursor": cursor}, token)
        connection = (data.get("user") or {}).get("repositories") or {}
        nodes.extend(connection.get("nodes") or [])
        pages += 1

        page_info = connection.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    if pages >= MAX_REPO_PAGES and cursor:
        print(
            "Warning: stopped after %d pages, some repositories were not counted"
            % MAX_REPO_PAGES,
            file=sys.stderr,
        )

    return nodes


def _aggregate_languages(repo_nodes):
    totals = {}
    for repo in repo_nodes:
        edges = (repo.get("languages") or {}).get("edges") or []
        for edge in edges:
            node = edge.get("node") or {}
            name = node.get("name")
            if not name:
                continue
            entry = totals.setdefault(
                name, {"size": 0, "color": node.get("color") or "#8b949e"}
            )
            entry["size"] += edge.get("size") or 0

    grand_total = sum(entry["size"] for entry in totals.values())
    if grand_total <= 0:
        return []

    ranked = sorted(totals.items(), key=lambda kv: kv[1]["size"], reverse=True)
    return [
        {
            "name": name,
            "color": entry["color"],
            "pct": round(entry["size"] * 100.0 / grand_total, 1),
        }
        for name, entry in ranked[:TOP_LANGUAGES]
    ]


def collect(token):
    """Fetch everything and return the JSON-ready stats dictionary."""
    data = _graphql(PROFILE_QUERY, {"login": LOGIN}, token)
    user = data.get("user")
    if not user:
        raise FetchError("User %r not found" % LOGIN)

    days, total_contributions = _flatten_calendar(user)
    current_streak, longest_streak = _streaks(days)

    repo_nodes = _collect_repos(token)
    stars = sum(repo.get("stargazerCount") or 0 for repo in repo_nodes)

    return {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": {
            "year": total_contributions,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        },
        "profile": {
            "followers": (user.get("followers") or {}).get("totalCount", 0),
            "public_repos": (user.get("publicRepos") or {}).get("totalCount", 0),
            "non_fork_repos": (user.get("nonForkRepos") or {}).get("totalCount", 0),
            "stars": stars,
        },
        "languages": _aggregate_languages(repo_nodes),
        "days": days,
    }


def write(stats, path=DATA_PATH):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(stats, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def load(path=DATA_PATH):
    """Read the cached stats, or None when there is nothing usable on disk."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            stats = json.load(handle)
    except (OSError, ValueError) as exc:
        print("Could not read %s: %s" % (path, exc), file=sys.stderr)
        return None
    return stats if stats.get("days") else None


def token_from_env():
    return os.environ.get("GH_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")


def main():
    token = token_from_env()
    if not token:
        print(
            "No token found. Set GH_STATS_TOKEN (or GITHUB_TOKEN) first.",
            file=sys.stderr,
        )
        return 1

    try:
        stats = collect(token)
    except FetchError as exc:
        print("Fetch failed, keeping the previous data: %s" % exc, file=sys.stderr)
        return 1

    write(stats)
    totals = stats["totals"]
    print(
        "Wrote %s  |  year=%s current=%s longest=%s stars=%s repos=%s"
        % (
            DATA_PATH,
            totals["year"],
            totals["current_streak"],
            totals["longest_streak"],
            stats["profile"]["stars"],
            stats["profile"]["public_repos"],
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
