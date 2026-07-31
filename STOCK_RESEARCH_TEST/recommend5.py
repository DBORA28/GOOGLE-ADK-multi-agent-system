# recommendation_agent — Agent 5: final synthesis and investment recommendation

from google.adk.agents import LlmAgent

recommendation_agent = LlmAgent(
    name="recommendation_agent",
    model="openai/gpt-4o-mini",
    description="Reads all analysis from other agents and gives a final BUY, SELL or HOLD recommendation.",
   
    instruction="""Use the following steps as internal reasoning only. Do NOT print STEP 1 or STEP 2 in your response.
STEP 1 — Internally note these values from prior agent outputs before writing anything:
  TICKER        (from MARKET_SNAPSHOT)      = [copy]
  TREND         (from MARKET_SNAPSHOT)      = [copy]
  DECISION      (from BUY_SELL_DECISION)    = [copy]
  CONFIDENCE    (from BUY_SELL_DECISION)    = [copy — this is a decimal number like 0.6 or 0.4]
  RISK RATING   (from RISK ASSESSMENT)      = [copy]
  UPSIDE_TARGET (from PROFIT_LOSS or N/A)   = [copy]
  DOWNSIDE_TARGET (from PROFIT_LOSS or N/A) = [copy]

STEP 2 — Fill the output block using ONLY the values noted in STEP 1.

STRICT RULES:
- CONFIDENCE must be copied as the exact decimal number from BUY_SELL_DECISION. Do NOT convert to words.
- Do NOT write HIGH, MEDIUM, or LOW for confidence anywhere in the output.
- Do NOT call any tools.
- Do NOT add analysis, predictions, or commentary beyond what prior agents provided.
- Reason must reference only values from STEP 1 — no external knowledge.

YOUR RESPONSE STARTS HERE — output only what is below this line:
INVESTMENT RECOMMENDATION: [TICKER]
Market Trend   : [TREND from STEP 1]
Decision       : [DECISION from STEP 1]
Confidence     : [CONFIDENCE decimal from STEP 1 — e.g. 0.6]
Risk Level     : [RISK RATING from STEP 1]
P&L Upside     : [UPSIDE_TARGET from STEP 1 or N/A]
P&L Downside   : [DOWNSIDE_TARGET from STEP 1 or N/A]

FINAL DECISION : [DECISION from STEP 1]
Confidence     : [CONFIDENCE decimal from STEP 1 — copy the number, do not convert to a word]
Reason         : [2 sentences using only values from STEP 1]
""",
    tools=[],
)
