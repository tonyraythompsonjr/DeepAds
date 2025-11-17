import random
from typing import List

from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# --------------------------------------------
# CONFIGURATION AND SETUP
# --------------------------------------------
st.set_page_config(page_title="DeepAds – Micro-AI Ad Studio", layout="centered")
st.title("DeepAds: Micro-AI Ad Studio")
st.write(
    """
Enter a product description and tone to generate ad copy, headlines, and a hero image.
DeepAds uses marketing frameworks (AIDA, PAS, 4 Ps) and trending keyword suggestions.
"""
)

# --------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------
def get_trending_keywords() -> List[str]:
    """Return example trending keywords (stub for a real trends API)."""
    return ["AI", "Sustainability", "Holiday", "Eco-friendly", "2025 Innovations"]


def generate_copy(desc: str, tone: str, fw: str, trends: List[str]) -> str:
    """Generate ad copy text using a simple framework template."""
    product_name = " ".join(desc.strip().split()[:3]) or "your product"
    keyword = trends[0] if trends else "innovation"
    desc = desc.strip().capitalize()

    if fw == "AIDA":
        return f"""Attention: {product_name} – discover the {keyword.lower()} trend everyone's talking about!

Interest: With a {tone.lower()} touch, our {product_name} helps solve your biggest challenge.

Desire: Imagine life with {product_name}. It blends {keyword.lower()} innovation with {tone.lower()} flair.

Action: Don’t wait – click the link below to join the movement!"""

    if fw == "PAS":
        return f"""Problem: Finding a {product_name} that meets your needs is tough.

Agitation: Mediocre options miss out on {keyword.lower()} advantages.

Solution: Our {product_name} offers a {tone.lower()} fix – smart design, trending appeal."""

    if fw == "4 Ps":
        return f"""Product: {desc} with a {tone.lower()} vibe.

Price: Competitive and budget-friendly.

Place: Available worldwide via our store.

Promotion: Limited-time {keyword} bonus!"""

    return desc


def generate_headline(desc: str, trends: List[str]) -> str:
    """Generate a simple, punchy headline."""
    product = " ".join(desc.strip().split()[:3]) or "Your Product"
    keyword = trends[0] if trends else "Innovation"
    return f"{product}: Experience {keyword} Today!"


def generate_image(desc: str) -> Image.Image:
    """Generate a placeholder hero image (Pillow 12+ safe)."""
    width, height = 800, 450
    # Random pastel background
    base_color = tuple(random.randint(200, 255) for _ in range(3))
    image = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(image)

    # Font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    except Exception:
        font = ImageFont.load_default()

    # Caption text
    text = " ".join(desc.strip().split()[:5]) or "Your Product"

    # Pillow 12: use textbbox instead of deprecated textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center position
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Background rectangle behind text
    margin = 20
    rect = [x - margin, y - margin, x + text_width + margin, y + text_height + margin]
    fill = tuple(max(c - 50, 0) for c in base_color)
    draw.rectangle(rect, fill=fill)

    # Draw text
    draw.text((x, y), text, font=font, fill="white")

    return image


def generate_short_link(ad_id: str) -> str:
    """Return a fake short link (stub for Bitly or similar)."""
    return f"https://example.com/{ad_id}"


def display_ad(
    framework: str,
    headline: str,
    copy: str,
    image: Image.Image,
    link: str,
) -> None:
    """Render a single ad variation in the Streamlit UI."""
    st.subheader(f"{framework} Variation")
    st.image(image, caption="Hero image", use_column_width=True)
    st.markdown(f"**Headline:** {headline}")
    st.write(copy)
    st.markdown(f"**CTA Link:** {link}")


# --------------------------------------------
# MAIN APP EXECUTION
# --------------------------------------------
product_desc = st.text_area("Product Description", height=150)
tone = st.selectbox(
    "Desired Tone",
    ["Friendly", "Professional", "Humorous", "Inspirational", "Bold", "Informative"],
)
use_gemini = st.checkbox(
    "Use Gemini (Nano Banana) for image generation", value=False
)

if st.button("Generate Ads"):
    if not product_desc.strip():
        st.error("Please enter a product description.")
    else:
        keywords = get_trending_keywords()
        st.info("Trending keywords: " + ", ".join(keywords))

        for i, fw in enumerate(["AIDA", "PAS", "4 Ps"]):
            copy = generate_copy(product_desc, tone, fw, keywords)
            headline = generate_headline(product_desc, keywords)

            # Default placeholder image
            img = generate_image(product_desc)

            # Optional Gemini (Nano Banana) image generation
            if use_gemini:
                try:
                    from deepads_gemini import deepads_generate_image

                    img = deepads_generate_image(product_desc)
                except Exception as e:
                    st.warning(f"Gemini image generation failed, using placeholder. Error: {e}")

            link = generate_short_link(f"ad{i + 1}")
            display_ad(fw, headline, copy, img, link)
```

You can drop this in as `deepads.py` on your `main` branch, commit, and push. That should clear the `ImageDraw.textsize` error on Streamlit Cloud and let you actually test the Nano Banana / Gemini path next.
