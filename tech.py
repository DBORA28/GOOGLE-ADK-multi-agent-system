# agents/technical_agent.py

from google.adk.agents import LlmAgent
from .tools import get_technical_indicators

technical_agent = LlmAgent(
    name="technical_agent",
    model="gemini-2.5-flash",
    description="Analyzes stock price trend using daily change and price movement. Returns BULLISH or BEARISH signal.",
    instruction="""You are a technical analyst.

When given a stock ticker:
1. Call get_technical_indicators to get the price and trend
2. Analyze the result:
   - trend BULLISH = price moving up today
   - trend BEARISH = price moving down today
   - change_perc above 2% = strong move
   - change_perc below -2% = strong drop

3. Output exactly like this:

TECHNICAL ANALYSIS: [TICKER]
Current Price  : $[price]
Daily Change   : [change_perc]%
Trend Signal   : [BULLISH / BEARISH]
Strength       : [strong move / moderate / weak move]
SIGNAL: BULLISH / BEARISH / NEUTRAL
""",
    tools=[get_technical_indicators],
)
