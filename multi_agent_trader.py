import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Sample market + wallet we want to trade
market = {
    "question": "Will Fed raise rates in 2025?",
    "yes_price": 0.55,
    "no_price": 0.45,
    "volume_24h": 180000,
    "spread": 0.10
}

top_wallet = {
    "address": "0xdef0...jkl",
    "win_rate": 0.75,
    "exit_discipline": 0.87,
    "profit_per_trade": 242,
    "recent_activity": "Exited 3 Fed-related markets early with 89% accuracy"
}

# Agent 1: Whale Copier
def agent_whale_copier():
    prompt = f"""You are a whale-copy agent. Analyze if we should copy this wallet's strategy:

Market: {market['question']}
Wallet: {top_wallet['address']} | Win Rate: {top_wallet['win_rate']*100:.0f}% | Exit Discipline: {top_wallet['exit_discipline']*100:.0f}%

Should we enter this trade by copying this whale? 
Score: 1-10 (10 = definitely copy)
Reasoning: brief"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Agent 2: Market Analyzer
def agent_market_analyzer():
    prompt = f"""You are a market-safety agent. Is this market safe to trade?

Market: {market['question']}
Price: Yes {market['yes_price']:.2f} | No {market['no_price']:.2f}
Spread: {market['spread']:.3f} (tighter = better)
Volume: ${market['volume_24h']:,}

Is the spread tight enough? Is volume sufficient? Score 1-10 (10 = safe to trade)
Score: 1-10
Reasoning: brief"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Agent 3: Risk Filter
def agent_risk_filter():
    prompt = f"""You are a risk-management agent. Does this trade pass our filters?

Wallet profit per trade: ${top_wallet['profit_per_trade']}
Market spread: {market['spread']:.3f}
Wallet exit discipline: {top_wallet['exit_discipline']*100:.0f}%

Check:
- Is profit/trade high enough to cover spread?
- Can we exit like this whale does?
- Risk/reward favorable?

Score 1-10 (10 = passes all filters)
Score: 1-10
Reasoning: brief"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Run all 3 agents
print("🤖 Agent 1: Whale Copier")
agent1 = agent_whale_copier()
print(agent1)
print("\n" + "="*50 + "\n")

print("🤖 Agent 2: Market Analyzer")
agent2 = agent_market_analyzer()
print(agent2)
print("\n" + "="*50 + "\n")

print("🤖 Agent 3: Risk Filter")
agent3 = agent_risk_filter()
print(agent3)
print("\n" + "="*50 + "\n")

# Consensus: 2/3 agents agree = execute
print("📊 CONSENSUS: If 2+ agents score >5, we TRADE")

# Save results
results = {
    "market": market["question"],
    "wallet": top_wallet["address"],
    "agent_1_whale_copier": agent1,
    "agent_2_market_analyzer": agent2,
    "agent_3_risk_filter": agent3
}

with open("trade_decision.json", "w") as f:
    json.dump(results, f, indent=2)

print("✓ Saved decision to trade_decision.json")
