import json
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Anthropic()

# Simulated live markets (next 5 you're watching)
live_markets = [
    {
        "id": 1,
        "question": "BTC > $95k by end of May?",
        "yes_price": 0.58,
        "no_price": 0.42,
        "volume": 320000,
        "spread": 0.16
    },
    {
        "id": 2,
        "question": "Fed cuts rates in June?",
        "yes_price": 0.48,
        "no_price": 0.52,
        "volume": 210000,
        "spread": 0.04
    },
    {
        "id": 3,
        "question": "Ethereum > $3500?",
        "yes_price": 0.61,
        "no_price": 0.39,
        "volume": 180000,
        "spread": 0.22
    }
]

# Simulated whale we're copying
whale = {
    "address": "0xdef0...jkl",
    "recent_bets": ["BTC > 95k", "Fed cuts", "Ethereum > 3500"],
    "conviction": "High on crypto, medium on macro"
}

# Portfolio
portfolio = {
    "cash": 1000.00,  # $1000 starting capital
    "positions": [],
    "trades_executed": 0,
    "wins": 0,
    "losses": 0,
    "pnl": 0
}

print(f"🚀 PAPER TRADING BOT STARTED")
print(f"Starting capital: ${portfolio['cash']:.2f}")
print("="*60)

# For each market, run multi-agent consensus
for market in live_markets:
    print(f"\n📊 Market {market['id']}: {market['question']}")
    print(f"   Yes: {market['yes_price']:.2f} | No: {market['no_price']:.2f}")
    print(f"   Spread: {market['spread']:.3f} | Volume: ${market['volume']:,}")
    
    # Quick Claude decision
    prompt = f"""Quick decision on this market:

{market['question']}
Yes: {market['yes_price']:.2f} | No: {market['no_price']:.2f}
Whale betting on: {whale['recent_bets'][live_markets.index(market)]}
Conviction: {whale['conviction']}

Should we execute? Answer ONLY: YES or NO (and brief reason)"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    
    decision = response.content[0].text
    print(f"   Decision: {decision[:50]}...")
    
    # Simulate execution
    if "YES" in decision.upper():
        # Allocate 10% of portfolio per trade
        trade_size = portfolio['cash'] * 0.10
        portfolio['positions'].append({
            "market_id": market['id'],
            "size": trade_size,
            "entry_price": market['yes_price'],
            "status": "OPEN"
        })
        portfolio['cash'] -= trade_size
        portfolio['trades_executed'] += 1
        print(f"   ✅ TRADE EXECUTED: ${trade_size:.2f}")
    else:
        print(f"   ❌ SKIPPED")

print("\n" + "="*60)
print(f"📈 PORTFOLIO SUMMARY")
print(f"Cash remaining: ${portfolio['cash']:.2f}")
print(f"Positions open: {len(portfolio['positions'])}")
print(f"Trades executed: {portfolio['trades_executed']}")
print(f"Current P&L: ${portfolio['pnl']:.2f}")

# Save
with open("paper_trade_log.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "portfolio": portfolio,
        "markets_analyzed": len(live_markets)
    }, f, indent=2)

print("\n✓ Logged to paper_trade_log.json")
