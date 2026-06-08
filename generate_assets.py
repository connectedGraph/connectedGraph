import os
from generators.typewriter import generate_typewriter
from generators.headers import generate_header
from generators.badges import generate_social_badges
from generators.tech_stack import generate_tech_stack
from generators.projects import generate_projects
from generators.thinking import generate_thinking_header
from generators.avatar import generate_avatar

def main():
    # Icons for section headers (Tokyo Night theme gradients)
    tech_path = '<path d="M16 18l6-6-6-6M8 6L2 12l6 6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    projects_path = '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M12 11l2 2-2 2" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>'
    apis_path = '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
    stats_path = '<path d="M18 20V10M12 20V4M6 20v-6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
    roadmap_path = '<path d="M9 6h11M9 12h11M9 18h11M5 6v.01M5 12v.01M5 18v.01" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
    ask_path = '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>'

    # Run each SVG asset generator
    generate_typewriter()
    generate_header("Tech Stack", "header_tech_stack.svg", tech_path)
    generate_header("Projects", "header_projects.svg", projects_path)
    generate_header("Public APIs", "header_public_apis.svg", apis_path)
    generate_header("GitHub Stats", "header_stats.svg", stats_path)
    generate_header("Roadmap", "header_roadmap.svg", roadmap_path)
    generate_header("Ask Me", "header_ask_me.svg", ask_path)
    generate_social_badges()
    generate_tech_stack()
    generate_projects()
    generate_thinking_header()
    generate_avatar()

if __name__ == "__main__":
    main()
