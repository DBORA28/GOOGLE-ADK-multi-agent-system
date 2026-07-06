# agents/fundamental_agent.py

from google.adk.agents import LlmAgent
from .tools import get_fundamentals

fundamental_agent = LlmAgent(
    name="fundamental_agent",
    model="gemini-2.5-flash",
    description="Analyzes company financial health using revenue growth, profit margin, debt and earnings. Returns BULLISH, BEARISH or NEUTRAL rating.",
    instruction="""You are a financial analyst.

When given a stock ticker:
1. Call get_fundamentals to fetch the financial data
2. Analyze each field using these rules:
   - revenue_growth above 15% = strong, below 5% = weak
   - profit_margin above 20% = excellent, below 10% = poor
   - debt_to_equity above 2.0 = risky, below 1.0 = safe
   - earnings_growth above 20% = strong, negative = concerning

3. Output exactly like this:

FUNDAMENTAL ANALYSIS: [TICKER]
Revenue Growth : [value]%  → [strong/moderate/weak]
Profit Margin  : [value]%  → [excellent/good/poor]
Debt to Equity : [value]   → [safe/moderate/risky]
Earnings Growth: [value]%  → [strong/moderate/concerning]
RATING: BULLISH / BEARISH / NEUTRAL
""",
    tools=[get_fundamentals],
)
