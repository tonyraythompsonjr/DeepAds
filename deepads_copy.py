# path: deepads_copy.py
from dataclasses import dataclass
from typing import List

from deepads_research import ResearchInsights
from deepads_image import suggest_aspect_ratio_for_platform


@dataclass
class AdConfig:
    product_description: str
    target_audience: str
    platform: str
    objective: str
    tone: str
    brand_personality: List[str]
    cta_label: str
    custom_cta: str
    frameworks: List[str]
    voice_style: str  # "Very Simple" | "Simple" | "Balanced" | "Technical"


@dataclass
class AdVariant:
    framework: str
    headline: str
    body: str
    cta: str
    short_link: str
    ltx_prompt: str


def _choose_keyword(insights: ResearchInsights) -> str:
    return insights.top_keywords[0] if insights.top_keywords else "innovation"


def _choose_cta(config: AdConfig) -> str:
    if config.custom_cta.strip():
        return config.custom_cta.strip()

    # Objective-aware default
    if config.cta_label == "Default for Objective":
        mapping = {
            "Awareness": "Learn More",
            "Traffic": "Learn More",
            "Conversion": "Shop Now",
            "Lead Gen": "Get Started",
            "Retention": "See What's New",
        }
        return mapping.get(config.objective, "Learn More")

    return config.cta_label


def _simplify_text_level(text: str, voice_style: str) -> str:
    """
    Very lightweight 'complexity' control.
    In the future, Claude can rewrite based on this signal.
    """
    if voice_style in ("Very Simple", "Simple"):
        # Avoid jargon-y words we might have used
        replacements = {
            "optimize": "improve",
            "conversion": "results",
            "experience": "use",
            "leverage": "use",
        }
        for old, new in replacements.items():
            text = text.replace(old, new).replace(old.capitalize(), new.capitalize())
    elif voice_style == "Technical":
        # Add a little technical flavour
        text += "\n\nTech note: Built with data-driven optimization in mind."
    return text


def _generate_headline(config: AdConfig, insights: ResearchInsights, framework: str) -> str:
    keyword = _choose_keyword(insights)
    product = " ".join(config.product_description.strip().split()[:4]) or "Your Product"
    audience = config.target_audience or "your audience"

    if framework == "AIDA":
        return f"{product}: The {keyword.title()} Upgrade {audience} Actually Use"
    if framework == "PAS":
        return f"Tired of {keyword.lower()} Failures? Meet {product}"
    if framework == "4Ps":
        return f"{product} – {keyword.title()} in Every Detail"
    if framework == "Story":
        return f"How {audience.title()} Go From Stuck to Thriving with {product}"

    return f"{product}: Experience {keyword.title()} Today"


def _generate_body(config: AdConfig, insights: ResearchInsights, framework: str) -> str:
    keyword = _choose_keyword(insights)
    pains = insights.pains[:2]
    desires = insights.desires[:2]
    objections = insights.objections[:1]

    base = config.product_description.strip().capitalize()
    audience = config.target_audience or "your audience"
    tone = config.tone.lower()

    if framework == "AIDA":
        body = f"""**Attention**  
{audience.title()} are craving {keyword.lower()} that actually works.

**Interest**  
{base} is built for {audience} who want less friction and more momentum.

**Desire**  
{" ".join(desires) or "Imagine a simpler, smoother way to hit your goals."}

**Action**  
Tap the CTA to move from “thinking about it” to “doing it” today."""
    elif framework == "PAS":
        problem = pains[0] if pains else f"wasting time on tools that don't fit {audience}"
        agitation = pains[1] if len(pains) > 1 else "your team is tired of trying to duct-tape solutions together"
        body = f"""**Problem**  
You’re {problem}.

**Agitation**  
And it’s not just annoying – {agitation}.

**Solution**  
{base} wraps {keyword.lower()} around how {audience} already work, so you get results without the chaos."""
    elif framework == "4Ps":
        desire_line = desires[0] if desires else "get consistent, predictable results"
        body = f"""**Product**  
{base} designed specifically for {audience}.

**Price**  
Priced so that {audience} can {desire_line} without blowing the budget.

**Place**  
Launch in minutes on {config.platform}.

**Promotion**  
Early adopters get our {keyword.lower()} playbook free."""
    elif framework == "Story":
        obj = objections[0] if objections else f"wondering if this really works for {audience}"
        body = f"""**Before**  
{audience.title()} were stuck {pains[0] if pains else "juggling tools and tactics"}.

**Turning Point**  
They tried {base} and saw {desires[0] if desires else "momentum in days, not months"}.

**After**  
Now they {desires[1] if len(desires) > 1 else "hit goals with less stress"} – even if they were {obj} at first."""
    else:
        body = base

    return _simplify_text_level(body, config.voice_style)


def _generate_short_link(framework: str) -> str:
    # Stub for bitly/rebrandly/etc.
    suffix = framework.lower().replace(" ", "-")
    return f"https://deepads.io/{suffix}-campaign"


def _generate_ltx_prompt(config: AdConfig, variant: AdVariant, insights: ResearchInsights) -> str:
    aspect = suggest_aspect_ratio_for_platform(config.platform)
    audience = config.target_audience or "ideal customers"
    pains = ", ".join(insights.pains[:3]) or "their current frustrations"
    desires = ", ".join(insights.desires[:3]) or "the outcome they want"

    # This is the "bridge" between copy + LTX Studio
    prompt = f"""
Video ad for {config.platform} in {aspect} aspect ratio.

Scene 1 (Hook): 
- Visual: Close-up of {audience} dealing with {pains}.
- On-screen text: "{variant.headline}"

Scene 2 (Solution):
- Visual: {config.product_description[:120]} in action, clear UI/product shots.
- On-screen text: Short benefit bullets highlighting {desires}.

Scene 3 (CTA):
- Visual: Clean end card with logo and simple background.
- On-screen text: "{variant.cta}"

Style: {", ".join(config.brand_personality) or "clean, modern, trustworthy"}.
Tone: {config.tone}.
"""
    return prompt.strip()


def generate_ad_variants_with_alex(config: AdConfig, insights: ResearchInsights) -> List[AdVariant]:
    """
    Main Alex 4.0 entrypoint.
    Today: deterministic templates.
    Future: call Claude API here and let it write copy using these signals.
    """
    variants: List[AdVariant] = []

    if not config.frameworks:
        config.frameworks = ["AIDA"]

    for fw in config.frameworks:
        headline = _generate_headline(config, insights, fw)
        body = _generate_body(config, insights, fw)
        cta = _choose_cta(config)
        short_link = _generate_short_link(fw)

        draft = AdVariant(
            framework=fw,
            headline=headline,
            body=body,
            cta=cta,
            short_link=short_link,
            ltx_prompt="",  # filled below
        )
        draft.ltx_prompt = _generate_ltx_prompt(config, draft, insights)

        variants.append(draft)

    return variants
