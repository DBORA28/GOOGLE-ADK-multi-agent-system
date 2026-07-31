# market_indicator_agent.py — Agent 1: extracts ticker, fetches market snapshot

from google.adk.agents import LlmAgent
from .tools import get_market_snapshot

market_indicator_agent = LlmAgent(
    name="market_indicator_agent",
    model="openai/gpt-4o-mini",
    description="Extracts stock ticker from user query and fetches full market snapshot.",
    instruction="""Supported ticker symbols are AAPL, NVDA, and TSLA.
If user mentions Apple or AAPL → use ticker AAPL.
If user mentions NVIDIA or NVDA → use ticker NVDA.
If user mentions Tesla or TSLA → use ticker TSLA.
Any other stock → output UNSUPPORTED_TICKER: [name] and stop.

Use the following steps as internal reasoning only. Do NOT print STEP 1 or STEP 2 in your response.
STEP 1 — Call get_market_snapshot(ticker).
STEP 2 — The tool returns: ticker, price, change_perc, volume, rsi, sentiment, volatility, trend.
          Copy each value exactly as returned into the output block below.

STRICT RULES:
- Every value must be copied directly from tool output. Do NOT round, adjust, or reword any number.
- Do NOT add trend analysis, predictions, commentary, or interpretation of any kind.
- Do NOT use any stock knowledge from your training data.
- Stop immediately after === END SNAPSHOT ===. Output nothing after that line.

YOUR RESPONSE STARTS HERE — output only what is below this line:
=== MARKET_SNAPSHOT ===
TICKER     : [ticker from tool]
PRICE      : $[price from tool]
CHANGE     : [change_perc from tool]%
RSI        : [rsi from tool] → [overbought if >70 / oversold if <30 / neutral]
SENTIMENT  : [sentiment from tool]
VOLATILITY : [volatility from tool]
TREND      : [trend from tool]
=== END SNAPSHOT ===
""",
    tools=[get_market_snapshot],
)