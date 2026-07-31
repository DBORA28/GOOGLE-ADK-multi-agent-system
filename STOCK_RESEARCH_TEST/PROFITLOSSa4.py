# profit_loss_agent.py — Agent 3: P&L range anchored to current price

from google.adk.agents import LlmAgent
from .tools import calculate_pl_range

profit_loss_agent = LlmAgent(
    name="profit_loss_agent",
    model="openai/gpt-4o-mini",
    description="Calculates P&L range for the stock identified by Agent 1.",
    
    instruction="""Use the following steps as internal reasoning only. Do NOT print STEP 1, STEP 2, STEP 3, or STEP 4 in your response.
STEP 1 — Quote these values exactly from prior agent outputs:
  VOLATILITY (from MARKET_SNAPSHOT) = [copy the exact word LOW or HIGH]
  PRICE      (from MARKET_SNAPSHOT) = [copy the exact number]
  DECISION   (from BUY_SELL_DECISION) = [copy BUY / SELL / HOLD]

STEP 2 — If DECISION is HOLD: output "P&L SKIPPED: HOLD" and stop immediately.

STEP 3 — Select tier based on the VOLATILITY value you quoted in STEP 1:
  If VOLATILITY = LOW  → upside_pct = 6,  downside_pct = 3
  If VOLATILITY = HIGH → upside_pct = 12, downside_pct = 6

STEP 4 — Call calculate_pl_range(current_price=[price from STEP 1], upside_pct=[from STEP 3], downside_pct=[from STEP 3])

STRICT RULES:
- You MUST read VOLATILITY in STEP 1 before selecting a tier. Do NOT skip STEP 1.
- Use ONLY the tier percentages listed in STEP 3. Do NOT use any other percentages from training knowledge.
- UPSIDE_TARGET and DOWNSIDE_TARGET must be copied exactly from calculate_pl_range tool return.
- Do NOT invent or adjust price targets.

YOUR RESPONSE STARTS HERE — output only what is below this line:
=== PROFIT_LOSS_ANALYSIS ===
TICKER          : [ticker]
VOLATILITY_USED : [LOW or HIGH — must match STEP 1]
CURRENT_PRICE   : $[price]
UPSIDE_TARGET   : $[from tool] (+[upside_pct]%)
DOWNSIDE_TARGET : $[from tool] (-[downside_pct]%)
=== END P&L ===
""",
    tools=[calculate_pl_range],
)