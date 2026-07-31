# Agent 2 — decision_llm_agent outputs
# Model: openai/gpt-4o-mini | Session: fixed
# Tool: stop_monitoring called for all 3 stocks.
# All count fields present. Confidence derived from indicator counts.
#
# AAPL: RSI overbought=SELL(1), TREND BULLISH=BUY(1), SENTIMENT POSITIVE=BUY(1),
#       VOLATILITY LOW=NEUTRAL(1), CHANGE +1.2%=BUY(1) → buy:3 sell:1 neutral:1 → 3/5=0.6 → BUY
# TSLA: RSI neutral=NEUTRAL(1), TREND BEARISH=SELL(1), SENTIMENT NEGATIVE=SELL(1),
#       VOLATILITY HIGH=SELL(1), CHANGE -2.1%=SELL(1) → buy:0 sell:4 neutral:1 → 0/5=0.0 → SELL
# NVDA: RSI neutral=NEUTRAL(1), TREND BULLISH=BUY(1), SENTIMENT POSITIVE=BUY(1),
#       VOLATILITY HIGH=SELL(1), CHANGE +3.5%=BUY(1) → buy:3 sell:1 neutral:1 → 3/5=0.6 → BUY

AAPL_DECISION = """
=== BUY_SELL_DECISION ===
TICKER               : AAPL
EVIDENCE_CITED       : RSI, TREND, SENTIMENT, VOLATILITY, CHANGE
SUPPORTING_BUY_COUNT : 3
SUPPORTING_SELL_COUNT: 1
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.6
DECISION             : BUY
=== END DECISION ===
"""

TSLA_DECISION = """
=== BUY_SELL_DECISION ===
TICKER               : TSLA
EVIDENCE_CITED       : RSI, TREND, SENTIMENT, VOLATILITY, CHANGE
SUPPORTING_BUY_COUNT : 0
SUPPORTING_SELL_COUNT: 4
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.0
DECISION             : SELL
=== END DECISION ===
"""

NVDA_DECISION = """
=== BUY_SELL_DECISION ===
TICKER               : NVDA
EVIDENCE_CITED       : RSI, TREND, SENTIMENT, VOLATILITY, CHANGE
SUPPORTING_BUY_COUNT : 3
SUPPORTING_SELL_COUNT: 1
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.6
DECISION             : BUY
=== END DECISION ===
"""