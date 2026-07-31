"""
inline_eval.py — Run ADK pipeline and evaluate response immediately using DeepEval.

What this does:
  - Runs each query through the full 5-agent pipeline
  - Captures the final Agent 5 recommendation as the output
  - Scores it against the ground truth market data using DeepEval
  - Prints faithfulness and hallucination scores immediately

How to run:
  cd /Users/ayush.rai/ADK
  export OPENAI_API_KEY='your-key-here'
  python3 -m evaluation.inline_eval
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

from STOCK_RESEARCH_TEST.agent import root_agent
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT,
    NVDA_MARKET_SNAPSHOT,
    TSLA_MARKET_SNAPSHOT,
)

# ── Queries and their ground truth sources ──────────────────────────────────

EVAL_CASES = [
    {
        "query":   "analyse APPLE stock based on NASDAQ indicators",
        "ticker":  "AAPL",
        "source":  AAPL_MARKET_SNAPSHOT,
    },
    {
        "query":   "analyse NVIDIA stock can we make it on hold",
        "ticker":  "NVDA",
        "source":  NVDA_MARKET_SNAPSHOT,
    },
    {
        "query":   "analyse tsla stock should i buy or sell",
        "ticker":  "TSLA",
        "source":  TSLA_MARKET_SNAPSHOT,
    },
]


def source_to_context(source_dict: dict) -> list[str]:
    """Convert source dict to list of strings DeepEval expects as context."""
    return [f"{k}: {v}" for k, v in source_dict.items()]


async def run_pipeline(query: str) -> str:
    """Run the full 5-agent pipeline and return Agent 5's final response text."""
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="stock_analysis_pipeline",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="stock_analysis_pipeline",
        user_id="eval_user",
    )

    final_response = ""

    async for event in runner.run_async(
        user_id="eval_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=query)],
        ),
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break

    return final_response


async def evaluate_case(case: dict) -> dict:
    """Run one query and score the response immediately."""
    ticker  = case["ticker"]
    query   = case["query"]
    context = source_to_context(case["source"])

    print(f"\n{'='*60}")
    print(f"Running pipeline for: {ticker}")
    print(f"Query: {query}")
    print("="*60)

    actual_output = await run_pipeline(query)

    if not actual_output:
        print(f"ERROR: No response received for {ticker}")
        return {"ticker": ticker, "error": "no response"}

    print(f"\nAgent 5 Response:\n{actual_output}")

    # Build DeepEval test case
    test_case = LLMTestCase(
        input=query,
        actual_output=actual_output,
        context=context,
        retrieval_context=context,
    )

    # Run metrics
    faithfulness  = FaithfulnessMetric(threshold=0.85, verbose_mode=True)
    hallucination = HallucinationMetric(threshold=0.30, verbose_mode=True)

    faithfulness.measure(test_case)
    hallucination.measure(test_case)

    # Print scores
    print(f"\n--- DeepEval Scores: {ticker} ---")
    print(f"Faithfulness  Score  : {faithfulness.score:.2f}  (pass if >= 0.85)")
    print(f"Faithfulness  Reason : {faithfulness.reason}")
    print(f"Hallucination Score  : {hallucination.score:.2f}  (pass if <= 0.30)")
    print(f"Hallucination Reason : {hallucination.reason}")

    passed = faithfulness.score >= 0.85 and hallucination.score <= 0.30
    print(f"\nOverall Result: {'PASS' if passed else 'FAIL'}")

    if hallucination.score > 0.30:
        print(f"HALLUCINATION DETECTED in {ticker} response")

    return {
        "ticker":        ticker,
        "faithfulness":  faithfulness.score,
        "hallucination": hallucination.score,
        "passed":        passed,
    }


async def main():
    results = []
    for case in EVAL_CASES:
        result = await evaluate_case(case)
        results.append(result)

    # Summary table
    print(f"\n{'='*60}")
    print("BASELINE SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithfulness':>14} {'Hallucination':>15} {'Result':>8}")
    print("-"*60)
    for r in results:
        if "error" in r:
            print(f"{r['ticker']:<8} {'ERROR':>14} {'ERROR':>15} {'FAIL':>8}")
        else:
            result_str = "PASS" if r["passed"] else "FAIL"
            print(f"{r['ticker']:<8} {r['faithfulness']:>14.2f} {r['hallucination']:>15.2f} {result_str:>8}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())