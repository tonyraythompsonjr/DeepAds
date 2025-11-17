# path: app.py
import uuid
import logging
from typing import List

import streamlit as st
from PIL import Image

from deepads_copy import (
    AdConfig,
    AdVariant,
    generate_ad_variants_with_alex,
)
from deepads_image import (
    generate_placeholder_hero_image,
    overlay_headline_on_image,
)
from deepads_research import (
    ResearchInsights,
    analyze_market_text,
)

# --------------------------------------------
# Logging
# --------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(request_id)s] %(message)s",
)

def _log(message: str, level: int = logging.INFO) -> None:
    extra = {"request_id": st.session_state.get("request_id", "N/A")}
    logging.log(level, message, extra=extra)


# --------------------------------------------
# Streamlit Setup
# --------------------------------------------
st.set_page_config(
    page_title="DeepAds - AI Ad Studio",
    layout="wide",
    page_icon="🎯",
)

st.markdown(
    """
<style>
.main-heading {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.subheading {
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}
.ad-card {
    padding: 1.5rem;
    border-radius: 1.25rem;
    border: 1px solid #e5e7eb;
    background: #ffffffcc;
    margin-bottom: 1.5rem;
}
.ad-card h3 {
    margin-top: 0;
}
.badge {
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 999px;
    background: #e5e7eb;
    font-size: 0.75rem;
    margin-right: 0.25rem;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-heading">DeepAds: AI Ad Studio</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="subheading">
Craft image & video-ready ads that speak your audience’s language.<br/>
Powered by <b>Alex 4.0</b> (copy brain) + IVOC-style market insights.
</div>
""",
    unsafe_allow_html=True,
)

if "request_id" not in st.session_state:
    st.session_state["request_id"] = str(uuid.uuid4())


# --------------------------------------------
# Sidebar – Ad Configuration
# --------------------------------------------
with st.sidebar:
    st.header("Ad Controls")

    product_description = st.text_area(
        "Product / Offer Description",
        height=140,
        placeholder="Describe your product, offer, or brand in natural language...",
        key="product_description",
    )

    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g. busy parents, SaaS founders, sneakerheads...",
    )

    platform = st.selectbox(
        "Primary Platform",
        ["Facebook", "Instagram", "TikTok", "YouTube", "LinkedIn", "X (Twitter)", "Display"],
    )

    objective = st.selectbox(
        "Ad Objective",
        ["Awareness", "Traffic", "Conversion", "Lead Gen", "Retention"],
    )

    tone = st.selectbox(
        "Tone",
        ["Friendly", "Professional", "Humorous", "Inspirational", "Bold", "Informative"],
    )

    brand_personality = st.multiselect(
        "Brand Personality Tags",
        ["Playful", "Luxurious", "Minimal", "Quirky", "Trusted", "Disruptive"],
        default=["Trusted"],
    )

    voice_style = st.select_slider(
        "Voice Style (Simple → Technical)",
        options=["Very Simple", "Simple", "Balanced", "Technical"],
        value="Balanced",
    )

    frameworks = st.multiselect(
        "Copy Frameworks",
        ["AIDA", "PAS", "4Ps", "Story"],
        default=["AIDA", "PAS", "4Ps"],
    )

    st.markdown("---")
    st.caption("Call-to-Action")

    cta_label = st.selectbox(
        "CTA Template",
        ["Default for Objective", "Shop Now", "Learn More", "Get Started", "Book a Demo", "Sign Up Free"],
    )
    custom_cta = st.text_input(
        "Custom CTA (optional)",
        placeholder="e.g. Start your free trial",
    )

    st.markdown("---")
    uploaded_image_file = st.file_uploader(
        "Optional: Upload Hero Image",
        type=["png", "jpg", "jpeg"],
        help="Use your own product shot or brand visual.",
    )

    overlay_text = st.checkbox(
        "Overlay headline text on image",
        value=False,
        help="Alex 4.0 will stamp the main headline on your hero image.",
    )


# --------------------------------------------
# Tabs: Ad Studio & Market Research
# --------------------------------------------
tab_ads, tab_research = st.tabs(["Ad Studio", "Market Research"])

