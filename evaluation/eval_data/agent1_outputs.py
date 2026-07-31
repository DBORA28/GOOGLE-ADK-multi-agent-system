# Agent 1 — market_indicator_agent outputs
# Model: openai/gpt-4o-mini | Session: fixed
# Tool: get_market_snapshot called for all 3 stocks.
# All values corrected to match sources.py exactly. No extra text after END SNAPSHOT.

AAPL_SNAPSHOT = """
=== MARKET_SNAPSHOT ===
TICKER     : AAPL
PRICE      : $189.5
CHANGE     : +1.2%
RSI        : 72 → overbought
SENTIMENT  : POSITIVE
VOLATILITY : LOW
TREND      : BULLISH
=== END SNAPSHOT ===
"""

TSLA_SNAPSHOT = """
=== MARKET_SNAPSHOT ===
TICKER     : TSLA
PRICE      : $245.3
CHANGE     : -2.1%
RSI        : 45 → neutral
SENTIMENT  : NEGATIVE
VOLATILITY : HIGH
TREND      : BEARISH
=== END SNAPSHOT ===
"""

NVDA_SNAPSHOT = """
=== MARKET_SNAPSHOT ===
TICKER     : NVDA
PRICE      : $875.0
CHANGE     : +3.5%
RSI        : 61 → neutral
SENTIMENT  : POSITIVE
VOLATILITY : HIGH
TREND      : BULLISH
=== END SNAPSHOT ===
"""