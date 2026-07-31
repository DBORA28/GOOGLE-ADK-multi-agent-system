# Agent 4 — risk_agent outputs
# Model: openai/gpt-4o-mini | Session: fixed
# Tool: get_risk_metrics called for all 3 stocks.
#
# AAPL: beta corrected from 0.8 → 1.1 (sources.py: beta: 1.1) → moderate risk
# TSLA: unchanged — beta 2.3, HIGH volatility, HIGH risk (was already correct)
# NVDA: tool NOW called (was fabricated before). beta corrected 1.9 → 1.7 (sources.py: beta: 1.7)

AAPL_RISK = """
RISK ASSESSMENT: AAPL
Volatility : LOW
Beta       : 1.1  → moderate risk

RISK RATING: MEDIUM
"""

TSLA_RISK = """
RISK ASSESSMENT: TSLA
Volatility : HIGH
Beta       : 2.3  → higher risk

RISK RATING: HIGH
"""

NVDA_RISK = """
RISK ASSESSMENT: NVDA
Volatility : HIGH
Beta       : 1.7  → higher risk

RISK RATING: HIGH
"""