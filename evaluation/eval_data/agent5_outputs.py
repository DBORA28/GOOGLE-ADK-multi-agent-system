# Agent 5 — recommendation_agent outputs
# Model: openai/gpt-4o-mini | Session: fixed
# Agent 5 has no tools — reads only from prior conversation context.
# All hallucinations corrected:
# - Confidence preserved as numeric (from Agent 2) — not converted to qualitative
# - Trend, Decision, P&L targets inherited correctly from fixed upstream agents

# AAPL: Trend BULLISH, Decision BUY (0.6), P&L from 6%/3% (LOW vol), beta 1.1
AAPL_RECOMMENDATION = """
INVESTMENT RECOMMENDATION: AAPL
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : MEDIUM
P&L Upside     : $200.87
P&L Downside   : $183.82

FINAL DECISION : BUY
Confidence     : 0.6
Reason         : AAPL shows bullish trend with positive sentiment and +1.2% change. RSI at 72 indicates overbought conditions but 3 of 5 indicators support a buy. Low volatility and beta of 1.1 indicate moderate risk.
"""

# TSLA: Trend BEARISH, Decision SELL (0.0), P&L from 12%/6% (HIGH vol), beta 2.3
TSLA_RECOMMENDATION = """
INVESTMENT RECOMMENDATION: TSLA
Market Trend   : BEARISH
Decision       : SELL
Confidence     : 0.0
Risk Level     : HIGH
P&L Upside     : $274.74
P&L Downside   : $230.58

FINAL DECISION : SELL
Confidence     : 0.0
Reason         : TSLA shows bearish trend with negative sentiment and -2.1% change. Zero buy indicators detected across all 5 signals. High volatility and beta of 2.3 confirm elevated risk.
"""

# NVDA: Trend BULLISH, Decision BUY (0.6), P&L from 12%/6% (HIGH vol), beta 1.7
NVDA_RECOMMENDATION = """
INVESTMENT RECOMMENDATION: NVDA
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : HIGH
P&L Upside     : $980.0
P&L Downside   : $822.5

FINAL DECISION : BUY
Confidence     : 0.6
Reason         : NVDA shows bullish trend with positive sentiment and +3.5% change. 3 of 5 indicators support a buy. High volatility (beta=1.7) is a risk factor but confidence threshold is met.
"""