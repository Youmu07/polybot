import requests
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Anthropic()

# Fetch REAL live markets
url = "https://clob.polymarket.com/markets?limit=20"

try:
    response = requests.get(url, timeout=10)
    markets = response.json()
    active_markets = markets.get('data', [])
    
    # Filter for actually trading
    trading = [m for m in active_markets if m.get('accepting_orders')]
    
    print(f"🔴 LIVE MARKET MONITOR")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total active: {len(trading)}")
    print("="*70)
    
    if not trading:
        print("No actively trading markets right now")
    else:
        # Show top 5
        for i, m in enumerate(trading[:5], 1):
            print(f"\n{i}. {m.get('question', 'N/A')[:60]}")
            print(f"   Volume 24h: ${m.get('volume24h', 0):,}")
            print(f"   Yes: {m.get('yes_price', 0):.2f} | No: {m.get('no_price', 0):.2f}")
    
    # Let Claude score the trading environment
    market_summary = f"Found {len(trading)} actively trading markets. Top opportunities: {[m.get('question', 'N/A')[:40] for m in trading[:3]]}"
    
    prompt = f"""Market environment right now:

{market_summary}

In 2 sentences: Is this a good environment for the bot to trade? Why or why not?"""
    
    analysis = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"\n{'='*70}")
    print(f"📊 CLAUDE ASSESSMENT:")
    print(analysis.content[0].text)
    
    # Save snapshot
    with open("market_snapshot.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "active_markets": len(trading),
            "top_3": [m.get('question', 'N/A') for m in trading[:3]]
        }, f, indent=2)
    
    print(f"\n✓ Snapshot saved")
    
except Exception as e:
    print(f"Error: {e}")
