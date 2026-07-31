"""
eval_agent2.py — DeepEval baseline for Agent 2 (decision_llm_agent)

What this tests:
  - Whether Agent 2's BUY/SELL/HOLD decision is faithful to the market snapshot context
  - Arithmetic check: confidence score should be derivable from indicator counts
    (EVIDENCE_CITED, SUPPORTING_BUY_COUNT, etc.) — missing fields are flagged separately

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.eval_agent2
"""

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from evaluation.eval_data.agent2_outputs import AAPL_DECISION, TSLA_DECISION, NVDA_DECISION
from evaluation.eval_data.agent1_outputs import AAPL_SNAPSHOT, TSLA_SNAPSHOT, NVDA_SNAPSHOT
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT,
    TSLA_MARKET_SNAPSHOT,
    NVDA_MARKET_SNAPSHOT,
)

CASES = [
    {"ticker": "AAPL", "output": AAPL_DECISION, "snapshot": AAPL_SNAPSHOT,
     "source": AAPL_MARKET_SNAPSHOT, "query": "analyse APPLE stock based on NASDAQ indicators"},
    {"ticker": "TSLA", "output": TSLA_DECISION, "snapshot": TSLA_SNAPSHOT,
     "source": TSLA_MARKET_SNAPSHOT, "query": "analyse tsla stock should i buy or sell"},
    {"ticker": "NVDA", "output": NVDA_DECISION, "snapshot": NVDA_SNAPSHOT,
     "source": NVDA_MARKET_SNAPSHOT, "query": "analyse NVIDIA stock can we make it on hold"},
]

REQUIRED_FIELDS = ["EVIDENCE_CITED", "SUPPORTING_BUY_COUNT", "SUPPORTING_SELL_COUNT", "NEUTRAL_COUNT"]


def source_to_context(snapshot: str, source: dict) -> list[str]:
    context = [snapshot]
    context += [f"{k}: {v}" for k, v in source.items()]
    return context


def check_arithmetic(output: str, ticker: str):
    """Flag missing fields that make confidence arithmetic unverifiable."""
    missing = [f for f in REQUIRED_FIELDS if f not in output]
    if missing:
        print(f"  ARITHMETIC CHECK FAIL — {ticker}: missing fields: {missing}")
        print(f"  Confidence score cannot be verified without indicator counts.")
    else:
        print(f"  ARITHMETIC CHECK PASS — {ticker}: all required fields present.")


def run():
    results = []

    for case in CASES:
        ticker  = case["ticker"]
        context = source_to_context(case["snapshot"], case["source"])

        print(f"\n{'='*60}")
        print(f"Agent 2 | {ticker}")
        print("="*60)
        print(f"Output:\n{case['output']}")

        check_arithmetic(case["output"], ticker)

        test_case = LLMTestCase(
            input=case["query"],
            actual_output=case["output"],
            context=context,
            retrieval_context=context,
        )

        faithfulness    = FaithfulnessMetric(threshold=0.85, verbose_mode=True)
        hallucination   = HallucinationMetric(threshold=0.30, verbose_mode=True)
        answer_relevancy = AnswerRelevancyMetric(threshold=0.70, verbose_mode=True)

        faithfulness.measure(test_case)
        hallucination.measure(test_case)
        answer_relevancy.measure(test_case)

        passed = (
            faithfulness.score >= 0.85
            and hallucination.score <= 0.30
            and answer_relevancy.score >= 0.70
        )

        print(f"\nFaithfulness    : {faithfulness.score:.2f}  | Reason: {faithfulness.reason}")
        print(f"Hallucination   : {hallucination.score:.2f}  | Reason: {hallucination.reason}")
        print(f"Answer Relevancy: {answer_relevancy.score:.2f}  | Reason: {answer_relevancy.reason}")
        print(f"Result          : {'PASS' if passed else 'FAIL'}")

        results.append({
            "ticker":           ticker,
            "faithfulness":     faithfulness.score,
            "hallucination":    hallucination.score,
            "answer_relevancy": answer_relevancy.score,
            "passed":           passed,
        })

    print(f"\n{'='*60}")
    print("AGENT 2 SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithful':>10} {'Hallucin':>10} {'Relevancy':>11} {'Result':>8}")
    print("-"*60)
    for r in results:
        print(f"{r['ticker']:<8} {r['faithfulness']:>10.2f} {r['hallucination']:>10.2f} {r['answer_relevancy']:>11.2f} {'PASS' if r['passed'] else 'FAIL':>8}")
    print("="*60)

    return results


if __name__ == "__main__":
    run()
