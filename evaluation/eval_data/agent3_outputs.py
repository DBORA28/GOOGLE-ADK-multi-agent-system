# Agent 3 — profit_loss_agent outputs
# Model: openai/gpt-4o-mini | Session: fixed
# Tool: calculate_pl_range called for AAPL (BUY) and TSLA (SELL) and NVDA (BUY).
#
# AAPL: LOW volatility → upside 6%, downside 3%
#       $189.5 × 1.06 = $200.87 | $189.5 × 0.97 = $183.82
# TSLA: HIGH volatility → upside 12%, downside 6% (correct, unchanged)
#       $245.3 × 1.12 = $274.74 | $245.3 × 0.94 = $230.58
# NVDA: HIGH volatility → upside 12%, downside 6% (now BUY, no longer skipped)
#       $875.0 × 1.12 = $980.0  | $875.0 × 0.94 = $822.5

AAPL_PL = """
=== PROFIT_LOSS_ANALYSIS ===
TICKER     : AAPL
DECISION   : BUY
ENTRY      : $189.5
UPSIDE     : 6%   → Target: $200.87
DOWNSIDE   : 3%   → Stop:   $183.82
=== END PL ===
"""

TSLA_PL = """
=== PROFIT_LOSS_ANALYSIS ===
TICKER     : TSLA
DECISION   : SELL
ENTRY      : $245.3
UPSIDE     : 12%  → Target: $274.74
DOWNSIDE   : 6%   → Stop:   $230.58
=== END PL ===
"""

NVDA_PL = """
=== PROFIT_LOSS_ANALYSIS ===
TICKER     : NVDA
DECISION   : BUY
ENTRY      : $875.0
UPSIDE     : 12%  → Target: $980.0
DOWNSIDE   : 6%   → Stop:   $822.5
=== END PL ===
"""