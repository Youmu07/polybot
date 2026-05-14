import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Simulate 5 past trades (what actually happened)
past_trades = [
    {
        "market": "Will Fed raise rates in 2025?",
        "whale_prediction": "No (0.45)",
        "actual_outcome": "No",
        "our_trade": "Followed whale → No",
        "result": "WIN"
    },
    {
        "market": "BTC > $100k by EOY?",
        "whale_prediction": "Yes (0.62)",
        "actual_outcome": "Yes",
        "our_trade": "Followed whale → Yes",
        "result": "WIN"
    },
    {
        "market": "Trump re-elected 2024?",
        "whale_prediction": "Yes (0.58)",
        "actual_outcome": "Yes",
        "our_trade": "Followed whale → Yes",
        "result": "WIN"
    },
    {
        "market": "OpenSea FDV > $5B?",
        "whale_prediction": "Yes (0.55)",
        "actual_outcome": "No",
        "our_trade": "Followed whale → Yes",
        "result": "LOSS"
    },
    {
        "market": "Julie Su Labor Secretary?",
        "whale_prediction": "No (0.42)",
        "actual_outcome": "No",
        "our_trade": "Followed whale → No",
        "result": "WIN"
    }
]

trades_text = "\n".join([
    f"{i+1}. {t['market']} → {t['result']}"
    for i, t in enumerate(past_trades)
])

prompt = f"""Backtest Summary:

{trades_text}

Evaluate:
1. Win rate: ___/5
2. What worked (winning strategy patterns)?
3. What failed (losing trades root cause)?
4. Adjustments needed?

Return JSON:
{{
  "win_rate": 0.XX,
  "wins": N,
  "losses": N,
  "patterns": ["pattern 1", "pattern 2"],
  "failures": ["reason 1", "reason 2"],
  "next_adjustments": ["adjustment 1", "adjustment 2"]
}}"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=600,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)

with open("backtest_results.json", "w") as f:
    f.write(response.content[0].text)

print("\n✓ Backtest complete")
