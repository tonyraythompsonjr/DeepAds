# path: deepads_research.py
from dataclasses import dataclass
from collections import Counter
from typing import List


@dataclass
class ResearchInsights:
    top_keywords: List[str]
    pains: List[str]
    desires: List[str]
    objections: List[str]
    raw_notes: str


_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "for", "in", "on", "is", "are",
    "it", "this", "that", "with", "at", "be", "as", "by", "from", "about", "was",
    "were", "have", "had", "has", "but", "if", "they", "you", "we", "i", "so",
}


def _tokenize(text: str) -> List[str]:
    cleaned = ""
    for ch in text.lower():
        cleaned += ch if ch.isalnum() or ch.isspace() else " "
    return [t for t in cleaned.split() if t and t not in _STOPWORDS]


def analyze_market_text(product_description: str, voc_text: str) -> ResearchInsights:
    """
    Lightweight 'research engine':
    - Extracts frequent keywords from product + VOC text.
    - Heuristically guesses pains, desires, objections from sentence patterns.
    """
    combined = f"{product_description}\n{voc_text}".strip()
    tokens = _tokenize(combined)
    counts = Counter(tokens)

    keywords = [w for w, c in counts.most_common(30) if c > 1][:15]

    pains: List[str] = []
    desires: List[str] = []
    objections: List[str] = []

    lines = [l.strip() for l in voc_text.split("\n") if l.strip()]
    for line in lines:
        lower = line.lower()
        if any(trigger in lower for trigger in ["frustrated", "tired of", "annoyed", "hate", "sick of", "doesn't work", "does not work"]):
            pains.append(line)
        if any(trigger in lower for trigger in ["want", "wish", "would love", "looking for", "need", "dream"]):
            desires.append(line)
        if any(trigger in lower for trigger in ["worried", "not sure", "concerned", "skeptical", "afraid"]):
            objections.append(line)

    # Fallbacks if VOC text is sparse
    if not pains and product_description:
        pains.append(f"People struggle to get consistent results with current solutions for {product_description[:80]}...")
    if not desires and product_description:
        desires.append(f"They want a simpler, faster way to benefit from {product_description[:80]}.")

    return ResearchInsights(
        top_keywords=keywords,
        pains=pains,
        desires=desires,
        objections=objections,
        raw_notes=voc_text,
    )
