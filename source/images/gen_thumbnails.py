#!/usr/bin/env python3
"""Generate article thumbnail cards for AITools review site.
Usage: python3 gen_thumbnails.py [slug]  # generate one, or omit for all
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, math, random

OUT_DIR = '/Users/zhua/aitools/source/images/thumbnails'
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1200, 630  # OG image standard ratio

# Category color palettes
PALETTES = {
    'coding':    {'bg1': (8, 8, 18),    'bg2': (18, 22, 50),   'accent': (99, 102, 241),  'glow': (60, 65, 200),  'tag': 'AI CODING'},
    'marketing': {'bg1': (18, 4, 12),   'bg2': (45, 10, 30),   'accent': (236, 72, 153),  'glow': (200, 50, 120), 'tag': 'AI MARKETING'},
    'content':   {'bg1': (6, 12, 22),   'bg2': (15, 28, 48),   'accent': (14, 165, 233),  'glow': (10, 130, 200), 'tag': 'AI CONTENT'},
    'automation':{'bg1': (4, 14, 8),    'bg2': (12, 38, 22),   'accent': (34, 197, 94),   'glow': (20, 160, 70),  'tag': 'AUTOMATION'},
    'infra':     {'bg1': (12, 8, 18),   'bg2': (32, 18, 48),   'accent': (168, 85, 247),  'glow': (130, 50, 200), 'tag': 'INFRASTRUCTURE'},
    'design':    {'bg1': (18, 6, 14),   'bg2': (48, 15, 35),   'accent': (251, 146, 60),  'glow': (220, 110, 30), 'tag': 'AI DESIGN'},
    'productivity':{'bg1': (8, 12, 18), 'bg2': (18, 26, 42),   'accent': (20, 184, 166),  'glow': (10, 150, 130), 'tag': 'PRODUCTIVITY'},
    'finance':   {'bg1': (6, 12, 8),    'bg2': (16, 32, 22),   'accent': (74, 222, 128),  'glow': (40, 180, 90),  'tag': 'AI FINANCE'},
    'writing':   {'bg1': (16, 10, 6),   'bg2': (38, 25, 14),   'accent': (251, 191, 36),  'glow': (220, 160, 20), 'tag': 'AI WRITING'},
    'default':   {'bg1': (10, 10, 18),  'bg2': (25, 22, 48),   'accent': (99, 102, 241),  'glow': (60, 65, 200),  'tag': 'AI TOOLS'},
}

# Tool definitions
TOOLS = {
    'cursor':           {'name': 'Cursor',              'palette': 'coding',     'rating': 8.5},
    'windsurf':         {'name': 'Windsurf',            'palette': 'coding',     'rating': 8.0},
    'bolt-new':         {'name': 'Bolt.new',            'palette': 'coding',     'rating': 7.5},
    'gamma':            {'name': 'Gamma',               'palette': 'content',    'rating': 8.0},
    'n8n':              {'name': 'n8n',                 'palette': 'automation', 'rating': 8.5},
    'jasper':           {'name': 'Jasper AI',           'palette': 'marketing',  'rating': 7.0},
    'railway':          {'name': 'Railway',             'palette': 'infra',      'rating': 8.0},
    'cursor-vs-windsurf':{'name': 'Cursor vs Windsurf', 'palette': 'coding',     'roundup': True},
    'best-ai-coding-tools-2026': {'name': 'Best AI Coding\ntools 2026', 'palette': 'coding', 'roundup': True},
}

def get_font(size):
    """Get a system font, fallback gracefully."""
    fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Helvetica Neue.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for f in fonts:
        try:
            return ImageFont.truetype(f, size)
        except:
            continue
    return ImageFont.load_default()

def draw_smooth_gradient(img, bg1, bg2):
    """Draw a smooth vertical gradient with Perlin-like noise."""
    draw = ImageDraw.Draw(img)
    random.seed(42)
    for y in range(H):
        t = y / H
        t = t * t * (3 - 2 * t)  # smoothstep
        r = int(bg1[0] + (bg2[0] - bg1[0]) * t)
        g = int(bg1[1] + (bg2[1] - bg1[1]) * t)
        b = int(bg1[2] + (bg2[2] - bg1[2]) * t)
        noise = random.randint(-2, 2)
        r = max(0, min(255, r + noise))
        g = max(0, min(255, g + noise))
        b = max(0, min(255, b + noise))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def add_glow_orbs(img, accent, glow):
    """Add 2-3 large glowing orbs for depth."""
    orbs = [
        (W // 5, H // 3, 180),
        (4 * W // 5, 2 * H // 3, 140),
        (W // 2, H // 2, 100),
    ]
    result = img.convert('RGBA')
    for cx, cy, radius in orbs:
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for r in range(radius, 0, -3):
            alpha = int(18 * (1 - r / radius))
            ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*glow, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=40))
        result = Image.alpha_composite(result, layer)
    return result.convert('RGB')

def add_hex_grid(draw, accent):
    """Draw a subtle hexagonal grid pattern."""
    spacing = 50
    dot_size = 1.5
    color = (*accent, 12)
    for row in range(20):
        for col in range(30):
            x = col * spacing + (spacing // 2 if row % 2 else 0)
            y = row * (spacing * 0.866)
            if 0 <= x <= W and 0 <= y <= H:
                draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], 
                           fill=(*accent, 10))

def add_diagonal_lines(draw, accent, side='right'):
    """Add decorative diagonal accent lines in a corner."""
    if side == 'right':
        for i in range(5):
            x_start = W - 60 + i * 18
            x_end = W
            y_start = 0
            y_end = 60 - i * 18
            draw.line([(x_start, y_start), (x_end, y_end)], fill=(*accent, 25), width=1)
    else:
        for i in range(5):
            x_start = 0
            x_end = 60 - i * 18
            y_start = H - 60 + i * 18
            y_end = H
            draw.line([(x_start, y_start), (x_end, y_end)], fill=(*accent, 25), width=1)

def add_large_letter(draw, name, accent):
    """Add a faded large letter as background element."""
    letter = name[0].upper()
    font_big = get_font(400)
    # Use RGBA for transparency
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    bb = ld.textbbox((0, 0), letter, font=font_big)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    ld.text((W - bw - 30, H - bh + 60), letter, fill=(*accent, 12), font=font_big)
    return layer

def generate_thumbnail(slug, data):
    """Generate a single thumbnail."""
    palette = PALETTES.get(data['palette'], PALETTES['default'])
    bg1, bg2 = palette['bg1'], palette['bg2']
    accent = palette['accent']
    glow = palette['glow']
    
    # Base gradient
    img = Image.new('RGB', (W, H))
    draw_smooth_gradient(img, bg1, bg2)
    
    # Glow orbs for depth
    img = add_glow_orbs(img, accent, glow)
    
    # Hex dot grid
    draw = ImageDraw.Draw(img)
    add_hex_grid(draw, accent)
    
    # Large faded letter in background
    letter_layer = add_large_letter(draw, data['name'], accent)
    img = Image.alpha_composite(img.convert('RGBA'), letter_layer).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Diagonal corner accents
    add_diagonal_lines(draw, accent, 'right')
    add_diagonal_lines(draw, accent, 'left')
    
    # Accent bar at top
    draw.rectangle([0, 0, W, 4], fill=accent)
    
    # Category tag (top-left) — text only, clean
    font_tag = get_font(13)
    tag_text = palette['tag']
    draw.text((48, 32), tag_text, fill=accent, font=font_tag)
    
    # AITools branding (top-right)
    font_brand = get_font(12)
    brand = "AITOOLS"
    bb_b = draw.textbbox((0, 0), brand, font=font_brand)
    draw.text((W - bb_b[2] + bb_b[0] - 48, 35), brand, fill=(100, 100, 120), font=font_brand)
    
    # Tool name — large, centered vertically
    name = data['name']
    font_size = 80 if '\n' not in name else 60
    font_name = get_font(font_size)
    
    lines = name.split('\n')
    line_data = []
    total_h = 0
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font_name)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        line_data.append((line, w, h))
        total_h += h
    total_h += (len(lines) - 1) * 12
    
    start_y = H // 2 - total_h // 2 - 10
    for i, (line, lw, lh) in enumerate(line_data):
        ly = start_y + sum(d[2] + 12 for d in line_data[:i])
        lx = 48
        # Text shadow
        draw.text((lx + 3, ly + 3), line, fill=(0, 0, 0), font=font_name)
        draw.text((lx, ly), line, fill=(255, 255, 255), font=font_name)
    
    # Rating badge or roundup badge (bottom-left)
    if data.get('rating') and not data.get('roundup'):
        rating = data['rating']
        font_rating = get_font(30)
        score_text = f"{rating}/10"
        bb_r = draw.textbbox((0, 0), score_text, font=font_rating)
        rw, rh = bb_r[2] - bb_r[0], bb_r[3] - bb_r[1]
        
        badge_x, badge_y = 48, H - 85
        # Pill badge
        draw.rounded_rectangle(
            [badge_x - 14, badge_y - 8, badge_x + rw + 20, badge_y + rh + 12],
            radius=8, fill=accent
        )
        draw.text((badge_x - 4, badge_y), score_text, fill=(0, 0, 0), font=font_rating)
        
        # "Full Review" link
        font_sm = get_font(14)
        link_text = "FULL REVIEW  →"
        draw.text((badge_x + rw + 24, badge_y + 8), link_text, fill=(130, 130, 150), font=font_sm)
        
    elif data.get('roundup'):
        font_roundup = get_font(15)
        rup_text = "ROUNDUP"
        bb_ru = draw.textbbox((0, 0), rup_text, font=font_roundup)
        ruw = bb_ru[2] - bb_ru[0]
        draw.rounded_rectangle([40, H - 62, 40 + ruw + 24, H - 38], radius=4, fill=accent)
        draw.text((52, H - 59), rup_text, fill=(0, 0, 0), font=font_roundup)
    
    out_path = os.path.join(OUT_DIR, f'{slug}.png')
    img.save(out_path, quality=95)
    print(f"✓ {slug}.png ({W}x{H})")
    return out_path

# Main
if __name__ == '__main__':
    if len(sys.argv) > 1:
        slug = sys.argv[1]
        if slug in TOOLS:
            generate_thumbnail(slug, TOOLS[slug])
        else:
            name = slug.replace('-', ' ').title()
            generate_thumbnail(slug, {'name': name, 'palette': 'default'})
    else:
        for slug, data in TOOLS.items():
            generate_thumbnail(slug, data)
        print(f"\nDone! {len(TOOLS)} thumbnails in {OUT_DIR}")
