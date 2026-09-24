"""Refresh the GitHub stats data and rebuild both stats cards.

    python update_stats.py              # fetch, then render dark + light
    python update_stats.py --offline    # render from the cached JSON only

When the fetch fails this exits non-zero without touching data/github_stats.json,
so the committed cards keep showing the last good numbers.
"""

import os
import sys

from fetchers import github_stats
from generators.github_stats import generate_activity_graph, generate_stats_card

THEMES = ["dark", "light"]


def render(stats):
    for theme in THEMES:
        os.makedirs(theme, exist_ok=True)
        generate_activity_graph(output_dir=theme, theme=theme, stats=stats)
        generate_stats_card(output_dir=theme, theme=theme, stats=stats)


def main(argv):
    offline = "--offline" in argv

    if offline:
        stats = github_stats.load()
        if not stats:
            print("No cached stats available to render.", file=sys.stderr)
            return 1
        print("Offline: rendering from the cached JSON.")
    else:
        token = github_stats.token_from_env()
        if not token:
            print(
                "No token found. Set GH_STATS_TOKEN (or GITHUB_TOKEN) first.",
                file=sys.stderr,
            )
            return 1
        try:
            stats = github_stats.collect(token)
        except github_stats.FetchError as exc:
            print("Fetch failed, keeping the previous data: %s" % exc, file=sys.stderr)
            return 1
        github_stats.write(stats)
        print("Wrote %s" % github_stats.DATA_PATH)

    render(stats)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
