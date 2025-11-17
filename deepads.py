"""
DeepAds: A Micro‑AI Ad Studio Web Application
------------------------------------------------

This Streamlit app provides a simple demonstration of how small businesses can
generate AI‑assisted advertising assets in minutes.  Users enter a product
description and choose a desired tone, and the app returns several
ready‑to‑use ad variations based on classic copywriting frameworks.  Each
variation includes a suggested headline, long‑form ad copy and a hero image.

Features
~~~~~~~~
* **Classic frameworks:**  The app produces ads based on three well‑known
  frameworks – AIDA, PAS and the 4 Ps.  AIDA stands for Awareness, Interest,
  Desire and Action.  It guides the reader through stages from creating brand
  awareness to motivating a call‑to‑action【582524550060636†L104-L115】.  PAS stands for
  Problem, Agitation and Solution; it helps copywriters define the problem,
  amplify its urgency and then present the product as the solution【809525659244526†L49-L71】.  The
  4 Ps – Product, Price, Place and Promotion – summarise key variables in the
  marketing mix【403791336675877†L17-L27】.

* **Trending keywords:**  A simple helper function demonstrates how trend
  analysis could be integrated.  In practice, you might call a social media
  analytics API to fetch the latest trending keywords.  Services like
  SocialKit expose APIs for transcript keyword mining and comment trend
  analysis to identify emerging themes【832569334843501†L8-L44】.  Here we return a
  static list of example keywords.

* **Multivariate testing ready:**  Each ad variation includes a short link
  placeholder.  Real‑world implementations could integrate with a link
  shortening service like Bitly, which provides analytics and multichannel
  tracking to compare performance across ad variations【406802743636952†L128-L144】.

Note that this application uses local stub functions in place of external
AI services.  To integrate with a real large language model (e.g., Anthropic’s
Claude or OpenAI’s GPT) or image generator (e.g., Nano Banana), replace
`generate_copy` and `generate_image` with appropriate API calls.
"""

import io
import random
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

import streamlit as st


def get_trending_keywords() -> List[str]:
    """Return a list of trending keywords.

    In a production system you would call a social media analytics API to
    fetch real‑time trending keywords or topics.  For example, the SocialKit
    API can extract frequently mentioned keywords from video transcripts and
    comments【832569334843501†L8-L44】.  Here we return a static list for demonstration.

    Returns
    -------
    List[str]
        A list of example trending keywords.
    """
    return ["AI", "Sustainability", "Holiday", "Eco‑friendly", "2025 Innovations"]


def generate_copy(
    product_description: str,
    tone: str,
    framework: str,
    trending_keywords: List[str],
) -> str:
    """Generate ad copy using a specified framework.

    This is a placeholder implementation designed to illustrate how different
    copywriting frameworks structure persuasive messages.  In practice, you
    would call a large language model here and pass a prompt seeded with
    winning ad frameworks (AIDA, PAS, 4 Ps) along with the product description,
    desired tone and trending keywords.  The model would then return
    sophisticated copy.

    Parameters
    ----------
    product_description : str
        A description of the product or service.
    tone : str
        The desired tone (e.g., friendly, professional).
    framework : str
        The copywriting framework to use ("AIDA", "PAS", or "4 Ps").
    trending_keywords : List[str]
        A list of trending keywords to weave into the copy.

    Returns
    -------
    str
        Generated ad copy text.
    """
    desc = product_description.strip().capitalize()
    # Extract a simple product name (first three words) for use in headlines
    product_name = " ".join(product_description.strip().split()[:3])
    keyword = trending_keywords[0] if trending_keywords else ""

    if framework == "AIDA":
        # Awareness
        attention = (
            f"Attention: {product_name} – discover the {keyword.lower()} trend everyone's talking about!"
        )
        # Interest
        interest = (
            f"Interest: With a {tone.lower()} touch, our {product_name} helps you solve your biggest challenge. "
            f"It’s designed to catch the eye and resonate with your audience."
        )
        # Desire
        desire = (
            f"Desire: Imagine how much easier life could be with {product_name}. "
            f"It combines {keyword.lower()} innovation with {tone.lower()} flair to deliver results you’ll love."
        )
        # Action
        action = (
            "Action: Don’t wait – click the link below to experience it yourself and join the movement!"
        )
        return "\n\n".join([attention, interest, desire, action])

    elif framework == "PAS":
        # Problem
        problem = (
            f"Problem: You’ve been looking for {product_name} that truly meets your needs, but most options fall short."
        )
        # Agitation
        agitation = (
            f"Agitation: Settling for mediocre solutions means missing out on the {keyword.lower()} advantages others are enjoying."
        )
        # Solution
        solution = (
            f"Solution: Our {product_name} offers a {tone.lower()} answer. It solves the problem with smart design and trending appeal."
        )
        return "\n\n".join([problem, agitation, solution])

    elif framework == "4 Ps":
        product = (
            f"Product: {desc} is engineered with a {tone.lower()} vibe to stand out."
        )
        price = (
            "Price: Contact us for a competitive offer that suits your budget."
        )
        place = (
            "Place: Available worldwide via our online store – accessible wherever you shop."
        )
        promotion = (
            f"Promotion: Limited‑time {keyword} bonus! Act now to secure your exclusive deal."
        )
        return "\n\n".join([product, price, place, promotion])

    else:
        return desc