with tab_research:
    st.subheader("Market Research (IVOC-style)")
    st.write(
        "Paste real language from **reviews, social posts, comments, support tickets, competitor ads**, etc. "
        "Alex 4.0 will mine it for pain points, desires, and objections."
    )

    competitor_corpus = st.text_area(
        "Voice of Customer Text",
        height=220,
        placeholder="Paste screenshots/text from social media, reviews, transcripts...",
        key="voc_text",
    )

    if st.button("Analyze Market"):
        insights: ResearchInsights = analyze_market_text(
            product_description=product_description,
            voc_text=competitor_corpus,
        )
        st.session_state["research_insights"] = insights
        _log("Market analysis computed.")

        st.markdown("#### Key Themes & Signals")

        cols = st.columns(3)
        with cols[0]:
            st.markdown("**Top Keywords**")
            for kw in insights.top_keywords[:10]:
                st.markdown(f"- {kw}")
        with cols[1]:
            st.markdown("**Pain Points**")
            for p in insights.pains[:6]:
                st.markdown(f"- {p}")
        with cols[2]:
            st.markdown("**Desires & Outcomes**")
            for d in insights.desires[:6]:
                st.markdown(f"- {d}")

        if insights.objections:
            st.markdown("**Common Objections**")
            for o in insights.objections[:6]:
                st.markdown(f"- {o}")

with tab_ads:
    st.subheader("Generate Ads")

    st.write(
        "Configure your ad in the sidebar, optionally run **Market Research** first, "
        "then generate tailored variants."
    )

    col_buttons = st.columns([1, 2])
    with col_buttons[0]:
        generate_clicked = st.button("🚀 Generate Ads")
    with col_buttons[1]:
        st.caption("Each framework → one variant. Use results as scripts, captions, or prompts.")

    if generate_clicked:
        if not product_description.strip():
            st.error("Please enter a product / offer description in the sidebar.")
        else:
            insights: ResearchInsights = st.session_state.get(
                "research_insights",
                analyze_market_text(
                    product_description=product_description,
                    voc_text=competitor_corpus or "",
                ),
            )

            config = AdConfig(
                product_description=product_description,
                target_audience=target_audience,
                platform=platform,
                objective=objective,
                tone=tone,
                brand_personality=brand_personality,
                cta_label=cta_label,
                custom_cta=custom_cta,
                frameworks=frameworks or ["AIDA"],
                voice_style=voice_style,
            )

            _log("Generating ad variants with Alex 4.0...")
            variants: List[AdVariant] = generate_ad_variants_with_alex(config, insights)

            if uploaded_image_file is not None:
                try:
                    base_image: Image.Image = Image.open(uploaded_image_file).convert("RGB")
                except Exception as e:
                    st.warning(f"Could not read uploaded image, falling back to placeholder. Error: {e}")
                    base_image = None
            else:
                base_image = None

            for variant in variants:
                st.markdown('<div class="ad-card">', unsafe_allow_html=True)

                col_left, col_right = st.columns([2, 1])

                with col_left:
                    st.markdown(
                        f'<span class="badge">{variant.framework}</span>'
                        f'<span class="badge">{platform}</span>'
                        f'<span class="badge">{objective}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"### {variant.headline}")
                    st.write(variant.body)
                    st.markdown(f"**CTA:** {variant.cta}")
                    st.markdown(f"*Short link:* `{variant.short_link}`")

                with col_right:
                    if base_image is not None:
                        if overlay_text:
                            hero_img = overlay_headline_on_image(base_image, variant.headline)
                        else:
                            hero_img = base_image
                    else:
                        hero_img = generate_placeholder_hero_image(
                            description=product_description,
                            platform=platform,
                        )
                    st.image(hero_img, caption="Hero image preview", use_column_width=True)

                st.markdown("**LTX Studio Prompt**")
                st.code(variant.ltx_prompt, language="markdown")

                st.markdown("</div>", unsafe_allow_html=True)

            st.success("Ads generated. Copy, tweak, and plug into your ad platforms (and LTX Studio).")
            _log("Ad variants rendered.")
