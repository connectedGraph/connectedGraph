import os, sys, json, base64
from flask import Flask, render_template, request, jsonify, send_from_directory

# ── make parent generators importable ──────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from generators.typewriter   import generate_typewriter
from generators.avatar       import generate_avatar
from generators.thinking     import generate_thinking_header
from generators.badges       import generate_social_badges
from generators.tech_stack   import generate_tech_stack
from generators.projects     import generate_projects
from generators.headers      import generate_header
from generators.api_docs     import generate_api_docs
from generators.footer       import generate_footer
from generators.ask_me_badge import generate_ask_me_badge

app = Flask(__name__)

PREVIEW_DIR  = os.path.join(os.path.dirname(__file__), "_preview")
MANIFEST     = os.path.join(os.path.dirname(__file__), "icon_manifest.json")
ICON_ROOT    = os.path.join(ROOT, "icon svg")
os.makedirs(PREVIEW_DIR, exist_ok=True)

HEADER_ICONS = {
    "tech_stack":  '<path d="M16 18l6-6-6-6M8 6L2 12l6 6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "projects":    '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M12 11l2 2-2 2" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>',
    "public_apis": '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "stats":       '<path d="M18 20V10M12 20V4M6 20v-6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "roadmap":     '<path d="M9 6h11M9 12h11M9 18h11M5 6v.01M5 12v.01M5 18v.01" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "ask_me":      '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
}

COMPONENT_FILES = {
    "typewriter":         "typewriter.svg",
    "avatar":             "avatar_animated.svg",
    "thinking":           "thinking_header.svg",
    "tech_stack":         "tech_stack.svg",
    "projects":           "projects.svg",
    "api_docs":           "api_docs.svg",
    "footer":             "footer.svg",
    "ask_me_badge":       "ask_me_badge.svg",
    "header_tech_stack":  "header_tech_stack.svg",
    "header_projects":    "header_projects.svg",
    "header_public_apis": "header_public_apis.svg",
    "header_stats":       "header_stats.svg",
    "header_roadmap":     "header_roadmap.svg",
    "header_ask_me":      "header_ask_me.svg",
}

BADGE_FILES = [
    "badge_website.svg", "badge_blog.svg", "badge_github.svg",
    "badge_qq.svg",      "badge_zhihu.svg", "badge_codex.svg",
]

# ── helpers ────────────────────────────────────────────────────────────────────

