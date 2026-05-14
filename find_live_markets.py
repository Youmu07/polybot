import requests
import json

# Try different Polymarket endpoints
endpoints = [
    "https://clob.polymarket.com/markets?active=true",
    "https://clob.polymarket.com/markets?order=volume&limit=100",
    "https://api.polymarket.com/markets?status=open",
]

print("🔍 Scanning for live markets...")

for endpoint in endpoints:
    try:
        print(f"\nTrying: {endpoint}")
        response = requests.get(endpoint, timeout=5)
        data = response.json()
        
        if isinstance(data, dict):
            markets = data.get('data', data.get('markets', []))
        else:
            markets = data
        
        # Filter for volume > 0 (actually trading)
        live = [m for m in markets if isinstance(m, dict) and m.get('volume24h', 0) > 0]
        
        print(f"   Found {len(live)} markets with volume")
        
        if live:
            print(f"   ✅ TOP MARKET:")
            top = live[0]
            print(f"      {top.get('question', 'N/A')[:60]}")
            print(f"      Volume: ${top.get('volume24h', 0):,}")
            break
            
    except Exception as e:
        print(f"   ✗ {type(e).__name__}")

print("\n" + "="*60)
print("If none work, we need to use websocket or Dune Analytics for real-time data")
