# risk_agent — Agent 4: evaluates investment risk using volatility and beta

from google.adk.agents import LlmAgent
from .tools import get_risk_metrics

risk_agent = LlmAgent(
    name="risk_agent",
    model="openai/gpt-4o-mini",
    description="Evaluates investment risk using volatility and beta. Returns LOW, MEDIUM or HIGH risk rating.",
    # instruction="""Read TICKER from MARKET_SNAPSHOT. Call get_risk_metrics(ticker).
    #
    # Rules: beta <1.0 = lower risk | 1.0–1.5 = moderate | >1.5 = higher risk.
    # LOW volatility = stable | HIGH volatility = unpredictable.
    #
    # Output exactly:
    # RISK ASSESSMENT: [TICKER]
    # Volatility : [LOW/HIGH]
    # Beta       : [value] → [interpretation]
    # RISK RATING: LOW / MEDIUM / HIGH
    # """
    # HALLUCINATIONS DETECTED:
    #   1. NVDA: get_risk_metrics tool was NOT called — agent fabricated beta=1.9 from training memory (actual=1.7)
    #   2. AAPL: tool was called but beta reported as 0.8 (actual=1.1) — tool output not copied exactly
    # FIX (combined):
    #   - Injection layer: STEP 1 forces tool call and explicit quoting of raw tool return before any output
    #   - Structure layer: hard MUST rule + copy-exactly constraint on beta value
    instruction="""Use the following steps as internal reasoning only. Do NOT print STEP 1 or STEP 2 in your response.
STEP 1 — Read TICKER from MARKET_SNAPSHOT. Then call get_risk_metrics(ticker) immediately.
          The tool returns: ticker, volatility, beta.
          Note the raw tool return internally: volatility=[copy], beta=[copy]

STEP 2 — Use ONLY the values from STEP 1 tool return to fill the output block.
          Apply these rules to determine interpretation:
          beta < 1.0  → lower risk
          beta 1.0–1.5 → moderate risk
          beta > 1.5  → higher risk

STRICT RULES:
- You MUST call get_risk_metrics(ticker) before writing any values. This is not optional.
- Do NOT use volatility or beta values from your training knowledge, from MARKET_SNAPSHOT, or from any prior agent output.
- The only valid source for volatility and beta is the get_risk_metrics tool return in this step.
- Copy beta exactly as the tool returned it. Do NOT round or adjust the number.
- If get_risk_metrics returns an error: output "RISK ASSESSMENT: ERROR — tool failed" and stop.

YOUR RESPONSE STARTS HERE — output only what is below this line:
RISK ASSESSMENT: [TICKER]
Volatility : [volatility from tool — LOW or HIGH]
Beta       : [beta from tool — exact number] → [interpretation from STEP 2 rules]
RISK RATING: [LOW if beta<1.0 and LOW vol | HIGH if beta>1.5 or HIGH vol | MEDIUM otherwise]
""",
    tools=[get_risk_metrics],
)
