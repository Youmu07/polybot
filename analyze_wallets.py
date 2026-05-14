import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Sample wallet data (we'll get real data later)
sample_wallets = [
    {
        "address": "0x1234...abc",
        "trade_count": 127,
        "win_rate": 0.72,
        "profit": 24500,
        "avg_entry_time": "2h before resolution",
        "avg_exit_time": "89% of settlement",
        "markets_traded": ["crypto", "politics", "macro"],
        "biggest_win": 5200,
        "largest_loss": -800
    },
    {
        "address": "0x5678...def",
        "trade_count": 89,
        "win_rate": 0.68,
        "profit": 12300,
        "avg_entry_time": "4h before resolution",
        "avg_exit_time": "72% of settlement",
        "markets_traded": ["politics"],
        "biggest_win": 3100,
        "largest_loss": -600
    },
    {
        "address": "0x9abc...ghi",
        "trade_count": 156,
        "win_rate": 0.71,
        "profit": 31200,
        "avg_entry_time": "1h before resolution",
        "avg_exit_time": "91% of settlement",
        "markets_traded": ["crypto", "macro", "sports"],
        "biggest_win": 8900,
        "largest_loss": -1200
    },
    {
        "address": "0xdef0...jkl",
        "trade_count": 201,
        "win_rate": 0.75,
        "profit": 48700,
        "avg_entry_time": "30m before resolution",
        "avg_exit_time": "87% of settlement",
        "markets_traded": ["all"],
        "biggest_win": 12000,
        "largest_loss": -2100
    }
]

# Let Claude score them and generate ranking logic
wallet_text = "\n".join([
    f"Wallet {w['address']} | Trades: {w['trade_count']} | Win Rate: {w['win_rate']*100:.0f}% | Profit: ${w['profit']:,} | Exit Time: {w['avg_exit_time']}"
    for w in sample_wallets
])

prompt = f"""You are analyzing professional traders on Polymarket. Score each wallet by "copiability" - how predictable and profitable their strategy is.

{wallet_text}

For each wallet:
1. Strategy consistency (1-10)
2. Profit per trade (score quality)
3. Risk management (win/loss ratio)
4. Exit discipline (do they exit early?)

Then generate a SCORING FUNCTION in Python that ranks new wallets.

Return ONLY JSON:
{{
  "ranked_wallets": [
    {{
      "address": "...",
      "copiability_score": 1-100,
      "strategy": "brief description",
      "reason": "why copy this trader"
    }}
  ],
  "scoring_function": "Python code that takes a wallet dict and returns a score 1-100"
}}"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1500,
    messages=[{"role": "user", "content": prompt}]
)

result = response.content[0].text
print(result)

# Save
with open("wallet_rankings.json", "w") as f:
    f.write(result)

print("\n✓ Saved rankings to wallet_rankings.json")
