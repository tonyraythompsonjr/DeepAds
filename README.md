# DeepAds – Micro‑AI Ad Studio (Streamlit)

Simple MVP Streamlit app that:
- Lets a user enter a product description and tone
- Sends the prompt to Claude (Anthropic) to generate ad copy
- (Optional) Can be extended to call image APIs for hero images

## Project Structure

```text
deepads/
  deepads.py                  # Main Streamlit app
  requirements.txt        # Python dependencies
  .streamlit/
    secrets.toml          # Local dev secrets (do *not* commit real keys)
```

## Local Setup

```bash
cd deepads
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export CLAUDE_API_KEY="your_real_key_here"  # or use secrets.toml
streamlit run deepads.py
```

## Deployment to Streamlit Cloud

1. Push this folder to GitHub as a repo (e.g. `deepads`).
2. In Streamlit Cloud, create a new app from that repo and select `deepads.py`.
3. In **App Settings → Secrets**, paste:

   ```toml
   claude_api_key = "YOUR_REAL_CLAUDE_KEY"
   openai_api_key = "YOUR_REAL_OPENAI_KEY"
   ```

4. Deploy the app.
```
