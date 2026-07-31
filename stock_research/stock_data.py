# agents/stock_data_agent.py

from google.adk.agents import LlmAgent
from .tools import get_stock_price, get_stock_news

stock_data_agent = LlmAgent(
    name="stock_data_agent",
    model="gemini-2.5-flash",
    description="Fetches current stock price, volume, and latest news for a given ticker.",
    instruction="""You are a stock data specialist.

When given a stock ticker:
1. Call get_stock_price to get the price and volume
2. Call get_stock_news to get the latest news headlines
3. Summarize the result like this:

STOCK DATA: [TICKER]
Price     : $[price]  ([change_perc]% today)
Volume    : [volume] shares traded
News      : [headline 1] | [headline 2]
""",
    tools=[get_stock_price, get_stock_news],
)
