import os

DEFAULT_PROJECTS = [
    {"name": "RoleFit · 职途星", "url": "https://github.com/connectedGraph/RoleFit",
     "status": "Build", "desc": "面向中文招聘数据的可解释智能人岗匹配系统 / Explainable AI job matching for Chinese recruitment data."},
    {"name": "知乎沉浸阅读", "url": "https://6767.chat/zhihu-immersive-reader/",
     "status": "Live", "desc": "知乎纯净阅读、AI 总结与 Markdown 导出 / Immersive Zhihu reading with AI summaries and exports."},
    {"name": "trae2api-web", "url": "https://github.com/connectedGraph/trae2api-web",
     "status": "Live", "desc": "TRAE SOLO 的 OpenAI 兼容代理与中文管理面板 / OpenAI-compatible proxy with a web console."},
    {"name": "三国杀台词鉴赏馆", "url": "https://6767.chat/sgs",
     "status": "Live", "desc": "台词检索、古文解析与语音播放 / Searchable Sanguosha quotes, annotations, and audio."},
    {"name": "DeepSeek 非官方 API", "url": "https://github.com/connectedGraph/Deepseek-unofficial-API",
     "status": "Lab", "desc": "支持专家模式的非官方接口实验 / Unofficial API experiments for DeepSeek Expert Mode."},
]

def _esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def generate_projects(output_dir=".", theme="dark", **kwargs):
    if theme == "light":
        card_bg     = "#f6f8fa"; card_stroke = "#d1d5db"
        sep_stroke  = "#d1d5db"; shadow_opacity = "0.12"
        folder_stroke = "#0366d6"; name_color = "#0366d6"; desc_color = "#444d56"
        status_colors = {
            "Live":  {"bg": "#dcffe4", "fg": "#1a7f37"},
            "Build": {"bg": "#fff3cd", "fg": "#b06000"},
            "Lab":   {"bg": "#f5ecff", "fg": "#6f42c1"},
            "Wip":   {"bg": "#fff3cd", "fg": "#b06000"},
            "Idea":  {"bg": "#eef2ff", "fg": "#3730a3"},
        }
    else:
        card_bg     = "#1a1b26"; card_stroke = "#24283b"
        sep_stroke  = "#24283b"; shadow_opacity = "0.5"
        folder_stroke = "#7aa2f7"; name_color = "#7dcfff"; desc_color = "#a9b1d6"
        status_colors = {
            "Live":  {"bg": "#132f22", "fg": "#22c55e"},
            "Build": {"bg": "#352311", "fg": "#e0af68"},
            "Lab":   {"bg": "#24183d", "fg": "#bb9af3"},
            "Wip":   {"bg": "#352311", "fg": "#e0af68"},
            "Idea":  {"bg": "#1a1f3a", "fg": "#7aa2f7"},
        }

    projects = kwargs.get("projects") or DEFAULT_PROJECTS
    projects = [p for p in projects if p.get("name")]
    if not projects:
        projects = DEFAULT_PROJECTS

    rows_html = ""
    for idx, p in enumerate(projects):
        row_y = 52 + idx * 48
        name_escaped   = _esc(p.get("name", ""))
        desc_escaped   = _esc(p.get("desc", ""))
        status         = p.get("status", "Live")
        sc             = status_colors.get(status) or status_colors.get("Live")

        sep_line = ""
        if idx < len(projects) - 1:
            sep_y = row_y + 24
            sep_line = f'<line x1="35" y1="{sep_y}" x2="715" y2="{sep_y}" stroke="{sep_stroke}" stroke-width="1"/>'

        rows_html += f"""    <g>
      <g transform="translate(35, {row_y - 12})" stroke="{folder_stroke}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M2 4a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4z"/>
      </g>
      <text x="62" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="13.5" font-weight="bold" fill="{name_color}">{name_escaped}</text>
      <rect x="245" y="{row_y - 11}" width="48" height="17" rx="8.5" fill="{sc['bg']}"/>
      <text x="269" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="9.5" font-weight="800" fill="{sc['fg']}" text-anchor="middle">{_esc(status)}</text>
      <foreignObject x="305" y="{row_y - 12}" width="410" height="32">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif; font-size: 11.5px; color: {desc_color}; line-height: 1.35; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin: 0; padding: 0;">{desc_escaped}</div>
      </foreignObject>
    </g>
    {sep_line}
"""

    body_h = max(48 * len(projects), 48)
    svg_h  = 30 + body_h + 10
    card_h = svg_h - 30

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="{svg_h}" viewBox="0 0 750 {svg_h}" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
  </defs>

  <rect x="15" y="15" width="720" height="{card_h}" rx="12" fill="{card_bg}" stroke="{card_stroke}" stroke-width="1.5" filter="url(#shadow)"/>

{rows_html}</svg>
"""

    filepath = os.path.join(output_dir, "projects.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
