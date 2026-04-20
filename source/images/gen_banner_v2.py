#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1200, 500

# Base dark gradient using horizontal bands (fast)
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

colors = [(15, 12, 41), (30, 25, 70), (48, 43, 99), (36, 36, 62)]
for y in range(H):
    t = y / H
    if t < 0.33:
        c1, c2 = colors[0], colors[1]
        t2 = t / 0.33
    elif t < 0.66:
        c1, c2 = colors[1], colors[2]
        t2 = (t - 0.33) / 0.33
    else:
        c1, c2 = colors[2], colors[3]
        t2 = (t - 0.66) / 0.34
    r = int(c1[0] + (c2[0] - c1[0]) * t2)
    g = int(c1[1] + (c2[1] - c1[1]) * t2)
    b = int(c1[2] + (c2[2] - c1[2]) * t2)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Diagonal gradient overlay
overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(H):
    for x in range(0, W, 2):
        t = (x + y * 0.5) / W
        alpha = int(20 * t)
        od.point((x, y), fill=(100, 80, 200, alpha))
img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
draw = ImageDraw.Draw(img)

# Glowing orbs (using ellipses with blur)
orb_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
orb_draw = ImageDraw.Draw(orb_layer)

for cx, cy, radius, color in [
    (950, 100, 180, (99, 102, 241)),
    (200, 400, 150, (139, 92, 246)),
    (500, 100, 120, (6, 182, 212)),
    (700, 350, 100, (99, 102, 241)),
]:
    for r in range(radius, 0, -3):
        alpha = int(25 * (1 - r/radius))
        orb_draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, alpha))

orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(radius=35))
img = Image.alpha_composite(img.convert('RGBA'), orb_layer).convert('RGB')
draw = ImageDraw.Draw(img)

# Grid
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=(40, 38, 70), width=1)
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=(40, 38, 70), width=1)

# Network nodes and lines
nodes = [
    (120, 80), (200, 150), (280, 70), (90, 200), (170, 340), (270, 290),
    (1050, 90), (970, 170), (890, 70), (1070, 290), (990, 370), (910, 240),
    (580, 110), (530, 390), (670, 300), (510, 220),
]

lines = [
    ((120,80),(200,150)), ((200,150),(280,70)), ((90,200),(170,340)),
    ((170,340),(270,290)), ((270,290),(120,80)),
    ((1050,90),(970,170)), ((970,170),(890,70)), ((1070,290),(990,370)),
    ((990,370),(910,240)), ((580,110),(530,390)), ((670,300),(510,220)),
    ((510,220),(580,110)),
]

line_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ll = ImageDraw.Draw(line_layer)
for (x1,y1), (x2,y2) in lines:
    ll.line([(x1,y1),(x2,y2)], fill=(99, 102, 241, 50), width=1)
line_layer = line_layer.filter(ImageFilter.GaussianBlur(radius=1))
img = Image.alpha_composite(img.convert('RGBA'), line_layer).convert('RGB')
draw = ImageDraw.Draw(img)

# Draw nodes with glow
for nx, ny in nodes:
    # Outer glow
    for r in range(15, 0, -1):
        alpha = max(0, 30 - r * 2)
        color = (min(255, 180 + alpha), min(255, 180 + alpha), min(255, 220 + alpha))
        draw.ellipse([nx-r, ny-r, nx+r, ny+r], fill=color)
    # Bright core
    draw.ellipse([nx-3, ny-3, nx+3, ny+3], fill=(220, 220, 255))
    draw.ellipse([nx-1, ny-1, nx+1, ny+1], fill=(255, 255, 255))

# Text
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except:
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica Neue.ttc", 72)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica Neue.ttc", 24)
        font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica Neue.ttc", 14)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

# Title with subtle shadow
title = "AITools"
bbox = draw.textbbox((0, 0), title, font=font_title)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx, ty = (W - tw) // 2, H // 2 - th - 35
# Shadow
draw.text((tx+2, ty+2), title, fill=(30, 25, 60), font=font_title)
draw.text((tx, ty), title, fill=(255, 255, 255), font=font_title)

# Subtitle
subtitle = "Honest Reviews for Solopreneurs"
bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
sw = bbox2[2] - bbox2[0]
sx, sy = (W - sw) // 2, ty + th + 20
draw.text((sx, sy), subtitle, fill=(200, 200, 220), font=font_sub)

# Tagline
tagline = "WE TEST AI TOOLS SO YOU DON'T HAVE TO"
bbox3 = draw.textbbox((0, 0), tagline, font=font_tag)
tgw = bbox3[2] - bbox3[0]
tgx, tgy = (W - tgw) // 2, sy + 45
draw.text((tgx, tgy), tagline, fill=(120, 120, 150), font=font_tag)

# Bottom dots
dot_y = H - 40
for i, active in enumerate([False, True, False, False, False]):
    dot_x = W // 2 - 16 + i * 8
    color = (99, 102, 241) if active else (50, 50, 70)
    draw.ellipse([dot_x-2, dot_y-2, dot_x+2, dot_y+2], fill=color)

img.save('/Users/zhua/aitools/source/images/banner.png', quality=95)
print(f"Banner saved: {img.size}")

# Also generate about page banner (same style, different text)
img2 = img.copy()
draw2 = ImageDraw.Draw(img2)
# Clear text area and redraw
draw2.rectangle([0, H//2-100, W, H//2+100], fill=(25, 22, 55))

title2 = "About AITools"
bbox4 = draw2.textbbox((0, 0), title2, font=font_title)
tw2 = bbox4[2] - bbox4[0]
tx2 = (W - tw2) // 2
draw2.text((tx2, ty), title2, fill=(255, 255, 255), font=font_title)

sub2 = "Your trusted source for AI tool reviews"
bbox5 = draw2.textbbox((0, 0), sub2, font=font_sub)
sw2 = bbox5[2] - bbox5[0]
sx2 = (W - sw2) // 2
draw2.text((sx2, sy), sub2, fill=(200, 200, 220), font=font_sub)

img2.save('/Users/zhua/aitools/source/images/about-banner.png', quality=95)
print("About banner saved")
