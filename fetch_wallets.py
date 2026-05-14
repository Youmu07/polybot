import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Load active markets we already fetched
with open("active_markets.json") as f:
    markets = json.load(f)

# Format for Claude
market_text = "\n".join([
    f"- {m.get('question')} | Volume: {m.get('volume_24h', 0)} | Spread: {abs(float(m.get('yes_price', 0.5)) - float(m.get('no_price', 0.5))):.3f}"
    for m in markets[:15]
])

prompt = f"""Analyze these Polymarket prediction markets and identify which ones attract professional traders (smart money):

{market_text}

For each market, score 1-10 on:
1. Information asymmetry (how much advantage insider knowledge gives)
2. Liquidity (easy to enter/exit big positions)
3. Predictability (data-driven vs pure speculation)

Rank top 5 markets that a professional trader would target.
Why would they trade each one?"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=800,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)

# Save the analysis
with open("trader_targets.txt", "w") as f:
    f.write(response.content[0].text)

print("\n✓ Saved analysis to trader_targets.txt")
