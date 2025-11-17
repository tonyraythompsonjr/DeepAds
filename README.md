# DeepAds – AI Ad Studio (Python + Streamlit)

DeepAds is a micro AI Ad Studio that helps you:
- Analyze **IVOC (voice of customer)** text (reviews, social, support tickets, competitor ads)
- Generate tailored **ad copy** using multiple frameworks via **Alex 4.0**
- Create **hero image previews** (or overlay your own uploads)
- Output **LTX Studio-ready prompts** for video/image generation

## Stack

- Python 3.11+
- Streamlit for UI
- Pillow for images
- Pytest for tests
- Optional: Anthropic/Claude later for advanced copy

## Getting Started (Local)

```bash
git clone <your-repo-url>.git
cd deepads

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
