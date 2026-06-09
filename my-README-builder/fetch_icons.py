"""Download a curated icon library from simple-icons CDN into icon svg/ subfolders.
   Run once: python fetch_icons.py"""
import os, json, urllib.request, concurrent.futures, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_ROOT = os.path.join(ROOT, "icon svg")

# (slug, label, subfolder) — slug is simple-icons slug
ICONS = [
    # ── Languages / code ────────────────────────────────────────────
    ("typescript",  "TypeScript",  "code"),
    ("go",          "Go",          "code"),
    ("rust",        "Rust",        "code"),
    ("openjdk",     "Java",        "code"),
    ("kotlin",      "Kotlin",      "code"),
    ("swift",       "Swift",       "code"),
    ("ruby",        "Ruby",        "code"),
    ("php",         "PHP",         "code"),
    ("cplusplus",   "C++",         "code"),
    ("c",           "C",           "code"),
    ("sharp",       "C#",          "code"),
    ("dart",        "Dart",        "code"),
    ("lua",         "Lua",         "code"),
    ("r",           "R",           "code"),
    ("scala",       "Scala",       "code"),
    ("perl",        "Perl",        "code"),
    ("elixir",      "Elixir",      "code"),
    ("haskell",     "Haskell",     "code"),

    # ── Frontend frameworks ────────────────────────────────────────
    ("vuedotjs",    "Vue.js",      "code"),
    ("angular",     "Angular",     "code"),
    ("svelte",      "Svelte",      "code"),
    ("solid",       "SolidJS",     "code"),
    ("astro",       "Astro",       "code"),
    ("nuxt",        "Nuxt",        "code"),
    ("gatsby",      "Gatsby",      "code"),
    ("remix",       "Remix",       "code"),
    ("tailwindcss", "Tailwind",    "code"),
    ("sass",        "Sass",        "code"),
    ("vite",        "Vite",        "code"),
    ("webpack",     "Webpack",     "code"),

    # ── Backend frameworks ─────────────────────────────────────────
    ("django",      "Django",      "code"),
    ("flask",       "Flask",       "code"),
    ("fastapi",     "FastAPI",     "code"),
    ("spring",      "Spring",      "code"),
    ("dotnet",      ".NET",        "code"),
    ("laravel",     "Laravel",     "code"),
    ("nestjs",      "NestJS",      "code"),
    ("rubyonrails", "Rails",       "code"),

    # ── Databases ──────────────────────────────────────────────────
    ("mongodb",     "MongoDB",     "db"),
    ("mysql",       "MySQL",       "db"),
    ("redis",       "Redis",       "db"),
    ("sqlite",      "SQLite",      "db"),
    ("postgresql",  "PostgreSQL",  "db"),
    ("mariadb",     "MariaDB",     "db"),
    ("supabase",    "Supabase",    "db"),
    ("firebase",    "Firebase",    "db"),
    ("elasticsearch", "Elastic",   "db"),

    # ── Cloud / DevOps ─────────────────────────────────────────────
    ("docker",      "Docker",      "cloud"),
    ("kubernetes",  "Kubernetes",  "cloud"),
    ("amazonwebservices", "AWS",   "cloud"),
    ("googlecloud", "Google Cloud","cloud"),
    ("microsoftazure", "Azure",    "cloud"),
    ("vercel",      "Vercel",      "cloud"),
    ("netlify",     "Netlify",     "cloud"),
    ("cloudflare",  "Cloudflare",  "cloud"),
    ("heroku",      "Heroku",      "cloud"),
    ("digitalocean","DigitalOcean","cloud"),
    ("github",      "GitHub",      "cloud"),
    ("gitlab",      "GitLab",      "cloud"),
    ("git",         "Git",         "cloud"),
    ("terraform",   "Terraform",   "cloud"),
    ("nginx",       "Nginx",       "cloud"),
    ("linux",       "Linux",       "cloud"),

    # ── AI / ML ────────────────────────────────────────────────────
    ("tensorflow",  "TensorFlow",  "devtools"),
    ("pytorch",     "PyTorch",     "devtools"),
    ("openai",      "OpenAI",      "devtools"),
    ("huggingface", "HuggingFace", "devtools"),
    ("anthropic",   "Anthropic",   "devtools"),
    ("googlegemini","Gemini",      "devtools"),
    ("ollama",      "Ollama",      "devtools"),

    # ── Editors / IDE ──────────────────────────────────────────────
    ("vscodium",       "VS Code",   "devtools"),
    ("neovim",         "Neovim",    "devtools"),
    ("intellijidea",   "IntelliJ",  "devtools"),
    ("pycharm",        "PyCharm",   "devtools"),
    ("jetbrains",      "JetBrains", "devtools"),
    ("vim",            "Vim",       "devtools"),

    # ── Contact / social ───────────────────────────────────────────
    ("gmail",       "Email",       "contact"),
    ("telegram",    "Telegram",    "contact"),
    ("discord",     "Discord",     "contact"),
    ("slack",       "Slack",       "contact"),
    ("x",           "X (Twitter)", "contact"),
    ("linkedin",    "LinkedIn",    "contact"),
    ("instagram",   "Instagram",   "contact"),
    ("youtube",     "YouTube",     "contact"),
    ("twitch",      "Twitch",      "contact"),
    ("sinaweibo",   "Weibo",       "contact"),
    ("wechat",      "WeChat",      "contact"),
    ("bilibili",    "Bilibili",    "contact"),
    ("mastodon",    "Mastodon",    "contact"),
    ("medium",      "Medium",      "contact"),
    ("devdotto",    "Dev.to",      "contact"),
    ("stackoverflow","StackOverflow","contact"),
    ("substack",    "Substack",    "contact"),
    ("dribbble",    "Dribbble",    "contact"),
]

