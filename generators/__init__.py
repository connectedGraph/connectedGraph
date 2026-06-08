# SVG Assets Generators Package for connectedGraph README

import os
import re

def load_icon_svg(name, default_svg, subfolder="", target_size=16, color=None):
    filepath = os.path.join("icon svg", subfolder, f"{name}.svg")
    if not os.path.exists(filepath):
        return default_svg
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Extract viewBox
        viewbox_match = re.search(r'viewBox="([^"]+)"', content)
        if not viewbox_match:
            width_match = re.search(r'width="(\d+)(?:px)?"', content)
            height_match = re.search(r'height="(\d+)(?:px)?"', content)
            if width_match and height_match:
                w = float(width_match.group(1))
                h = float(height_match.group(1))
                viewbox = [0, 0, w, h]
            else:
                viewbox = [0, 0, 24, 24]
        else:
            viewbox = [float(x) for x in viewbox_match.group(1).split()]
        
        vx, vy, vw, vh = viewbox
        scale_x = target_size / vw
        scale_y = target_size / vh
        scale = min(scale_x, scale_y)
        
        # Extract content inside <svg>...</svg>
        inner_match = re.search(r'<svg[^>]*>(.*)</svg>', content, re.DOTALL)
        if not inner_match:
            return default_svg
        inner_content = inner_match.group(1).strip()
        
        # Remove XML declaration and comments/DOCTYPE
        inner_content = re.sub(r'<\?xml[^>]*\?>', '', inner_content)
        inner_content = re.sub(r'<!DOCTYPE[^>]*>', '', inner_content)
        
        # Rename IDs to prevent conflicts
        ids = re.findall(r'id="([^"]+)"', inner_content)
        for id_val in ids:
            new_id = f"{name}_{id_val}"
            inner_content = inner_content.replace(f'id="{id_val}"', f'id="{new_id}"')
            inner_content = inner_content.replace(f'url(#{id_val})', f'url(#{new_id})')
            inner_content = inner_content.replace(f'url(\'#{id_val}\')', f'url(\'#{new_id}\')')
            
        # Extract fill and stroke from the <svg ...> tag
        svg_tag_match = re.search(r'<svg([^>]*)>', content)
        svg_tag_attrs = svg_tag_match.group(1) if svg_tag_match else ""
        
        svg_fill_match = re.search(r'fill="([^"]+)"', svg_tag_attrs)
        svg_stroke_match = re.search(r'stroke="([^"]+)"', svg_tag_attrs)
        
        svg_fill = svg_fill_match.group(1) if svg_fill_match else None
        svg_stroke = svg_stroke_match.group(1) if svg_stroke_match else None
        
        # If color is specified, we make the icon themed/monochrome by stripping explicit black/currentColors
        if color:
            inner_content = re.sub(r'stroke="(?:#000000|#000|currentColor)"', '', inner_content)
            inner_content = re.sub(r'fill="(?:#000000|#000|currentColor)"', '', inner_content)
            g_fill = None
            g_stroke = None
        else:
            g_fill = svg_fill
            g_stroke = svg_stroke
            
        transform_str = f"scale({scale:.5f})"
        if vx != 0 or vy != 0:
            transform_str = f"scale({scale:.5f}) translate({-vx:.5f}, {-vy:.5f})"
            
        g_attrs = f'transform="{transform_str}"'
        if g_fill:
            g_attrs += f' fill="{g_fill}"'
        if g_stroke:
            g_attrs += f' stroke="{g_stroke}"'
            
        return f'<g {g_attrs}>{inner_content}</g>'
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default_svg