def generate_headline(product_description: str, trending_keywords: List[str]) -> str:
    """Generate a simple headline for the advertisement.

    A headline should be punchy and reflect both the product and a trending
    angle.  In a real system this function would again call an LLM to generate
    several headline options.  Here we assemble a straightforward headline
    combining the product name with the first trending keyword.

    Parameters
    ----------
    product_description : str
        The description of the product.
    trending_keywords : List[str]
        List of trending keywords to incorporate.

    Returns
    -------
    str
        A headline string.
    """
    product_name = " ".join(product_description.strip().split()[:3])
    keyword = trending_keywords[0] if trending_keywords else "Innovation"
    return f"{product_name}: Experience {keyword} Today!"


def generate_image(product_description: str) -> Image.Image:
    """Generate a placeholder hero image.

    Since we cannot call external image generation services from this example,
    this function creates a simple image with a random pastel background and
    overlays the product name as text.  Replace this stub with a call to
    your preferred image generation API (e.g., Nano Banana) in a production
    environment.

    Parameters
    ----------
    product_description : str
        The product description used to annotate the image.

    Returns
    -------
    PIL.Image.Image
        A Pillow image object.
    """
    width, height = 800, 450
    # Generate a random pastel background colour
    base_color = (
        random.randint(200, 255),
        random.randint(200, 255),
        random.randint(200, 255),
    )
    image = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(image)
    # Attempt to use a default font; Streamlit will handle rendering fallback
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    text = " ".join(product_description.strip().split()[:5])
    text = text if text else "Your Product"
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((width - text_width) / 2, (height - text_height) / 2)
    # Place semi‑transparent rectangle behind text for readability
    rect_margin = 20
    rect_coords = [
        text_position[0] - rect_margin,
        text_position[1] - rect_margin,
        text_position[0] + text_width + rect_margin,
        text_position[1] + text_height + rect_margin,
    ]
    rect_color = (
        max(base_color[0] - 50, 0),
        max(base_color[1] - 50, 0),
        max(base_color[2] - 50, 0),
    )
    draw.rectangle(rect_coords, fill=rect_color)
    draw.text(text_position, text, font=font, fill="white")
    return image


def generate_short_link(ad_id: str) -> str:
    """Create a placeholder short link for the call‑to‑action.

    Bitly and similar services allow marketers to create and track unique
    shortened URLs.  Each variation can have its own link so that click
    through rates can be measured and fed back into future prompts.  In
    practice, you would call the Bitly API here and obtain a real short
    URL【406802743636952†L128-L144】.  This stub returns a synthetic link based on the
    ad identifier.

    Parameters
    ----------
    ad_id : str
        A unique identifier for the ad variation.

    Returns
    -------
    str
        A dummy short link.
    """
    return f"https://example.com/{ad_id}"


def display_ad_variation(
    framework: str,
    headline: str,
    copy: str,
    image: Image.Image,
    short_link: str,
) -> None:
    """Render an ad variation in the Streamlit interface."""
    st.subheader(f"{framework} Variation")
    st.image(image, caption="Hero image", use_column_width=True)
    st.markdown(f"**Headline:** {headline}")
    st.write(copy)
    st.markdown(f"**CTA Link:** {short_link}")


def main() -> None:
    """Main entry point for the Streamlit application."""
    st.set_page_config(page_title="DeepAds – Micro‑AI Ad Studio", layout="centered")
    st.title("DeepAds: Micro‑AI Ad Studio")
    st.write(
        "Enter a product description and choose a tone to instantly generate ad copy, "
        "headlines, and a hero image.  DeepAds uses classic marketing frameworks "
        "(AIDA, PAS, 4 Ps) and trending keyword analysis to inspire your advertising."
    )
    # Collect user inputs
    product_desc = st.text_area("Product Description", height=150)
    tone_options = [
        "Friendly",
        "Professional",
        "Humorous",
        "Inspirational",
        "Bold",
        "Informative",
    ]
    tone = st.selectbox("Desired Tone", tone_options)

    if st.button("Generate Ads"):
        if not product_desc.strip():
            st.error("Please enter a product description to generate ads.")
            return
        # Fetch trending keywords
        trending = get_trending_keywords()
        st.info("Trending keywords: " + ", ".join(trending))
        frameworks = ["AIDA", "PAS", "4 Ps"]
        for idx, fw in enumerate(frameworks):
            ad_copy = generate_copy(product_desc, tone, fw, trending)
            headline = generate_headline(product_desc, trending)
            image = generate_image(product_desc)
            short_link = generate_short_link(f"ad{idx + 1}")
            display_ad_variation(fw, headline, ad_copy, image, short_link)


if __name__ == "__main__":
    main()

# … existing imports and copy-generation code …
from PIL import Image  # already used in helper

# Add a checkbox or separate section if you want the user to enable image generation
generate_image = st.checkbox("Generate hero image with Gemini (Nano Banana)", value=True)

if st.button("Generate Ad"):
    # Validate input
    if not product_desc:
        st.error("Please enter a product description.")
    else:
        # Generate headline and copy via your LLM (Claude/GPT) as before …

        # If image generation enabled, call the helper
        if generate_image:
            with st.spinner("Creating hero image…"):
                try:
                    hero_img = deepads_generate_image(product_desc)
                    st.image(hero_img, caption="Hero image from Nano Banana",
                             use_column_width=True)
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
