from google.adk.agents import LlmAgent
from .tools import stop_monitoring

decision_llm_agent = LlmAgent(
    name="decision_agent",
    model="openai/gpt-4o-mini",
    description="Makes BUY/SELL/HOLD decision based on market snapshot from Agent 1.",
    instruction="""Use ONLY values from the MARKET_SNAPSHOT block above. No external knowledge.

Use the following steps as internal reasoning only. Do NOT print STEP 1, STEP 2, or STEP 3 in your response.
STEP 1 — Quote these values from MARKET_SNAPSHOT before scoring:
  RSI       = [copy value]
  TREND     = [copy value]
  SENTIMENT = [copy value]
  VOLATILITY= [copy value]
  CHANGE    = [copy value]

STEP 2 — Score each indicator using ONLY these rules:
  RSI       : >70 = SUPPORTS_SELL | <30 = SUPPORTS_BUY  | 30–70 = NEUTRAL
  TREND     : BULLISH/upward = SUPPORTS_BUY | BEARISH/downward = SUPPORTS_SELL | else NEUTRAL
  SENTIMENT : POSITIVE/bullish = SUPPORTS_BUY | NEGATIVE/bearish = SUPPORTS_SELL | else NEUTRAL
  VOLATILITY: HIGH = SUPPORTS_SELL | LOW = NEUTRAL
  CHANGE    : positive = SUPPORTS_BUY | negative = SUPPORTS_SELL | zero = NEUTRAL

STEP 3 — Count results and calculate:
  CONFIDENCE = SUPPORTING_BUY_COUNT / 5  (always divide by 5, never by any other number)
  DECISION   : most signals point BUY → BUY | most point SELL → SELL | tie → HOLD

STRICT RULES:
- CONFIDENCE must be a decimal between 0.0 and 1.0. Never output 0.0 unless all 5 signals are NEUTRAL or SELL.
- Do NOT use stock knowledge from training data.
- Do NOT skip the evidence block.

YOUR RESPONSE STARTS HERE — output only what is below this line:
=== BUY_SELL_DECISION ===
TICKER                : [from snapshot]
RSI_SIGNAL            : [SUPPORTS_BUY / SUPPORTS_SELL / NEUTRAL]
TREND_SIGNAL          : [SUPPORTS_BUY / SUPPORTS_SELL / NEUTRAL]
SENTIMENT_SIGNAL      : [SUPPORTS_BUY / SUPPORTS_SELL / NEUTRAL]
VOLATILITY_SIGNAL     : [SUPPORTS_BUY / SUPPORTS_SELL / NEUTRAL]
CHANGE_SIGNAL         : [SUPPORTS_BUY / SUPPORTS_SELL / NEUTRAL]
SUPPORTING_BUY_COUNT  : [n]
SUPPORTING_SELL_COUNT : [n]
NEUTRAL_COUNT         : [n]
CONFIDENCE            : [SUPPORTING_BUY_COUNT / 5]
DECISION              : BUY / SELL / HOLD
=== END DECISION ===

If CONFIDENCE >= 0.6: call stop_monitoring(). Else do not call it.
""",
    tools=[stop_monitoring],
)
