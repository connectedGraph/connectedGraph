import os, sys, json, tempfile, shutil, base64
from flask import Flask, render_template, request, jsonify, send_file

# ── make parent generators importable ──────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from generators.typewriter  import generate_typewriter
from generators.avatar      import generate_avatar
from generators.thinking    import generate_thinking_header
from generators.badges      import generate_social_badges
from generators.tech_stack  import generate_tech_stack
from generators.projects    import generate_projects
from generators.headers     import generate_header
from generators.api_docs    import generate_api_docs
from generators.footer      import generate_footer
from generators.ask_me_badge import generate_ask_me_badge

app = Flask(__name__)

# ── helpers ────────────────────────────────────────────────────────────────────

PREVIEW_DIR = os.path.join(os.path.dirname(__file__), "_preview")
os.makedirs(PREVIEW_DIR, exist_ok=True)

HEADER_ICONS = {
    "tech_stack":  '<path d="M16 18l6-6-6-6M8 6L2 12l6 6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "projects":    '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M12 11l2 2-2 2" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>',
    "public_apis": '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "stats":       '<path d="M18 20V10M12 20V4M6 20v-6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "roadmap":     '<path d="M9 6h11M9 12h11M9 18h11M5 6v.01M5 12v.01M5 18v.01" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
    "ask_me":      '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>',
}

def _svg_to_data_uri(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/svg+xml;base64,{encoded}"

def _build_component(component, theme, params, out_dir):
    """Generate a single component into out_dir using the supplied params."""
    os.chdir(ROOT)  # generators resolve relative paths from ROOT

    if component == "typewriter":
        generate_typewriter(output_dir=out_dir, theme=theme, **params)
    elif component == "avatar":
        generate_avatar(output_dir=out_dir, theme=theme, **params)
    elif component == "thinking":
        generate_thinking_header(output_dir=out_dir, theme=theme, **params)
    elif component == "badges":
        generate_social_badges(output_dir=out_dir, theme=theme)
    elif component == "tech_stack":
        generate_tech_stack(output_dir=out_dir, theme=theme)
    elif component == "projects":
        generate_projects(output_dir=out_dir, theme=theme)
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


COMPONENT_FILES = {
    "typewriter":    "typewriter.svg",
    "avatar":        "avatar_animated.svg",
    "thinking":      "thinking_header.svg",
    "badges":        None,  # multi-file
    "tech_stack":    "tech_stack.svg",
    "projects":      "projects.svg",
    "api_docs":      "api_docs.svg",
    "footer":        "footer.svg",
    "ask_me_badge":  "ask_me_badge.svg",
    "header_tech_stack":  "header_tech_stack.svg",
    "header_projects":    "header_projects.svg",
    "header_public_apis": "header_public_apis.svg",
    "header_stats":       "header_stats.svg",
    "header_roadmap":     "header_roadmap.svg",
    "header_ask_me":      "header_ask_me.svg",
}

# ── routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/preview", methods=["POST"])
def preview():
    data             = request.get_json(force=True)
    component        = data.get("component", "typewriter")
    theme            = data.get("theme", "dark")
    params           = data.get("params", {})
    write_to_project = data.get("write_to_project", False)

    preview_theme_dir = os.path.join(PREVIEW_DIR, theme)
    os.makedirs(preview_theme_dir, exist_ok=True)

    try:
        _build_component(component, theme, params, preview_theme_dir)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Optionally also write to the real project dark/light folders
    if write_to_project:
        project_out = os.path.join(ROOT, theme)
        os.makedirs(project_out, exist_ok=True)
        try:
            _build_component(component, theme, params, project_out)
        except Exception:
            pass  # preview still works even if write fails

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
    params = data.get("params", {})

    results = []
    os.chdir(ROOT)

    for theme in ["dark", "light"]:
        out_dir = os.path.join(ROOT, theme)
        os.makedirs(out_dir, exist_ok=True)

        # typewriter / avatar / thinking accept custom params
        generate_typewriter(output_dir=out_dir, theme=theme, **params.get("typewriter", {}))
        generate_avatar(output_dir=out_dir, theme=theme, **params.get("avatar", {}))
        generate_thinking_header(output_dir=out_dir, theme=theme, **params.get("thinking", {}))

        # rest use defaults
        generate_social_badges(output_dir=out_dir, theme=theme)
        generate_tech_stack(output_dir=out_dir, theme=theme)
        generate_projects(output_dir=out_dir, theme=theme)
        generate_api_docs(output_dir=out_dir, theme=theme)
        generate_footer(output_dir=out_dir, theme=theme)
        generate_ask_me_badge(output_dir=out_dir, theme=theme)

        for key, icon in HEADER_ICONS.items():
            label = key.replace("_", " ").title()
            generate_header(label, f"header_{key}.svg", icon, output_dir=out_dir, theme=theme)

        results.append(f"✅ {theme} — done")

    return jsonify({"results": results, "success": True})


@app.route("/api/defaults")
def defaults():
    return jsonify({
        "typewriter": {
            "animation_duration": 12,
        },
        "avatar": {
            "ring_color_1": "#7aa2f7",
            "ring_color_2": "#bb9af3",
            "ring_color_3": "#7dcfff",
            "pulse_duration": 4,
        },
        "thinking": {
            "sweep_color": "#22d3ee",
            "spin_duration": 2.4,
        },
    })


if __name__ == "__main__":
    print("\n  README Builder running at  http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