CDN_TPL = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
COLOR_TPL = "https://cdn.jsdelivr.net/npm/simple-icons@latest/_data/simple-icons.json"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_color_map():
    """Pull the simple-icons metadata once to learn brand hex colors."""
    try:
        data = json.loads(fetch(COLOR_TPL).decode("utf-8"))
        # Newer simple-icons exposes data as a list of {title, slug, hex}
        if isinstance(data, list):
            entries = data
        else:
            entries = data.get("icons", [])
        result = {}
        for e in entries:
            slug = e.get("slug") or re.sub(r"[^a-z0-9]", "", e.get("title", "").lower())
            hex_ = e.get("hex")
            if slug and hex_:
                result[slug] = "#" + hex_
        return result
    except Exception as e:
        print(f"  [warn] color map fetch failed: {e}", file=sys.stderr)
        return {}


def download(slug, subfolder, color):
    target_dir = os.path.join(ICON_ROOT, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, f"{slug}.svg")
    if os.path.exists(target):
        return slug, "skip"
    try:
        body = fetch(CDN_TPL.format(slug=slug)).decode("utf-8")
        # Inject brand colour as fill on the <svg> root so it renders coloured.
        if color and "fill=" not in body[:body.find(">") + 1]:
            body = body.replace("<svg ", f'<svg fill="{color}" ', 1)
        with open(target, "w", encoding="utf-8") as f:
            f.write(body)
        return slug, "ok"
    except Exception as e:
        return slug, f"fail: {e}"


def main():
    print(f"Fetching simple-icons brand colors...")
    colors = get_color_map()
    print(f"  -> {len(colors)} brand colors loaded")

    print(f"\nDownloading {len(ICONS)} icons...")
    manifest = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(download, slug, sub, colors.get(slug)): (slug, label, sub)
                   for (slug, label, sub) in ICONS}
        for fut in concurrent.futures.as_completed(futures):
            slug, label, sub = futures[fut]
            _, status = fut.result()
            color = colors.get(slug, "#888888")
            manifest.append({"slug": slug, "label": label, "subfolder": sub, "color": color})
            mark = "OK" if status in ("ok", "skip") else "X "
            print(f"  [{mark}] {slug:24s} -> {sub}/{slug}.svg  ({status})")

    manifest.sort(key=lambda m: (m["subfolder"], m["label"].lower()))
    out = os.path.join(os.path.dirname(__file__), "icon_manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nManifest written: {out}")


if __name__ == "__main__":
    main()
