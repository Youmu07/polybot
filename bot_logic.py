import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Mock live markets (we'll replace with real API data later)
sample_markets = [
    {
        "question": "Will BTC exceed $100k by EOY?",
        "yes_price": 0.62,
        "no_price": 0.38,
        "volume_24h": 250000,
        "spread": 0.24
    },
    {
        "question": "Will Fed raise rates again in 2025?",
        "yes_price": 0.55,
        "no_price": 0.45,
        "volume_24h": 180000,
        "spread": 0.10
    },
    {
        "question": "Will Trump be re-elected?",
        "yes_price": 0.58,
        "no_price": 0.42,
        "volume_24h": 420000,
        "spread": 0.16
    }
]

# Let Claude score these markets
market_text = "\n".join([
    f"- {m['question']} | Yes: {m['yes_price']:.2f} | No: {m['no_price']:.2f} | Volume: ${m['volume_24h']:,} | Spread: {m['spread']:.3f}"
    for m in sample_markets
])

prompt = f"""You are a professional trader analyzing these LIVE Polymarket opportunities.

{market_text}

For each market:
1. What data would you need to gain an edge?
2. What's your confidence in your prediction?
3. Position size: 1-10 (10 = max conviction)

Return ONLY JSON with this structure:
{{
  "markets": [
    {{
      "question": "...",
      "conviction": 1-10,
      "edge": "brief explanation",
      "data_needed": ["list", "of", "data"]
    }}
  ],
  "best_opportunity": "which market"
}}"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

result = response.content[0].text

# Parse and save
print(result)

with open("market_analysis.json", "w") as f:
    f.write(result)

print("\n✓ Saved analysis")
