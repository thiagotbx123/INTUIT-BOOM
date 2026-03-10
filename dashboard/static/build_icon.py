"""Generate QBO Demo Manager .ico — modern AI/TestBox/synthetic data vibe."""

from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 256
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Rounded rect background — dark forest green
bg = (5, 14, 5, 255)
r = 48
draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=r, fill=bg)

# Subtle grid pattern — synthetic data vibe
grid_color = (20, 50, 20, 80)
for i in range(0, SIZE, 20):
    draw.line([(i, 0), (i, SIZE)], fill=grid_color, width=1)
    draw.line([(0, i), (SIZE, i)], fill=grid_color, width=1)

# Data points — scattered dots like a scatter plot (synthetic data)
import random

random.seed(42)
for _ in range(25):
    x = random.randint(30, 226)
    y = random.randint(100, 200)
    sz = random.randint(3, 6)
    alpha = random.randint(60, 140)
    dot_color = (98, 204, 174, alpha)  # TestBox teal
    draw.ellipse([x - sz, y - sz, x + sz, y + sz], fill=dot_color)

# Rising trend line through the dots — AI/analytics vibe
points = [(30, 200), (80, 170), (128, 145), (176, 120), (226, 90)]
for i in range(len(points) - 1):
    draw.line([points[i], points[i + 1]], fill=(98, 204, 174, 200), width=3)

# Small circle at each trend point
for px, py in points:
    draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(98, 204, 174, 255))

# Glow ring at the top endpoint — AI pulse
cx, cy = 226, 90
for radius in range(18, 4, -2):
    alpha = int(30 * (18 - radius) / 14)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=(98, 204, 174, alpha), width=1)
draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(98, 204, 174, 255))

# "QBO" text at top — bold, clean
try:
    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
except OSError:
    font = ImageFont.load_default()

draw.text((SIZE // 2, 42), "QBO", fill=(224, 242, 239, 255), font=font, anchor="mt")

# Small "DEMO MANAGER" subtitle
try:
    font_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
except OSError:
    font_sm = ImageFont.load_default()

draw.text((SIZE // 2, 75), "DEMO MANAGER", fill=(98, 204, 174, 180), font=font_sm, anchor="mt")

# Purple accent bar at bottom — TestBox purple
draw.rounded_rectangle([30, 225, 226, 233], radius=4, fill=(109, 36, 130, 150))
# Gradient-like: add teal section
draw.rounded_rectangle([30, 225, 128, 233], radius=4, fill=(98, 204, 174, 150))

# Save multi-size ICO
out_dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(out_dir, "qbo-demo-manager.ico")

sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icons = [img.resize(s, Image.LANCZOS) for s in sizes]
icons[-1].save(ico_path, format="ICO", sizes=sizes)

print(f"Icon saved: {ico_path}")
