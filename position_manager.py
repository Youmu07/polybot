import json
from datetime import datetime, timedelta
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

print("="*70)
print("📊 POSITION MANAGER")
print("="*70)

# Open positions from previous trades
open_positions = [
    {
        "id": 1,
        "market": "BTC > $95k by end of May?",
        "entry_price": 0.58,
        "entry_time": "2 hours ago",
        "current_price": 0.62,
        "size": 100,
        "expected_max": 0.85,  # Expected settlement price
        "current_profit": (0.62 - 0.58) * 100  # $4
    },
    {
        "id": 2,
        "market": "Fed cuts rates in June?",
        "entry_price": 0.48,
        "entry_time": "30 min ago",
        "current_price": 0.51,
        "size": 80,
        "expected_max": 0.75,
        "current_profit": (0.51 - 0.48) * 80  # $2.40
    }
]

print(f"\n📈 OPEN POSITIONS: {len(open_positions)}")
for pos in open_positions:
    pnl_pct = (pos['current_profit'] / (pos['entry_price'] * pos['size'])) * 100
    print(f"   {pos['id']}. {pos['market'][:40]}")
    print(f"      Entry: {pos['entry_price']:.2f} | Current: {pos['current_price']:.2f}")
    print(f"      P&L: ${pos['current_profit']:.2f} ({pnl_pct:.1f}%)")

# Claude evaluates each position for exit
print(f"\n🧠 CLAUDE EXIT ANALYSIS")

for pos in open_positions:
    prompt = f"""Position evaluation:

Market: {pos['market']}
Entry: {pos['entry_price']:.2f}
Current: {pos['current_price']:.2f}
Expected max: {pos['expected_max']:.2f}
Profit captured: {((pos['current_price'] - pos['entry_price']) / (pos['expected_max'] - pos['entry_price'])) * 100:.0f}%

Our rule: Exit at 85% of expected move OR 3x volume spike.

Should we exit NOW? Answer: YES or NO (and reason)"""
    
    decision = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"\n   Position {pos['id']}: {decision.content[0].text[:100]}...")

# Execute exits
print(f"\n💰 EXIT EXECUTION")
exited = 0
remaining = len(open_positions)

for pos in open_positions:
    pct_of_max = (pos['current_price'] - pos['entry_price']) / (pos['expected_max'] - pos['entry_price'])
    
    # Exit rule: 85% of expected move
    if pct_of_max >= 0.85:
        print(f"   Position {pos['id']}: EXIT at 85% of move | Lock ${pos['current_profit']:.2f}")
        exited += 1
        remaining -= 1
    else:
        print(f"   Position {pos['id']}: HOLD ({pct_of_max*100:.0f}% of max)")

print(f"\n📊 SUMMARY")
print(f"   Exited: {exited}")
print(f"   Holding: {remaining}")
print(f"   Realized profit this round: ${sum([p['current_profit'] for p in open_positions[:exited]]):.2f}")

# Log results
with open("position_log.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "positions_evaluated": len(open_positions),
        "exited": exited,
        "holding": remaining
    }, f, indent=2)

print(f"\n✓ Logged to position_log.json")
print("="*70)
