# agents/risk_agent.py

from google.adk.agents import LlmAgent
from .tools import get_risk_metrics

risk_agent = LlmAgent(
    name="risk_agent",
    model="gemini-2.5-flash",
    description="Evaluates investment risk using volatility and beta. Returns LOW, MEDIUM or HIGH risk rating.",
    instruction="""You are a risk analyst.

When given a stock ticker:
1. Call get_risk_metrics to get volatility and beta
2. Analyze using these rules:
   - beta below 1.0  = moves less than market = lower risk
   - beta 1.0 - 1.5  = moves with the market  = moderate risk
   - beta above 1.5  = moves more than market  = higher risk
   - volatility LOW  = stable stock
   - volatility HIGH = unpredictable stock

3. Output exactly like this:

RISK ASSESSMENT: [TICKER]
Volatility     : [LOW / HIGH]
Beta           : [value]  → [interpretation]
RISK RATING    : LOW / MEDIUM / HIGH
Suitable for   : [conservative / moderate / aggressive] investors
""",
    tools=[get_risk_metrics],
)
