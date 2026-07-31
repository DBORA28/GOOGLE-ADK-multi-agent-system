# price_monitor.py  —  LoopAgent for price alert monitoring

from google.adk.agents import LoopAgent, LlmAgent
from .tools import check_price_alert, stop_monitoring

# This LlmAgent runs INSIDE the loop on every iteration.
# It checks the price, reports the result, and calls stop_monitoring() to end
# the loop early when the alert fires.
price_checker_agent = LlmAgent(
    name="price_checker",
    model="gemini-2.5-flash",
    description="Checks if a stock price has dropped below a threshold and reports the result.",
    instruction="""You are a price alert monitor.

You will be given a stock ticker and a threshold price.

On each check:
1. Call check_price_alert(ticker, threshold_price) to get the current price status.

2. If alert_triggered is True:
   - Output exactly:
     PRICE ALERT FIRED
     Ticker         : [ticker]
     Current Price  : $[current_price]
     Threshold      : $[threshold]
     Status         : PRICE HAS DROPPED BELOW THRESHOLD
   - Then call stop_monitoring() to end the monitoring loop.

3. If alert_triggered is False:
   - Output exactly:
     CHECK COMPLETE
     Ticker         : [ticker]
     Current Price  : $[current_price]
     Threshold      : $[threshold]
     Status         : Price still above threshold. Watching...
   - Do NOT call stop_monitoring().
""",
    tools=[check_price_alert, stop_monitoring],
)

# LoopAgent wraps the price_checker_agent.
# It runs it up to max_iterations times.
# It stops early if price_checker_agent calls stop_monitoring() and escalates.
price_monitor_agent = LoopAgent(
    name="price_monitor",
    description="Monitors a stock price on repeat and alerts when it drops below a given threshold.",
    sub_agents=[price_checker_agent],
    max_iterations=3,
)
