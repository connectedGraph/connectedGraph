import os

def generate_avatar(output_dir=".", theme="dark"):
    import base64
    try:
        with open("avatar.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_href = f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Warning: Could not read avatar.jpg: {e}")
        image_href = "./avatar.jpg" # fallback

    if theme == "light":
        ring1 = "#0366d6"
        ring2 = "#6f42c1"
        ring3 = "#005cc5"
        border = "#0366d6"
        border_hover = "#6f42c1"
    else:
        ring1 = "#7aa2f7"
        ring2 = "#bb9af3"
        ring3 = "#7dcfff"
        border = "#7aa2f7"
        border_hover = "#bb9af3"

    # We will embed the local avatar.jpg by wrapping it inside an SVG pattern mask
    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 160 160" fill="none">
  <defs>
    <!-- Shadow filters for realistic glass depth -->
    <filter id="avatar-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
    
    <!-- Pattern to mask the local avatar.jpg image inside the circular path -->
    <pattern id="avatar-pattern" x="0" y="0" width="1" height="1" patternUnits="objectBoundingBox">
      <image href="{image_href}" x="0" y="0" width="120" height="120" preserveAspectRatio="xMidYMid slice"/>
    </pattern>
  </defs>
 
  <style>
    /* Pulsing Bubble/Ring animations */
    .bubble-ring-1 {{
      stroke: {ring1};
      stroke-width: 1.5px;
      opacity: 0.85;
      transform-origin: 80px 80px;
      animation: pulse-ring 4s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
    }}
    
    .bubble-ring-2 {{
      stroke: {ring2};
      stroke-width: 1.2px;
      opacity: 0.6;
      transform-origin: 80px 80px;
      animation: pulse-ring 4s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
      animation-delay: 1.3s;
    }}
    
    .bubble-ring-3 {{
      stroke: {ring3};
      stroke-width: 1px;
      opacity: 0.35;
      transform-origin: 80px 80px;
      animation: pulse-ring 4s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
      animation-delay: 2.6s;
    }}
    
    .avatar-border {{
      stroke: {border};
      stroke-width: 3.5px;
      transition: stroke 0.3s ease;
    }}
    
    .avatar-container:hover .avatar-border {{
      stroke: {border_hover};
    }}

    @keyframes pulse-ring {{
      0% {{
        transform: scale(0.74);
        opacity: 0.85;
      }}
      80%, 100% {{
        transform: scale(0.97);
        opacity: 0;
      }}
    }}
  </style>

  <!-- Animated Bubble Rings -->
  <circle cx="80" cy="80" r="76" class="bubble-ring-3"/>
  <circle cx="80" cy="80" r="76" class="bubble-ring-2"/>
  <circle cx="80" cy="80" r="76" class="bubble-ring-1"/>

  <!-- Avatar Group -->
  <g class="avatar-container" filter="url(#avatar-shadow)">
    <!-- Main Image circle with 120px diameter (60px radius) -->
    <circle cx="80" cy="80" r="60" fill="url(#avatar-pattern)" />
    <!-- Overlay Border -->
    <circle cx="80" cy="80" r="60" fill="none" class="avatar-border" />
  </g>
</svg>
"""
    filepath = os.path.join(output_dir, "avatar_animated.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
