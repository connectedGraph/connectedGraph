from generators import load_icon_svg, clear_collected_defs, get_collected_defs

def generate_social_badges():
    # Globe icon (stroke-based)
    globe_path = '<circle cx="8" cy="8" r="6.5"/><path d="M1.5 8h13M8 1.5c1.5 2 1.5 11 0 13M8 1.5c-1.5 2-1.5 11 0 13"/>'
    # Pen/Edit icon (stroke-based)
    pen_path = '<path d="M11.5 1.5a1.5 1.5 0 1 1 2 2L4.5 12.5 1.5 13.5l1-3zM10 3l3 3"/>'
    # GitHub icon (fill-based)
    github_path = '<path d="M8 .2C3.6.2 0 3.8 0 8.2c0 3.5 2.3 6.5 5.5 7.6.4.1.5-.2.5-.4v-1.4c-2.2.5-2.7-1.1-2.7-1.1-.4-.9-.9-1.2-.9-1.2-.7-.5.1-.5.1-.5.8.1 1.2.8 1.2.8.7 1.2 1.9.9 2.3.7.1-.5.3-.9.5-1.1-1.8-.2-3.6-.9-3.6-4 0-.9.3-1.6.8-2.2-.1-.2-.4-1 .1-2.1 0 0 .7-.2 2.2.8a7.8 7.8 0 0 1 4.1 0c1.5-1 2.2-.8 2.2-.8.5 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.2 0 3.1-1.9 3.8-3.7 4 .3.3.5.8.5 1.6V15c0 .2.1.5.6.4C13.7 14.7 16 11.7 16 8.2 16 3.8 12.4.2 8 .2z" fill="{color}" stroke="none"/>'
    # QQ icon (stroke-based, scaled 192x192)
    qq_path = '<g transform="scale(0.08333)" stroke-width="15"><path d="M153.933 114.718c-2.953-9.509-6.349-17.5-11.573-30.58C143.172 49.786 128.922 22 96.101 22c-33.189 0-47.125 28.34-46.24 62.139-5.241 13.097-8.62 21.033-11.573 30.579-6.276 20.256-4.246 28.636-2.695 28.821 3.323.407 12.94-15.243 12.94-15.243 0 9.064 4.651 20.886 14.73 29.413-4.873 1.499-15.82 5.532-13.217 9.953 2.105 3.57 36.217 2.275 46.056 1.165 9.838 1.11 43.95 2.405 46.055-1.165 2.602-4.403-8.362-8.454-13.217-9.953 10.078-8.546 14.73-20.367 14.73-29.413 0 0 9.617 15.65 12.94 15.243 1.569-.203 3.6-8.583-2.677-28.821Z"/></g>'
    # Zhihu icon (fill-based, scaled 24x24)
    zhihu_path = '<g transform="scale(0.6667)"><path d="M5.721 0C2.251 0 0 2.25 0 5.719V18.28C0 21.751 2.252 24 5.721 24h12.56C21.751 24 24 21.75 24 18.281V5.72C24 2.249 21.75 0 18.281 0zm1.964 4.078c-.271.73-.5 1.434-.68 2.11h4.587c.545-.006.445 1.168.445 1.171H9.384a58.104 58.104 0 01-.112 3.797h2.712c.388.023.393 1.251.393 1.266H9.183a9.223 9.223 0 01-.408 2.102l.757-.604c.452.456 1.512 1.712 1.906 2.177.473.681.063 2.081.063 2.081l-2.794-3.382c-.653 2.518-1.845 3.607-1.845 3.607-.523.468-1.58.82-2.64.516 2.218-1.73 3.44-3.917 3.667-6.497H4.491c0-.015.197-1.243.806-1.266h2.71c.024-.32.086-3.254.086-3.797H6.598c-.136.406-.158.447-.268.753-.594 1.095-1.603 1.122-1.907 1.155.906-1.821 1.416-3.6 1.591-4.064.425-1.124 1.671-1.125 1.671-1.125zM13.078 6h6.377v11.33h-2.573l-2.184 1.373-.401-1.373h-1.219zm1.313 1.219v8.86h.623l.263.937 1.455-.938h1.456v-8.86z" fill="{color}"/></g>'
    # Codex icon (fill-based, scaled 24x24)
    codex_path = '<g transform="scale(0.6667)"><path clip-rule="evenodd" fill-rule="evenodd" d="M8.086.457a6.105 6.105 0 013.046-.415c1.333.153 2.521.72 3.564 1.7a.117.117 0 00.107.029c1.408-.346 2.762-.224 4.061.366l.063.03.154.076c1.357.703 2.33 1.77 2.918 3.198.278.679.418 1.388.421 2.126a5.655 5.655 0 01-.18 1.631.167.167 0 00.04.155 5.982 5.982 0 011.578 2.891c.385 1.901-.01 3.615-1.183 5.14l-.182.22a6.063 6.063 0 01-2.934 1.851.162.162 0 00-.108.102c-.255.736-.511 1.364-.987 1.992-1.199 1.582-2.962 2.462-4.948 2.451-1.583-.008-2.986-.587-4.21-1.736a.145.145 0 00-.14-.032c-.518.167-1.04.191-1.604.185a5.924 5.924 0 01-2.595-.622 6.058 6.058 0 01-2.146-1.781c-.203-.269-.404-.522-.551-.821a7.74 7.74 0 01-.495-1.283 6.11 6.11 0 01-.017-3.064.166.166 0 00.008-.074.115.115 0 00-.037-.064 5.958 5.958 0 01-1.38-2.202 5.196 5.196 0 01-.333-1.589 6.915 6.915 0 01.188-2.132c.45-1.484 1.309-2.648 2.577-3.493.282-.188.55-.334.802-.438.286-.12.573-.22.861-.304a.129.129 0 00.087-.087A6.016 6.016 0 015.635 2.31C6.315 1.464 7.132.846 8.086.457zm-.804 7.85a.848.848 0 00-1.473.842l1.694 2.965-1.688 2.848a.849.849 0 001.46.864l1.94-3.272a.849.849 0 00.007-.854l-1.94-3.393zm5.446 6.24a.849.849 0 000 1.695h4.848a.849.849 0 000-1.696h-4.848z" fill="{color}"/></g>'

    badges = [
        ("badge_website.svg", 108, globe_path, "#7dcfff", "6767.chat", False),
        ("badge_blog.svg", 72, pen_path, "#bb9af3", "Blog", False),
        ("badge_github.svg", 88, github_path, "#a9b1d6", "GitHub", True),
        ("badge_qq.svg", 65, qq_path, "#7dcfff", "QQ", False),
        ("badge_zhihu.svg", 80, zhihu_path, "#7aa2f7", "Zhihu", True),
        ("badge_codex.svg", 88, codex_path, "#9ece6a", "Codex", True)
    ]

    label_widths = {
        "6767.chat": 62,
        "Blog": 26,
        "GitHub": 42,
        "QQ": 18,
        "Zhihu": 33,
        "Codex": 35
    }

    for filename, width, icon_svg, color, label, is_fill in badges:
        clear_collected_defs()
        local_name = label.lower()
        if local_name == "6767.chat":
            local_name = "website"
            
        import os
        has_local = os.path.exists(os.path.join("icon svg", f"{local_name}.svg"))
        
        if has_local:
            loaded_svg = load_icon_svg(local_name, icon_svg, color=color)
            if is_fill:
                icon_content = f'<g fill="{color}">{loaded_svg}</g>'
            else:
                icon_content = f'<g stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">{loaded_svg}</g>'
        else:
            if is_fill:
                icon_content = icon_svg.replace("{color}", color)
            else:
                icon_content = f'<g stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">{icon_svg}</g>'
        
        # Calculate horizontal centering for icon + text group
        text_w = label_widths.get(label, len(label) * 7)
        content_w = 16 + 6 + text_w # icon (16) + gap (6) + text width
        start_x = (width - content_w) / 2
        text_x = start_x + 16 + 6
        
        badge_defs = get_collected_defs()
        defs_block = f"\n  <defs>\n{badge_defs}\n  </defs>" if badge_defs else ""
        
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" fill="none">{defs_block}
  <rect x="0.5" y="0.5" width="{width - 1}" height="27" rx="14" fill="#16161e" stroke="#24283b" stroke-width="1"/>
  <g transform="translate({start_x:.1f}, 6)">
    {icon_content}
  </g>
  <text x="{text_x:.1f}" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#c0caf5">{label}</text>
</svg>"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated {filename}")
