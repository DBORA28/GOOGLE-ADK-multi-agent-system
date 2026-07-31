# agent.py — ADK entry point and full workflow pipeline

from google.adk.agents import Agent
from .market_indicatorA1 import market_indicator_agent
from .decsionmakerA2 import decision_llm_agent
from .PROFITLOSSa4 import profit_loss_agent
from .risk3 import risk_agent
from .recommend5 import recommendation_agent

decision_loop = Agent(
    name="decision_loop",
    description="Retries buy/sell decision until confidence threshold is met.",
    sub_agents=[decision_llm_agent],
    max_iterations=1,
)

root_agent = Agent(
    name="stock_analysis_pipeline",
    description="Full stock analysis for AAPL, NVDA, or TSLA: indicators → decision → P&L → risk → recommendation.",
    sub_agents=[
        market_indicator_agent,
        decision_loop,
        profit_loss_agent,
        risk_agent,
        recommendation_agent,
    ],
)
#async_execution= false.  if true all agents run in parallel (and root_agent returns when all sub-agents complete. if false, agents run sequentially and root_agent returns final output of last agent.)
