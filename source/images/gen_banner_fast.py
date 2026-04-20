#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 500

# 1. Base gradient (horizontal bands - fast)
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    if t < 0.33:
        c = (int(15 + 15*t/0.33), int(12 + 13*t/0.33), int(41 + 29*t/0.33))
    elif t < 0.66:
        t2 = (t - 0.33) / 0.33
        c = (int(30 + 18*t2), int(25 + 18*t2), int(70 + 29*t2))
    else:
        t2 = (t - 0.66) / 0.34
        c = (int(48 - 12*t2), int(43 - 7*t2), int(99 - 37*t2))
    draw.line([(0, y), (W, y)], fill=c)

# 2. Glowing orbs (fast: draw on small canvas, resize, composite)
orb_small = Image.new('RGBA', (W//8, H//8), (0,0,0,0))
od = ImageDraw.Draw(orb_small)
for cx, cy, r, color in [
    (950//8, 100//8, 22, (99, 102, 241, 40)),
    (200//8, 400//8, 18, (139, 92, 246, 35)),
    (500//8, 100//8, 15, (6, 182, 212, 25)),
    (700//8, 350//8, 12, (99, 102, 241, 30)),
]:
    od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
orb_big = orb_small.resize((W, H), Image.LANCZOS)
img = Image.alpha_composite(img.convert('RGBA'), orb_big).convert('RGB')
draw = ImageDraw.Draw(img)

# 3. Grid
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=(38, 35, 65), width=1)
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=(38, 35, 65), width=1)

# 4. Network lines
nodes = [
    (120,80),(200,150),(280,70),(90,200),(170,340),(270,290),
    (1050,90),(970,170),(890,70),(1070,290),(990,370),(910,240),
    (580,110),(530,390),(670,300),(510,220),
]
lines = [
    ((120,80),(200,150)),((200,150),(280,70)),((90,200),(170,340)),
    ((170,340),(270,290)),((270,290),(120,80)),
    ((1050,90),(970,170)),((970,170),(890,70)),((1070,290),(990,370)),
    ((990,370),(910,240)),((580,110),(530,390)),((670,300),(510,220)),
    ((510,220),(580,110)),
]
for (x1,y1),(x2,y2) in lines:
    draw.line([(x1,y1),(x2,y2)], fill=(70, 65, 130), width=1)

# 5. Nodes
for nx, ny in nodes:
    draw.ellipse([nx-10, ny-10, nx+10, ny+10], fill=(60, 55, 100))
    draw.ellipse([nx-5, ny-5, nx+5, ny+5], fill=(100, 95, 160))
    draw.ellipse([nx-2, ny-2, nx+2, ny+2], fill=(200, 200, 240))

# 6. Text
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_tag = ImageFont.load_default()

title = "AITools"
bb = draw.textbbox((0,0), title, font=font_title)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
tx, ty = (W-tw)//2, H//2 - th - 35
draw.text((tx+2, ty+2), title, fill=(30, 25, 60), font=font_title)
draw.text((tx, ty), title, fill=(255, 255, 255), font=font_title)

sub = "Honest Reviews for Solopreneurs"
bb2 = draw.textbbox((0,0), sub, font=font_sub)
sx, sy = (W-bb2[2]+bb2[0])//2, ty + th + 20
draw.text((sx, sy), sub, fill=(200, 200, 220), font=font_sub)

tag = "WE TEST AI TOOLS SO YOU DON'T HAVE TO"
bb3 = draw.textbbox((0,0), tag, font=font_tag)
tgx = (W-bb3[2]+bb3[0])//2
tgy = sy + 45
draw.text((tgx, tgy), tag, fill=(120, 120, 150), font=font_tag)

# Dots
dot_y = H - 40
for i, active in enumerate([False, True, False, False, False]):
    dx = W//2 - 16 + i*8
    c = (99, 102, 241) if active else (50, 50, 70)
    draw.ellipse([dx-2, dot_y-2, dx+2, dot_y+2], fill=c)

img.save('/Users/zhua/aitools/source/images/banner.png', quality=95)
print(f"Banner OK: {img.size}")

# About banner - copy and re-draw title
img2 = Image.new('RGB', (W, H))
draw2 = ImageDraw.Draw(img2)
for y in range(H):
    t = y / H
    if t < 0.33:
        c = (int(15 + 15*t/0.33), int(12 + 13*t/0.33), int(41 + 29*t/0.33))
    elif t < 0.66:
        t2 = (t - 0.33) / 0.33
        c = (int(30 + 18*t2), int(25 + 18*t2), int(70 + 29*t2))
    else:
        t2 = (t - 0.66) / 0.34
        c = (int(48 - 12*t2), int(43 - 7*t2), int(99 - 37*t2))
    draw2.line([(0, y), (W, y)], fill=c)
img2 = Image.alpha_composite(img2.convert('RGBA'), orb_big).convert('RGB')
draw2 = ImageDraw.Draw(img2)
for x in range(0, W, 40):
    draw2.line([(x, 0), (x, H)], fill=(38, 35, 65), width=1)
for y in range(0, H, 40):
    draw2.line([(0, y), (W, y)], fill=(38, 35, 65), width=1)
for (x1,y1),(x2,y2) in lines:
    draw2.line([(x1,y1),(x2,y2)], fill=(70, 65, 130), width=1)
for nx, ny in nodes:
    draw2.ellipse([nx-10, ny-10, nx+10, ny+10], fill=(60, 55, 100))
    draw2.ellipse([nx-5, ny-5, nx+5, ny+5], fill=(100, 95, 160))
    draw2.ellipse([nx-2, ny-2, nx+2, ny+2], fill=(200, 200, 240))

t2 = "About AITools"
bb4 = draw2.textbbox((0,0), t2, font=font_title)
tw2, th2 = bb4[2]-bb4[0], bb4[3]-bb4[1]
draw2.text(((W-tw2)//2, ty), t2, fill=(255,255,255), font=font_title)
s2 = "Your trusted source for AI tool reviews"
bb5 = draw2.textbbox((0,0), s2, font=font_sub)
sw2 = bb5[2]-bb5[0]
draw2.text(((W-sw2)//2, sy), s2, fill=(200,200,220), font=font_sub)

img2.save('/Users/zhua/aitools/source/images/about-banner.png', quality=95)
print("About banner OK")
