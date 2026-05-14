import requests
import json

url = "https://clob.polymarket.com/markets?limit=50"

response = requests.get(url)
data = response.json()

markets = data.get('data', [])

# Filter for active markets
active = [m for m in markets if m.get('accepting_orders') == True]

print(f"Total markets: {len(markets)}")
print(f"Active markets: {len(active)}")

if active:
    print("\nFirst active market:")
    m = active[0]
    print(f"Question: {m.get('question')}")
    print(f"Slug: {m.get('market_slug')}")
    print(f"End date: {m.get('end_date_iso')}")
    
    # Save all active markets
    with open("active_markets.json", "w") as f:
        json.dump(active, f, indent=2)
    print(f"\n✓ Saved {len(active)} active markets to active_markets.json")
else:
    print("No active markets found")
