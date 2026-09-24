"""SVG cards for the GitHub Stats section.

Two cards, both 750 wide, matching the house style used by tech_stack.py and
projects.py: 15px inset, rx=12, url(#shadow), text in the system sans stack,
dark = Tokyo Night / light = GitHub Primer.

Data shape comes from fetchers.github_stats; DEFAULT_STATS keeps the generator
working offline with placeholder numbers.
"""

import os
from datetime import date

from generators import clear_collected_defs, get_collected_defs

DEFAULT_STATS = {
    "updated_at": "",
    "totals": {"year": 0, "current_streak": 0, "longest_streak": 0},
    "profile": {"followers": 0, "public_repos": 0, "non_fork_repos": 0, "stars": 0},
    "languages": [],
    "days": [],
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

FONT = "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"

SVG_W = 750
CARD_X = 15
CARD_W = SVG_W - 30

PAD_L = 45
PAD_R = SVG_W - 45
CONTENT_W = PAD_R - PAD_L


def _esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def _text_w(s, size):
    """Rough advance width, same approximation style as badges.py."""
    return len(str(s)) * size * 0.6


def _num(value):
    try:
        return "{:,}".format(int(value))
    except (TypeError, ValueError):
        return "0"


def _streak(value):
    """A count with its unit set smaller, e.g. 22 days."""
    count = int(value or 0)
    unit = "day" if count == 1 else "days"
    return f'{_num(count)}<tspan font-size="15" font-weight="700"> {unit}</tspan>'


def _palette(theme):
    if theme == "light":
        return {
            "card_bg": "#f6f8fa", "card_stroke": "#d1d5db", "shadow_opacity": "0.12",
            "track_fill": "#ffffff", "sep_stroke": "#d1d5db",
            "text_color": "#24292e", "muted_color": "#6a737d", "title_color": "#0366d6",
            "blue": "#0366d6", "cyan": "#005cc5", "purple": "#6f42c1",
            "green": "#22863a", "orange": "#b06000",
            "grad_start": "#0366d6", "grad_end": "#6f42c1",
            "area_opacity": "0.22",
        }
    return {
        "card_bg": "#1a1b26", "card_stroke": "#24283b", "shadow_opacity": "0.5",
        "track_fill": "#16161e", "sep_stroke": "#24283b",
        "text_color": "#c0caf5", "muted_color": "#565f89", "title_color": "#7aa2f7",
        "blue": "#7aa2f7", "cyan": "#7dcfff", "purple": "#bb9af3",
        "green": "#9ece6a", "orange": "#e0af68",
        "grad_start": "#7aa2f7", "grad_end": "#bb9af3",
        "area_opacity": "0.35",
    }


def _svg_open(height, palette, extra_defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{height}" viewBox="0 0 {SVG_W} {height}" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="{palette['shadow_opacity']}"/>
    </filter>
    <linearGradient id="header-grad" x1="0" y1="0" x2="200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{palette['grad_start']}"/>
      <stop offset="100%" stop-color="{palette['grad_end']}"/>
    </linearGradient>
{extra_defs}    {get_collected_defs()}
  </defs>

  <rect x="{CARD_X}" y="15" width="{CARD_W}" height="{height - 30}" rx="12" fill="{palette['card_bg']}" stroke="{palette['card_stroke']}" stroke-width="1.5" filter="url(#shadow)"/>
"""


def generate_stats_card(output_dir=".", theme="dark", **kwargs):
    """Counters card: contributions, streaks, stars, repositories, languages."""
    clear_collected_defs()

    stats = kwargs.get("stats") or DEFAULT_STATS
    totals = stats.get("totals") or {}
    profile = stats.get("profile") or {}
    languages = stats.get("languages") or []

    p = _palette(theme)

    # --- layout -----------------------------------------------------------
    TILE_TOP = 38
    TILE_W = CONTENT_W / 4.0
    NUM_Y = TILE_TOP + 30
    LABEL_Y = TILE_TOP + 52
    ROW1_BOTTOM = TILE_TOP + 60
    ROW2_Y = ROW1_BOTTOM + 34
    LANG_LABEL_Y = ROW2_Y + 38
    BAR_Y = LANG_LABEL_Y + 8
    BAR_H = 10
    LEGEND_Y = BAR_Y + BAR_H + 20
    SVG_H = LEGEND_Y + 32

    tiles = [
        ("Contributions", _num(totals.get("year")), p["blue"]),
        ("Current Streak", _streak(totals.get("current_streak")), p["green"]),
        ("Longest Streak", _streak(totals.get("longest_streak")), p["orange"]),
        ("Stars Earned", _num(profile.get("stars")), p["purple"]),
    ]

    parts = []
    for i, (label, value, color) in enumerate(tiles):
        cx = PAD_L + TILE_W * i + TILE_W / 2.0
        if i:
            parts.append(
                f'  <line x1="{PAD_L + TILE_W * i:.1f}" y1="{TILE_TOP + 8}" '
                f'x2="{PAD_L + TILE_W * i:.1f}" y2="{ROW1_BOTTOM - 8}" '
                f'stroke="{p["sep_stroke"]}" stroke-width="1"/>'
            )
        parts.append(
            f'  <text x="{cx:.1f}" y="{NUM_Y}" font-family="{FONT}" font-size="30" '
            f'font-weight="800" fill="{color}" text-anchor="middle">{value}</text>'
        )
        parts.append(
            f'  <text x="{cx:.1f}" y="{LABEL_Y}" font-family="{FONT}" font-size="10.5" '
            f'font-weight="700" fill="{p["muted_color"]}" letter-spacing="0.8" '
            f'text-anchor="middle">{_esc(label.upper())}</text>'
        )

    # --- row 2: repositories and followers --------------------------------
    row2 = []
    cursor_x = PAD_L
    for value, word, color in (
        (profile.get("public_repos"), "Repositories", p["cyan"]),
        (profile.get("followers"), "Followers", p["blue"]),
    ):
        number = _num(value)
        row2.append(
            f'<text x="{cursor_x:.1f}" y="{ROW2_Y}" font-family="{FONT}" font-size="17" '
            f'font-weight="800" fill="{color}">{number}</text>'
        )
        word_x = cursor_x + _text_w(number, 17) + 7
        row2.append(
            f'<text x="{word_x:.1f}" y="{ROW2_Y}" font-family="{FONT}" font-size="11.5" '
            f'font-weight="600" fill="{p["muted_color"]}">{_esc(word)}</text>'
        )
        cursor_x = word_x + _text_w(word, 11.5) + 34

    updated = (stats.get("updated_at") or "")[:10]
    if updated:
        row2.append(
            f'<text x="{PAD_R}" y="{ROW2_Y}" font-family="{FONT}" font-size="10.5" '
            f'fill="{p["muted_color"]}" text-anchor="end">updated {_esc(updated)}</text>'
        )

    # --- row 3: language distribution -------------------------------------
    lang_parts = [
        f'  <text x="{PAD_L}" y="{LANG_LABEL_Y}" font-family="{FONT}" font-size="10.5" '
        f'font-weight="700" fill="{p["muted_color"]}" letter-spacing="0.8">LANGUAGES</text>'
    ]

    top = [l for l in languages if l.get("pct")][:5]
    if top:
        share = [l["pct"] for l in top]
        rest = round(100.0 - sum(share), 1)
        if rest >= 0.5:
            top = top + [{"name": "Other", "color": None, "pct": rest}]
            share = share + [rest]
        total_share = sum(share) or 100.0

        lang_parts.append(
            f'  <clipPath id="lang-clip"><rect x="{PAD_L}" y="{BAR_Y}" '
            f'width="{CONTENT_W}" height="{BAR_H}" rx="{BAR_H / 2:.1f}"/></clipPath>'
        )
        lang_parts.append(
            f'  <rect x="{PAD_L}" y="{BAR_Y}" width="{CONTENT_W}" height="{BAR_H}" '
            f'rx="{BAR_H / 2:.1f}" fill="{p["track_fill"]}" stroke="{p["card_stroke"]}" stroke-width="1"/>'
        )

        segments = []
        offset = float(PAD_L)
        for entry in top:
            width = CONTENT_W * entry["pct"] / total_share
            color = entry.get("color") or p["muted_color"]
            segments.append(
                f'    <rect x="{offset:.2f}" y="{BAR_Y}" width="{width:.2f}" height="{BAR_H}" '
                f'fill="{color}"/>'
            )
            offset += width
        lang_parts.append(
            f'  <g clip-path="url(#lang-clip)" stroke="{p["card_bg"]}" stroke-width="2">\n'
            + "\n".join(segments)
            + "\n  </g>"
        )

        slot_w = CONTENT_W / len(top)
        for i, entry in enumerate(top):
            dot_x = PAD_L + slot_w * i + 4
            color = entry.get("color") or p["muted_color"]
            lang_parts.append(
                f'  <circle cx="{dot_x:.1f}" cy="{LEGEND_Y - 3.5:.1f}" r="4" fill="{color}"/>'
            )
            lang_parts.append(
                f'  <text x="{dot_x + 11:.1f}" y="{LEGEND_Y}" font-family="{FONT}" '
                f'font-size="10.5" fill="{p["text_color"]}">'
                f'{_esc(entry["name"])} <tspan fill="{p["muted_color"]}">{entry["pct"]}%</tspan></text>'
            )

    body = "\n".join(parts + ["  " + t for t in row2] + lang_parts)

    content = _svg_open(SVG_H, p) + "\n" + body + "\n</svg>\n"

    filepath = os.path.join(output_dir, "github_stats.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")


def generate_activity_graph(output_dir=".", theme="dark", **kwargs):
    """Area chart of daily contributions over the last twelve months."""
    clear_collected_defs()

    stats = kwargs.get("stats") or DEFAULT_STATS
    days = [d for d in (stats.get("days") or []) if d.get("date")]
    if not days:
        # Nothing to draw; emit an empty card so the README never breaks.
        p = _palette(theme)
        content = _svg_open(120, p) + "\n</svg>\n"
        filepath = os.path.join(output_dir, "activity_graph.svg")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filepath} ({theme}, no data)")
        return

    p = _palette(theme)

    # --- layout -----------------------------------------------------------
    TITLE_Y = 46
    PLOT_TOP = 70
    PLOT_BOTTOM = 196
    PLOT_H = PLOT_BOTTOM - PLOT_TOP
    MONTH_Y = PLOT_BOTTOM + 20
    FOOTER_Y = MONTH_Y + 20
    SVG_H = FOOTER_Y + 26

    counts = [d.get("count", 0) or 0 for d in days]
    peak = max(counts) or 1

    step = CONTENT_W / float(len(days) - 1) if len(days) > 1 else 0.0

    def x_at(index):
        return PAD_L + index * step

    def y_at(count):
        return PLOT_BOTTOM - (count / float(peak)) * PLOT_H

    points = [(x_at(i), y_at(c)) for i, c in enumerate(counts)]
    line_d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    area_d = (line_d
              + f" L {points[-1][0]:.2f},{PLOT_BOTTOM} L {points[0][0]:.2f},{PLOT_BOTTOM} Z")

    extra_defs = (
        f'    <linearGradient id="area-fill" x1="0" y1="{PLOT_TOP}" x2="0" y2="{PLOT_BOTTOM}" '
        f'gradientUnits="userSpaceOnUse">\n'
        f'      <stop offset="0%" stop-color="{p["grad_start"]}" stop-opacity="{p["area_opacity"]}"/>\n'
        f'      <stop offset="100%" stop-color="{p["grad_start"]}" stop-opacity="0"/>\n'
        f'    </linearGradient>\n'
        f'    <linearGradient id="line-grad" x1="{PAD_L}" y1="0" x2="{PAD_R}" y2="0" '
        f'gradientUnits="userSpaceOnUse">\n'
        f'      <stop offset="0%" stop-color="{p["grad_start"]}"/>\n'
        f'      <stop offset="100%" stop-color="{p["grad_end"]}"/>\n'
        f'    </linearGradient>\n'
    )

    total = _num(sum(counts))
    parts = [
        f'  <text x="{PAD_L}" y="{TITLE_Y}" font-family="{FONT}" font-size="12" '
        f'font-weight="800" fill="{p["title_color"]}" letter-spacing="1">CONTRIBUTION ACTIVITY</text>',
        f'  <rect x="{PAD_L}" y="{TITLE_Y + 7}" width="45" height="2" rx="1" fill="url(#header-grad)"/>',
        f'  <text x="{PAD_R}" y="{TITLE_Y}" font-family="{FONT}" font-size="11.5" '
        f'font-weight="600" fill="{p["muted_color"]}" text-anchor="end">{total} in the last year</text>',
        f'  <line x1="{PAD_L}" y1="{PLOT_BOTTOM}" x2="{PAD_R}" y2="{PLOT_BOTTOM}" '
        f'stroke="{p["sep_stroke"]}" stroke-width="1"/>',
    ]

    # Month ticks: a faint gridline plus a label at each month boundary.
    seen = set()
    for index, day in enumerate(days):
        try:
            current = date.fromisoformat(day["date"])
        except ValueError:
            continue
        key = (current.year, current.month)
        if key in seen:
            continue
        seen.add(key)
        if index == 0:
            continue
        x = x_at(index)
        parts.append(
            f'  <line x1="{x:.2f}" y1="{PLOT_TOP}" x2="{x:.2f}" y2="{PLOT_BOTTOM}" '
            f'stroke="{p["sep_stroke"]}" stroke-width="1" opacity="0.5"/>'
        )
        parts.append(
            f'  <text x="{x:.2f}" y="{MONTH_Y}" font-family="{FONT}" font-size="10" '
            f'fill="{p["muted_color"]}" text-anchor="middle">{MONTHS[current.month - 1]}</text>'
        )

    parts.append(f'  <path d="{area_d}" fill="url(#area-fill)"/>')
    parts.append(
        f'  <path d="{line_d}" fill="none" stroke="url(#line-grad)" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )

    updated = (stats.get("updated_at") or "")[:10]
    if updated:
        parts.append(
            f'  <text x="{PAD_R}" y="{FOOTER_Y}" font-family="{FONT}" font-size="10.5" '
            f'fill="{p["muted_color"]}" text-anchor="end">updated {_esc(updated)}</text>'
        )

    content = _svg_open(SVG_H, p, extra_defs) + "\n" + "\n".join(parts) + "\n</svg>\n"

    filepath = os.path.join(output_dir, "activity_graph.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
