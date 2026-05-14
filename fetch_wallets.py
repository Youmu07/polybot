import requests
import json

url = "https://clob.polymarket.com/markets?limit=50"

response = requests.get(url)
data = response.json()

# Print the structure to see what we got
print(json.dumps(data, indent=2)[:1000])
EOF
