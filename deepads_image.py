# path: deepads_image.py
import random
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont


def suggest_aspect_ratio_for_platform(platform: str) -> str:
    mapping = {
        "Facebook": "1:1 or 4:5",
        "Instagram": "4:5 (feed) or 9:16 (Reels)",
        "TikTok": "9:16",
        "YouTube": "16:9",
        "LinkedIn": "1.91:1 or 1:1",
        "X (Twitter)": "16:9",
        "Display": "300x250 / 728x90 / 160x600",
    }
    return mapping.get(platform, "4:5")


def generate_placeholder_hero_image(description: str, platform: str) -> Image.Image:
    """Generate a simple pastel hero image with the first few words stamped."""
    width, height = 900, 500

    base_color = tuple(random.randint(200, 245) for _ in range(3))
    image = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
    except Exception:
        font = ImageFont.load_default()

    text = " ".join(description.strip().split()[:5]) or "Your Product"
    platform_tag = f"{platform} • DeepAds"

    # Headline block
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - tw) / 2
    y = (height - th) / 2

    margin = 24
    rect = [x - margin, y - margin, x + tw + margin, y + th + margin]
    fill = tuple(max(c - 40, 0) for c in base_color)
    draw.rounded_rectangle(rect, radius=24, fill=fill)
    draw.text((x, y), text, font=font, fill="white")

    # Platform tag
    small_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18) if hasattr(ImageFont, "truetype") else font
    pbbox = draw.textbbox((0, 0), platform_tag, font=small_font)
    pw, ph = pbbox[2] - pbbox[0], pbbox[3] - pbbox[1]
    pad = 12
    px, py = width - pw - 2 * pad - 16, height - ph - 2 * pad - 16
    prect = [px, py, px + pw + 2 * pad, py + ph + 2 * pad]
    draw.rounded_rectangle(prect, radius=999, fill=(0, 0, 0, 128))
    draw.text((px + pad, py + pad), platform_tag, font=small_font, fill="white")

    return image


def overlay_headline_on_image(image: Image.Image, headline: str) -> Image.Image:
    """Overlay a semi-transparent headline block on a user-uploaded image."""
    img = image.copy()
    draw = ImageDraw.Draw(img)

    width, height = img.size
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except Exception:
        font = ImageFont.load_default()

    text = headline[:80]
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    margin = 24

    x = (width - tw) / 2
    y = height - th - margin * 3

    rect = [x - margin, y - margin, x + tw + margin, y + th + margin]
    overlay_color: Tuple[int, int, int] = (0, 0, 0)  # dark overlay
    draw.rectangle(rect, fill=overlay_color)
    draw.text((x, y), text, font=font, fill="white")

    return img
