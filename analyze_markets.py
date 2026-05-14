import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Load active markets
with open("active_markets.json") as f:
    markets = json.load(f)

# Format for Claude
market_text = "\n".join([
    f"- {m.get('question')} (ends: {m.get('end_date_iso')})"
    for m in markets[:10]
])

prompt = f"""Analyze these active Polymarket prediction markets:

{market_text}

For each:
1. What would you need to know to predict the outcome?
2. Which markets have the clearest binary outcomes?
3. Rank top 3 by "predictability" (how much data exists to forecast them)

Keep it concise."""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)

