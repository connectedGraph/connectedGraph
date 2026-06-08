import os

def generate_projects(output_dir=".", theme="dark"):
    if theme == "light":
        card_bg = "#f6f8fa"
        card_stroke = "#d1d5db"
        sep_stroke = "#d1d5db"
        shadow_opacity = "0.12"
        folder_stroke = "#0366d6"
        name_color = "#0366d6"
        desc_color = "#444d56"
        
        status_colors = {
            "Live": {"bg": "#dcffe4", "fg": "#1a7f37"},
            "Build": {"bg": "#fff3cd", "fg": "#b06000"},
            "Lab": {"bg": "#f5ecff", "fg": "#6f42c1"}
        }
    else:
        card_bg = "#1a1b26"
        card_stroke = "#24283b"
        sep_stroke = "#24283b"
        shadow_opacity = "0.5"
        folder_stroke = "#7aa2f7"
        name_color = "#7dcfff"
        desc_color = "#a9b1d6"
        
        status_colors = {
            "Live": {"bg": "#132f22", "fg": "#22c55e"},
            "Build": {"bg": "#352311", "fg": "#e0af68"},
            "Lab": {"bg": "#24183d", "fg": "#bb9af3"}
        }

    projects = [
        {
            "name": "Zhihu Immersive Reader",
            "url": "https://6767.chat/zhihu-immersive-reader/",
            "status": "Live",
            "desc": "Immersive reading script for Zhihu, featuring ad-blocking, AI summaries, and Markdown exports."
        },
        {
            "name": "Sanguosha Voice & Lines",
            "url": "https://6767.chat/sgs",
            "status": "Live",
            "desc": "Interactive quote library for Sanguosha game, featuring dialogue search, audio playback, and admin panel."
        },
        {
            "name": "AIED DuoGrow SaaS",
            "url": "https://github.com/connectedGraph/AIED-DuoGrow-SaaS",
            "status": "Build",
            "desc": "Lightweight English learning web app with parent-child feedback loops and AI grading."
        },
        {
            "name": "BrightlyPk",
            "url": "https://github.com/connectedGraph/BrightlyPk",
            "status": "Lab",
            "desc": "Node.js + WebSocket powered real-time multiplayer trivia competition platform."
        },
        {
            "name": "Deepseek Unofficial API",
            "url": "https://github.com/connectedGraph/Deepseek-unofficial-API",
            "status": "Lab",
            "desc": "Node.js library wrapper for Deepseek Expert Mode."
        }
    ]

    rows_html = ""
    for idx, p in enumerate(projects):
        row_y = 52 + idx * 48
        
        # XML escape special characters for safety
        name_escaped = p['name'].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        desc_escaped = p['desc'].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Draw separator line between rows (except after the last one)
        sep_line = ""
        if idx < len(projects) - 1:
            sep_y = row_y + 24
            sep_line = f'<line x1="35" y1="{sep_y}" x2="715" y2="{sep_y}" stroke="{sep_stroke}" stroke-width="1"/>'
            
        bg_col = status_colors[p['status']]['bg']
        fg_col = status_colors[p['status']]['fg']
            
        rows_html += f"""    <!-- Row {idx}: {name_escaped} -->
    <g transform="translate(0, 0)">
      <!-- Folder Icon -->
      <g transform="translate(35, {row_y - 12})" stroke="{folder_stroke}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M2 4a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4z"/>
      </g>
      
      <!-- Project Name -->
      <text x="62" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="13.5" font-weight="bold" fill="{name_color}">{name_escaped}</text>
      
      <!-- Status Badge -->
      <rect x="245" y="{row_y - 11}" width="48" height="17" rx="8.5" fill="{bg_col}"/>
      <text x="269" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="9.5" font-weight="800" fill="{fg_col}" text-anchor="middle">{p['status']}</text>
      
      <!-- Description -->
      <foreignObject x="305" y="{row_y - 12}" width="410" height="32">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif; font-size: 11.5px; color: {desc_color}; line-height: 1.35; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin: 0; padding: 0;">
          {desc_escaped}
        </div>
      </foreignObject>
    </g>
    {sep_line}
"""

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="310" viewBox="0 0 750 310" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="720" height="280" rx="12" fill="{card_bg}" stroke="{card_stroke}" stroke-width="1.5" filter="url(#shadow)"/>

{rows_html}</svg>
"""

    filepath = os.path.join(output_dir, "projects.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
