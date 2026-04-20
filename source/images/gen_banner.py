#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math, random

random.seed(42)

W, H = 1200, 500
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# Draw gradient background (dark blue-purple)
for y in range(H):
    for x in range(W):
        t = (x + y) / (W + H)
        if t < 0.5:
            t2 = t * 2
            r = int(15 + (48 - 15) * t2)
            g = int(12 + (43 - 12) * t2)
            b = int(41 + (99 - 41) * t2)
        else:
            t2 = (t - 0.5) * 2
            r = int(48 + (36 - 48) * t2)
            g = int(43 + (36 - 43) * t2)
            b = int(99 + (62 - 99) * t2)
        img.putpixel((x, y), (r, g, b))

# Add subtle grid
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 8), width=1)
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=(255, 255, 255, 8), width=1)

# Add glowing orbs
from PIL import ImageFilter

orb_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
orb_draw = ImageDraw.Draw(orb_layer)

for r in range(150, 0, -1):
    alpha = int(60 * (1 - r/150))
    orb_draw.ellipse([1050-r, -50-r, 1050+r, -50+r], fill=(99, 102, 241, alpha))

for r in range(125, 0, -1):
    alpha = int(50 * (1 - r/125))
    orb_draw.ellipse([150-r, 420-r, 150+r, 420+r], fill=(139, 92, 246, alpha))

for r in range(100, 0, -1):
    alpha = int(35 * (1 - r/100))
    orb_draw.ellipse([400-r, 50-r, 400+r, 50+r], fill=(6, 182, 212, alpha))

orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(radius=40))
img = Image.alpha_composite(img.convert('RGBA'), orb_layer).convert('RGB')
draw = ImageDraw.Draw(img)

# Network nodes
nodes = [
    (120, 80), (200, 150), (280, 60), (100, 200), (160, 350), (260, 300), (350, 400),
    (1050, 100), (980, 180), (900, 80), (1080, 300), (1000, 380), (920, 250),
    (600, 120), (550, 380), (650, 300), (500, 200), (700, 420),
]

lines = [
    ((120,80),(200,150)), ((200,150),(280,60)), ((100,200),(160,350)),
    ((260,300),(350,400)), ((160,350),(260,300)),
    ((1050,100),(980,180)), ((980,180),(900,80)), ((1080,300),(1000,380)),
    ((1000,380),(920,250)), ((600,120),(550,380)), ((650,300),(500,200)),
    ((550,380),(700,420)), ((500,200),(600,120)),
]

for (x1,y1), (x2,y2) in lines:
    steps = max(abs(x2-x1), abs(y2-y1))
    if steps == 0: continue
    for i in range(steps):
        t = i / steps
        x = int(x1 + (x2-x1) * t)
        y = int(y1 + (y2-y1) * t)
        alpha = int(80 * (1 - abs(t - 0.5) * 2))
        if 0 <= x < W and 0 <= y < H:
            img.putpixel((x, y), (
                min(255, img.getpixel((x,y))[0] + alpha//4),
                min(255, img.getpixel((x,y))[1] + alpha//4),
                min(255, img.getpixel((x,y))[2] + alpha//3),
            ))

for nx, ny in nodes:
    for r in range(12, 0, -1):
        alpha = int(40 * (1 - r/12))
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx*dx + dy*dy <= r*r:
                    px, py = nx+dx, ny+dy
                    if 0 <= px < W and 0 <= py < H:
                        orig = img.getpixel((px, py))
                        img.putpixel((px, py), (
                            min(255, orig[0] + alpha),
                            min(255, orig[1] + alpha),
                            min(255, orig[2] + alpha),
                        ))
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                px, py = nx+dx, ny+dy
                if 0 <= px < W and 0 <= py < H:
                    img.putpixel((px, py), (220, 220, 255))

draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_tag = ImageFont.load_default()

title = "AITools"
bbox = draw.textbbox((0, 0), title, font=font_title)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx, ty = (W - tw) // 2, H // 2 - th - 30
draw.text((tx, ty), title, fill=(255, 255, 255), font=font_title)

subtitle = "Honest Reviews for Solopreneurs"
bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
sw = bbox2[2] - bbox2[0]
sx, sy = (W - sw) // 2, ty + th + 20
draw.text((sx, sy), subtitle, fill=(200, 200, 220), font=font_sub)

tagline = "WE TEST AI TOOLS SO YOU DON'T HAVE TO"
bbox3 = draw.textbbox((0, 0), tagline, font=font_tag)
tgw = bbox3[2] - bbox3[0]
tgx, tgy = (W - tgw) // 2, sy + 45
draw.text((tgx, tgy), tagline, fill=(120, 120, 150), font=font_tag)

dot_y = H - 40
for i, active in enumerate([False, True, False, False, False]):
    dot_x = W // 2 - 16 + i * 8
    color = (99, 102, 241) if active else (60, 60, 80)
    draw.ellipse([dot_x-2, dot_y-2, dot_x+2, dot_y+2], fill=color)

img.save('/Users/zhua/aitools/source/images/banner.png', quality=95)
print(f"Banner saved: {img.size}")