def _svg_to_data_uri(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/svg+xml;base64,{encoded}"

def _build_component(component, theme, params, out_dir):
    """Generate a single component into out_dir using the supplied params."""
    os.chdir(ROOT)  # generators resolve relative paths from ROOT

    if component == "typewriter":
        generate_typewriter(output_dir=out_dir, theme=theme, **(params or {}))
    elif component == "avatar":
        generate_avatar(output_dir=out_dir, theme=theme, **(params or {}))
    elif component == "thinking":
        generate_thinking_header(output_dir=out_dir, theme=theme, **(params or {}))
    elif component == "badges":
        generate_social_badges(output_dir=out_dir, theme=theme)
    elif component == "tech_stack":
        generate_tech_stack(output_dir=out_dir, theme=theme, **(params or {}))
    elif component == "projects":
        generate_projects(output_dir=out_dir, theme=theme, **(params or {}))
    elif component == "api_docs":
        generate_api_docs(output_dir=out_dir, theme=theme)
    elif component == "footer":
        generate_footer(output_dir=out_dir, theme=theme)
    elif component == "ask_me_badge":
        generate_ask_me_badge(output_dir=out_dir, theme=theme)
    elif component.startswith("header_"):
        key = component[len("header_"):]
        label = key.replace("_", " ").title()
        icon_path = HEADER_ICONS.get(key, "")
        generate_header(label, f"{component}.svg", icon_path, output_dir=out_dir, theme=theme)
    else:
        raise ValueError(f"unknown component: {component}")


# ── routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/icons")
def icons_manifest():
    """Return a merged manifest: simple-icons download + the legacy bundled icons.
    The picker uses this for the Tech Stack editor."""
    manifest = []
    if os.path.exists(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    # Merge legacy bundled icons that aren't in the simple-icons set
    known_slugs = {m["slug"] for m in manifest}
    legacy = [
        ("nextjs",       "Next.js",      "code",     "#000000"),
        ("react",        "React",        "code",     "#61DAFB"),
        ("javascript",   "JavaScript",   "code",     "#F7DF1E"),
        ("html5",        "HTML5",        "code",     "#E34F26"),
        ("css3",         "CSS3",         "code",     "#1572B6"),
        ("nodejs",       "Node.js",      "code",     "#339933"),
        ("python",       "Python",       "code",     "#3776AB"),
        ("express",      "Express",      "code",     "#a9b1d6"),
        ("pgsql",        "PostgreSQL",   "code",     "#316192"),
        ("claude-api",   "Claude API",   "devtools", "#D97757"),
        ("claudecode",   "Claude Code",  "devtools", "#D97757"),
        ("codex",        "Codex",        "devtools", "#9ECE6A"),
        ("deepseek-api", "Deepseek API", "devtools", "#4D6BFE"),
        ("qq",           "QQ",           "contact",  "#7DCFFF"),
        ("zhihu",        "Zhihu",        "contact",  "#0084FF"),
    ]
    for slug, label, sub, color in legacy:
        if slug in known_slugs:
            continue
        path = os.path.join(ICON_ROOT, sub, f"{slug}.svg")
        if os.path.exists(path):
            manifest.append({"slug": slug, "label": label, "subfolder": sub, "color": color})
    manifest.sort(key=lambda m: (m["subfolder"], m["label"].lower()))
    return jsonify(manifest)


@app.route("/static/icon/<path:relpath>")
def serve_icon(relpath):
    """Serve files from the project's `icon svg/` directory under /static/icon/."""
    safe = os.path.normpath(relpath).replace("\\", "/")
    if safe.startswith("..") or os.path.isabs(safe):
        return ("forbidden", 403)
    return send_from_directory(ICON_ROOT, safe)


@app.route("/api/preview", methods=["POST"])
def preview():
    data             = request.get_json(force=True)
    component        = data.get("component", "typewriter")
    theme            = data.get("theme", "dark")
    params           = data.get("params", {}) or {}
    write_to_project = data.get("write_to_project", False)

    preview_theme_dir = os.path.join(PREVIEW_DIR, theme)
    os.makedirs(preview_theme_dir, exist_ok=True)

    try:
        _build_component(component, theme, params, preview_theme_dir)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if write_to_project:
        project_out = os.path.join(ROOT, theme)
        os.makedirs(project_out, exist_ok=True)
        try:
            _build_component(component, theme, params, project_out)
        except Exception as e:
            print(f"[warn] write_to_project failed: {e}")

    filename = COMPONENT_FILES.get(component)
    if not filename:
        return jsonify({"error": "multi-file component — use build-all"}), 400

    svg_path = os.path.join(preview_theme_dir, filename)
    if not os.path.exists(svg_path):
        return jsonify({"error": f"SVG not found: {svg_path}"}), 404

    return jsonify({"svg": _svg_to_data_uri(svg_path)})


@app.route("/api/build-all", methods=["POST"])
def build_all():
    data   = request.get_json(force=True)
    params = data.get("params", {}) or {}

    results = []
    os.chdir(ROOT)

    for theme in ["dark", "light"]:
        out_dir = os.path.join(ROOT, theme)
        os.makedirs(out_dir, exist_ok=True)
        preview_theme_dir = os.path.join(PREVIEW_DIR, theme)
        os.makedirs(preview_theme_dir, exist_ok=True)

        # Single components — write to BOTH the project root and preview cache.
        for target in (out_dir, preview_theme_dir):
            generate_typewriter(output_dir=target, theme=theme, **params.get("typewriter", {}))
            generate_avatar(output_dir=target, theme=theme, **params.get("avatar", {}))
            generate_thinking_header(output_dir=target, theme=theme, **params.get("thinking", {}))

            generate_social_badges(output_dir=target, theme=theme)
            generate_tech_stack(output_dir=target, theme=theme, **params.get("tech_stack", {}))
            generate_projects(output_dir=target, theme=theme, **params.get("projects", {}))
            generate_api_docs(output_dir=target, theme=theme)
            generate_footer(output_dir=target, theme=theme)
            generate_ask_me_badge(output_dir=target, theme=theme)

            for key, icon in HEADER_ICONS.items():
                label = key.replace("_", " ").title()
                generate_header(label, f"header_{key}.svg", icon, output_dir=target, theme=theme)

        results.append(f"OK {theme} done")

    return jsonify({"results": results, "success": True})


@app.route("/api/all-previews")
def all_previews():
    """Return data URIs for every cached component+theme. Used by Overview."""
    out = {}
    for theme in ("dark", "light"):
        theme_dir = os.path.join(PREVIEW_DIR, theme)
        if not os.path.isdir(theme_dir):
            continue
        out[theme] = {}
        for key, fname in COMPONENT_FILES.items():
            p = os.path.join(theme_dir, fname)
            if os.path.exists(p):
                out[theme][key] = _svg_to_data_uri(p)
        out[theme]["badges"] = []
        for bf in BADGE_FILES:
            p = os.path.join(theme_dir, bf)
            if os.path.exists(p):
                out[theme]["badges"].append({
                    "name": bf.replace("badge_", "").replace(".svg", ""),
                    "svg":  _svg_to_data_uri(p),
                })
    return jsonify(out)


@app.route("/api/defaults")
def defaults():
    return jsonify({
        "typewriter": {"animation_duration": 12},
        "avatar":     {"ring_color_1": "#7aa2f7", "ring_color_2": "#bb9af3", "ring_color_3": "#7dcfff", "pulse_duration": 4},
        "thinking":   {"sweep_color": "#22d3ee", "spin_duration": 2.4},
    })


if __name__ == "__main__":
    print("\n  README Builder running at  http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
