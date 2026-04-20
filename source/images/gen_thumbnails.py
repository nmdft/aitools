#!/usr/bin/env python3
"""Generate article thumbnail cards for AITools review site."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = '/Users/zhua/aitools/source/images/thumbnails'
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 800, 450

# Tool data: name, primary_color, accent_color, rating, tagline
tools = {
    'cursor': {
        'name': 'Cursor',
        'color1': (0, 0, 0),       # black
        'color2': (30, 30, 30),
        'accent': (255, 180, 0),    # gold accent
        'rating': '8.5/10',
        'tag': 'AI Code Editor',
    },
    'windsurf': {
        'name': 'Windsurf',
        'color1': (10, 25, 60),     # deep blue
        'color2': (20, 50, 100),
        'accent': (0, 200, 255),    # cyan accent
        'rating': '8.0/10',
        'tag': 'AI Code Editor',
    },
    'gamma': {
        'name': 'Gamma',
        'color1': (40, 0, 60),      # purple
        'color2': (80, 20, 120),
        'accent': (200, 100, 255),  # light purple
        'rating': '8.0/10',
        'tag': 'AI Presentations',
    },
    'n8n': {
        'name': 'n8n',
        'color1': (50, 10, 10),     # dark red
        'color2': (100, 30, 30),
        'accent': (255, 90, 90),    # n8n red/pink
        'rating': '8.5/10',
        'tag': 'Workflow Automation',
    },
    'bolt-new': {
        'name': 'Bolt.new',
        'color1': (0, 0, 0),
        'color2': (20, 20, 20),
        'accent': (140, 80, 255),   # purple
        'rating': '7.5/10',
        'tag': 'AI Web Dev',
    },
    'jasper': {
        'name': 'Jasper',
        'color1': (10, 10, 40),     # dark indigo
        'color2': (30, 20, 80),
        'accent': (255, 100, 50),   # Jasper orange-red
        'rating': '7.0/10',
        'tag': 'AI Content Writer',
    },
    'cursor-vs-windsurf': {
        'name': 'Cursor vs Windsurf',
        'color1': (0, 15, 40),
        'color2': (10, 35, 70),
        'accent': (255, 200, 0),    # gold
        'rating': None,
        'tag': 'HEAD-TO-HEAD COMPARISON',
    },
    'ai-tools-list': {
        'name': 'Top 10 AI Coding Tools',
        'color1': (0, 30, 30),      # dark teal
        'color2': (0, 60, 60),
        'accent': (0, 220, 180),    # teal accent
        'rating': None,
        'tag': '2026 ROUNDUP',
    },
    'ai-marketing-tools': {
        'name': 'AI Marketing Tools',
        'color1': (40, 0, 20),      # dark magenta
        'color2': (80, 10, 40),
        'accent': (255, 80, 150),   # pink
        'rating': None,
        'tag': 'FOR SOLOPRENEURS',
    },
    'ai-automation-tools': {
        'name': 'AI Automation Tools',
        'color1': (0, 20, 10),      # dark green
        'color2': (0, 50, 30),
        'accent': (50, 220, 100),   # green
        'rating': None,
        'tag': '2026 GUIDE',
    },
}

try:
    font_name = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
    font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    font_rating = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    font_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
except:
    font_name = ImageFont.load_default()
    font_tag = ImageFont.load_default()
    font_rating = ImageFont.load_default()
    font_big = ImageFont.load_default()

for slug, data in tools.items():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    
    c1, c2 = data['color1'], data['color2']
    for y in range(H):
        t = y / H
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Decorative accent bar at top
    draw.rectangle([0, 0, W, 4], fill=data['accent'])
    
    # Large decorative letter (first char) as background element
    big_letter = data['name'][0].upper()
    bb = draw.textbbox((0, 0), big_letter, font=font_big)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    # Draw faded letter in bottom-right
    letter_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(letter_layer)
    ld.text((W - bw - 30, H - bh - 20), big_letter, fill=(*data['accent'], 25), font=font_big)
    img = Image.alpha_composite(img.convert('RGBA'), letter_layer).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Tag line (top-left)
    draw.text((40, 35), data['tag'], fill=data['accent'], font=font_tag)
    
    # Tool name (center)
    bb_name = draw.textbbox((0, 0), data['name'], font=font_name)
    nw, nh = bb_name[2] - bb_name[0], bb_name[3] - bb_name[1]
    nx = 40
    ny = H // 2 - nh // 2 - 10
    draw.text((nx, ny), data['name'], fill=(255, 255, 255), font=font_name)
    
    # Rating badge (bottom-left) if exists
    if data['rating']:
        rating_text = data['rating']
        bb_r = draw.textbbox((0, 0), rating_text, font=font_rating)
        rw, rh = bb_r[2] - bb_r[0], bb_r[3] - bb_r[1]
        # Badge background
        badge_x, badge_y = 40, H - rh - 50
        draw.rounded_rectangle(
            [badge_x - 10, badge_y - 5, badge_x + rw + 20, badge_y + rh + 10],
            radius=6, fill=data['accent']
        )
        draw.text((badge_x, badge_y), rating_text, fill=(0, 0, 0), font=font_rating)
    
    # "Review" label bottom-right
    review_text = "Full Review →"
    bb_rev = draw.textbbox((0, 0), review_text, font=font_tag)
    rw2 = bb_rev[2] - bb_rev[0]
    draw.text((W - rw2 - 40, H - 45), review_text, fill=(150, 150, 160), font=font_tag)
    
    out_path = os.path.join(OUT_DIR, f'{slug}.png')
    img.save(out_path, quality=95)
    print(f"✓ {slug}.png")

print(f"\nDone! {len(tools)} thumbnails generated in {OUT_DIR}")
