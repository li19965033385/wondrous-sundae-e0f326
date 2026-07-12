#!/usr/bin/env python3
"""SVG Image Generator for AI Tools Hub."""
import os, textwrap

CATEGORY_THEMES = {
    "ai-chatbots":    ["#4f46e5", "#7c3aed", "🤖"],
    "ai-image-gen":   ["#0891b2", "#06b6d4", "🎨"],
    "ai-video":       ["#dc2626", "#ef4444", "🎬"],
    "ai-writing":     ["#059669", "#10b981", "✍️"],
    "ai-coding":      ["#2563eb", "#3b82f6", "💻"],
    "ai-productivity":["#d97706", "#f59e0b", "⚡"],
    "ai-audio":       ["#db2777", "#ec4899", "🎵"],
    "ai-business":    ["#7c3aed", "#a855f7", "💼"],
    "ai-news":        ["#1e293b", "#475569", "📰"],
    "tutorials":      ["#0d9488", "#14b8a6", "📚"],
}

def wrap_text(text, max_chars=20):
    words = text.strip().split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= max_chars:
            current += (" " if current else "") + w
        else:
            if current: lines.append(current)
            current = w
    if current: lines.append(current)
    return lines[:4]  # max 4 lines

def generate_article_svg(slug, title, category, output_dir):
    """Generate a beautiful SVG hero image for an article."""
    theme = CATEGORY_THEMES.get(category, ["#4f46e5", "#7c3aed", "🤖"])
    c1, c2, icon = theme
    lines = wrap_text(title, 22)
    line_h = 60
    start_y = 280 - (len(lines) * line_h) // 2

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="overlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(0,0,0,0)"/>
      <stop offset="100%" stop-color="rgba(0,0,0,0.3)"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#overlay)"/>
  <g opacity="0.1">
    <circle cx="200" cy="150" r="300" fill="#fff"/>
    <circle cx="1000" cy="500" r="250" fill="#fff"/>
    <circle cx="600" cy="100" r="200" fill="#fff"/>
  </g>
  <text x="600" y="140" text-anchor="middle" font-size="120" fill="rgba(255,255,255,0.95)">{icon}</text>
'''

    for i, line in enumerate(lines):
        y = start_y + i * line_h
        svg += f'  <text x="600" y="{y}" text-anchor="middle" font-family="system-ui,-apple-system,sans-serif" font-size="42" font-weight="700" fill="#fff">\n'
        # Split by emoji or special chars
        svg += f'    <tspan x="600" dy="0">{line}</tspan>\n'
        svg += f'  </text>\n'

    svg += f'''
  <rect x="420" y="480" width="360" height="44" rx="22" fill="rgba(255,255,255,0.2)"/>
  <text x="600" y="509" text-anchor="middle" font-family="system-ui,sans-serif" font-size="20" font-weight="500" fill="rgba(255,255,255,0.95)">{icon} AI Tools Hub</text>
</svg>'''

    path = os.path.join(output_dir, f"{slug}.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    return f"/img/articles/{slug}.svg"

def generate_all_article_images(articles, output_dir):
    """Generate SVG images for all articles that don't have a custom og_image."""
    img_dir = os.path.join(output_dir, "img", "articles")
    os.makedirs(img_dir, exist_ok=True)
    generated = []
    for a in articles:
        if a.get("og_image") and not a["og_image"].startswith("/img/articles/"):
            continue
        path = generate_article_svg(a["slug"], a.get("title_cn") or a["title"], a.get("category", "tutorials"), img_dir)
        a["og_image"] = path
        generated.append(a["slug"])
    return generated

# Generate OG default image
def generate_default_og(output_dir):
    path = os.path.join(output_dir, "img", "og-default.jpg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4f46e5"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <g opacity="0.15">
    <circle cx="200" cy="200" r="350" fill="#fff"/>
    <circle cx="1000" cy="450" r="300" fill="#fff"/>
  </g>
  <text x="600" y="280" text-anchor="middle" font-family="system-ui,sans-serif" font-size="160" fill="rgba(255,255,255,0.95)">🤖</text>
  <text x="600" y="390" text-anchor="middle" font-family="system-ui,sans-serif" font-size="52" font-weight="700" fill="#fff">AI Tools Hub</text>
  <text x="600" y="440" text-anchor="middle" font-family="system-ui,sans-serif" font-size="24" fill="rgba(255,255,255,0.85)">AI工具资源站 - Your AI Tools Guide</text>
  <rect x="450" y="470" width="300" height="4" rx="2" fill="rgba(255,255,255,0.3)"/>
</svg>'''
    with open(path.replace(".jpg", ".svg"), "w") as f:
        f.write(svg)
    # For simplicity, keep .svg extension
    return "/img/og-default.svg"

if __name__ == "__main__":
    print("SVG Image Generator Module loaded.")
