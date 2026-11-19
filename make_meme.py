#!/usr/bin/env python3
"""Generate the GTA 6 x make.fun meme for bounty gta6-meme-x-01.

Concept (chosen by Ghal): GTA 6 loading screen — "LOADING SINCE 2013…",
the make.fun ghost as the loading icon, progress stuck at 99% after 13 years,
with a make.fun earn-money pitch in the bottom band.

Output: meme.png (1080x1080 PNG). Assets: assets/mark-1024.png (official
make.fun ghost mark) and assets/wordmark-white.png (official wordmark,
recolored white for the dark background).
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1080
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
BOLD_OBL = FONT_DIR + "DejaVuSans-BoldOblique.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# --- background: Vice City sunset gradient ---
stops = [(0.00, (24, 9, 58)), (0.42, (94, 22, 96)),
         (0.72, (214, 58, 110)), (1.00, (255, 150, 80))]
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            c = lerp(c0, c1, (t - t0) / (t1 - t0))
            break
    for x in range(W):
        px[x, y] = c
img = img.convert("RGBA")

# --- stars in the upper sky ---
rng = random.Random(6)
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stars)
for _ in range(90):
    x, y = rng.randint(0, W), rng.randint(0, 430)
    r = rng.choice([1, 1, 2])
    sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rng.randint(60, 170)))
img.alpha_composite(stars)

# --- palm tree silhouettes (bottom corners) ---
def palm(draw, base_x, base_y, height, lean, scale=1.0):
    dark = (16, 6, 34, 255)
    top_x = base_x + lean
    top_y = base_y - height
    # curved trunk as tapered segments
    n = 14
    pts = []
    for i in range(n + 1):
        t = i / n
        x = base_x + lean * (t ** 1.6)
        y = base_y - height * t
        w = (16 - 9 * t) * scale
        pts.append((x, y, w))
    for i in range(n):
        x0, y0, w0 = pts[i]
        x1, y1, w1 = pts[i + 1]
        draw.polygon([(x0 - w0, y0), (x0 + w0, y0), (x1 + w1, y1), (x1 - w1, y1)], fill=dark)
    # fronds: tapered curved leaves radiating from the crown
    for ang_deg in (-165, -130, -95, -60, -25, 10, 45):
        a = math.radians(ang_deg)
        L = 150 * scale
        steps = 12
        spine = []
        for i in range(steps + 1):
            t = i / steps
            droop = 55 * scale * t * t
            x = top_x + math.cos(a) * L * t
            y = top_y + math.sin(a) * L * t * 0.62 + droop
            spine.append((x, y))
        for i in range(steps):
            x0, y0 = spine[i]
            x1, y1 = spine[i + 1]
            w0 = 13 * scale * (1 - i / steps) + 2
            w1 = 13 * scale * (1 - (i + 1) / steps) + 2
            dx, dy = x1 - x0, y1 - y0
            norm = math.hypot(dx, dy) or 1
            nx, ny = -dy / norm, dx / norm
            draw.polygon([(x0 + nx * w0, y0 + ny * w0), (x0 - nx * w0, y0 - ny * w0),
                          (x1 - nx * w1, y1 - ny * w1), (x1 + nx * w1, y1 + ny * w1)], fill=dark)

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
palm(od, 30, H + 20, 330, 40, 1.0)
palm(od, W - 20, H + 20, 350, -45, 1.05)
img.alpha_composite(overlay)

d = ImageDraw.Draw(img)

def center_text(text, fnt, y, fill, shadow=None):
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2 - bbox[0]
    if shadow:
        d.text((x + 3, y + 4), text, font=fnt, fill=shadow)
    d.text((x, y), text, font=fnt, fill=fill)
    return tw

# --- GTA VI title (GTA white, VI sunset gradient) ---
f_title = font(BOLD_OBL, 168)
gta, vi = "GTA ", "VI"
w_gta = d.textbbox((0, 0), gta, font=f_title)[2]
w_vi = d.textbbox((0, 0), vi, font=f_title)[2]
x0 = (W - (w_gta + w_vi)) // 2
y_title = 66
d.text((x0 + 5, y_title + 6), gta + vi, font=f_title, fill=(40, 8, 50, 200))
d.text((x0, y_title), gta, font=f_title, fill=(255, 255, 255, 255))
# gradient fill for "VI" via mask
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.text((x0 + w_gta, y_title), vi, font=f_title, fill=255)
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gp = grad.load()
for y in range(y_title, y_title + 200):
    t = (y - y_title) / 200
    c = lerp((255, 94, 168), (255, 176, 86), t)
    for x in range(x0 + w_gta, x0 + w_gta + w_vi + 20):
        gp[x, y] = c + (255,)
img.paste(grad, (0, 0), mask)
d = ImageDraw.Draw(img)
center_text("G R A N D   T H E F T   A U T O", font(BOLD, 27), 258, (255, 255, 255, 210))

# --- make.fun ghost as the loading icon, with a soft glow ---
mark = Image.open("assets/mark-1024.png").convert("RGBA")
mark = mark.resize((240, 240), Image.LANCZOS)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([540 - 160, 442 - 160, 540 + 160, 442 + 160], fill=(255, 94, 168, 110))
glow = glow.filter(ImageFilter.GaussianBlur(45))
img.alpha_composite(glow)
img.alpha_composite(mark, (540 - 120, 442 - 120))
d = ImageDraw.Draw(img)

# --- caption ---
center_text("LOADING SINCE 2013…", font(BOLD, 64), 592, (255, 255, 255, 255),
            shadow=(40, 8, 50, 190))

# --- loading bar stuck at 99% ---
bx0, bx1, by, bh = 170, 910, 690, 48
track = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(track)
td.rounded_rectangle([bx0, by, bx1, by + bh], radius=bh // 2, fill=(18, 7, 36, 210))
img.alpha_composite(track)
fill_w = int((bx1 - bx0) * 0.99)
bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bar)
bd.rounded_rectangle([bx0, by, bx0 + fill_w, by + bh], radius=bh // 2, fill=(255, 255, 255, 255))
bargrad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bp = bargrad.load()
for x in range(bx0, bx0 + fill_w):
    t = (x - bx0) / (bx1 - bx0)
    c = lerp((255, 94, 168), (255, 176, 86), t)
    for y in range(by, by + bh):
        bp[x, y] = c + (255,)
img.paste(bargrad, (0, 0), bar)
d = ImageDraw.Draw(img)
d.text((bx1 - 78, by + 8), "99%", font=font(BOLD, 30), fill=(255, 255, 255, 255))
center_text("13 years later… still buffering.", font(BOLD, 38), 762,
            (255, 235, 245, 235), shadow=(40, 8, 50, 170))

# --- bottom band: make.fun wordmark + earn-money pitch ---
band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bnd = ImageDraw.Draw(band)
bnd.rounded_rectangle([90, 872, 990, 1026], radius=30, fill=(14, 5, 30, 215))
img.alpha_composite(band)
d = ImageDraw.Draw(img)
wm = Image.open("assets/wordmark-white.png").convert("RGBA")
wm_h = 58
wm = wm.resize((int(wm.width * wm_h / wm.height), wm_h), Image.LANCZOS)
img.alpha_composite(wm, ((W - wm.width) // 2, 893))
d = ImageDraw.Draw(img)
center_text("Earn real money with your AI agent.", font(BOLD, 35), 966,
            (255, 255, 255, 245))

img.convert("RGB").save("meme.png", "PNG")
print("saved meme.png", img.size)
