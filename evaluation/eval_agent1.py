"""
eval_agent1.py — DeepEval baseline for Agent 1 (market_indicator_agent)

What this tests:
  - Whether Agent 1's market snapshot is faithful to get_market_snapshot tool output
  - Whether Agent 1 hallucinated any field values not present in the tool response

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.eval_agent1
"""

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

from evaluation.eval_data.agent1_outputs import AAPL_SNAPSHOT, TSLA_SNAPSHOT, NVDA_SNAPSHOT
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT,
    TSLA_MARKET_SNAPSHOT,
    NVDA_MARKET_SNAPSHOT,
)

CASES = [
    {"ticker": "AAPL", "output": AAPL_SNAPSHOT, "source": AAPL_MARKET_SNAPSHOT,
     "query": "analyse APPLE stock based on NASDAQ indicators"},
    {"ticker": "TSLA", "output": TSLA_SNAPSHOT, "source": TSLA_MARKET_SNAPSHOT,
     "query": "analyse tsla stock should i buy or sell"},
    {"ticker": "NVDA", "output": NVDA_SNAPSHOT, "source": NVDA_MARKET_SNAPSHOT,
     "query": "analyse NVIDIA stock can we make it on hold"},
]


def source_to_context(d: dict) -> list[str]:
    return [f"{k}: {v}" for k, v in d.items()]


def run():
    results = []

    for case in CASES:
        ticker  = case["ticker"]
        context = source_to_context(case["source"])

        print(f"\n{'='*60}")
        print(f"Agent 1 | {ticker}")
        print("="*60)
        print(f"Output:\n{case['output']}")

        test_case = LLMTestCase(
            input=case["query"],
            actual_output=case["output"],
            context=context,
            retrieval_context=context,
        )

        faithfulness  = FaithfulnessMetric(threshold=0.85, verbose_mode=True)
        hallucination = HallucinationMetric(threshold=0.30, verbose_mode=True)

        faithfulness.measure(test_case)
        hallucination.measure(test_case)

        passed = faithfulness.score >= 0.85 and hallucination.score <= 0.30
        print(f"\nFaithfulness  : {faithfulness.score:.2f}  | Reason: {faithfulness.reason}")
        print(f"Hallucination : {hallucination.score:.2f}  | Reason: {hallucination.reason}")
        print(f"Result        : {'PASS' if passed else 'FAIL'}")

        results.append({
            "ticker":        ticker,
            "faithfulness":  faithfulness.score,
            "hallucination": hallucination.score,
            "passed":        passed,
        })

    print(f"\n{'='*60}")
    print("AGENT 1 SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithfulness':>14} {'Hallucination':>15} {'Result':>8}")
    print("-"*60)
    for r in results:
        print(f"{r['ticker']:<8} {r['faithfulness']:>14.2f} {r['hallucination']:>15.2f} {'PASS' if r['passed'] else 'FAIL':>8}")
    print("="*60)

    return results


if __name__ == "__main__":
    run()
