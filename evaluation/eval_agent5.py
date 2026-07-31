"""
eval_agent5.py — DeepEval baseline for Agent 5 (recommendation_agent)

What this tests:
  - Whether the final recommendation is faithful to all upstream agent outputs
  - Confidence type check: Agent 2 emits a numeric score (0.0–1.0);
    Agent 5 must NOT silently convert it to qualitative (LOW/MEDIUM/HIGH)
  - Hallucination against full source context (snapshot + risk + P&L)

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.eval_agent5
"""

import re

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from evaluation.eval_data.agent5_outputs import AAPL_RECOMMENDATION, TSLA_RECOMMENDATION, NVDA_RECOMMENDATION
from evaluation.eval_data.agent1_outputs import AAPL_SNAPSHOT, TSLA_SNAPSHOT, NVDA_SNAPSHOT
from evaluation.eval_data.agent2_outputs import AAPL_DECISION, TSLA_DECISION, NVDA_DECISION
from evaluation.eval_data.agent3_outputs import AAPL_PL, TSLA_PL, NVDA_PL
from evaluation.eval_data.agent4_outputs import AAPL_RISK, TSLA_RISK, NVDA_RISK
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT,
    TSLA_MARKET_SNAPSHOT,
    NVDA_MARKET_SNAPSHOT,
)

CASES = [
    {
        "ticker":             "AAPL",
        "output":             AAPL_RECOMMENDATION,
        "snapshot":           AAPL_SNAPSHOT,
        "decision":           AAPL_DECISION,
        "pl":                 AAPL_PL,
        "risk":               AAPL_RISK,
        "source":             AAPL_MARKET_SNAPSHOT,
        "query":              "analyse APPLE stock based on NASDAQ indicators",
        "agent2_confidence":  "0.6",
    },
    {
        "ticker":             "TSLA",
        "output":             TSLA_RECOMMENDATION,
        "snapshot":           TSLA_SNAPSHOT,
        "decision":           TSLA_DECISION,
        "pl":                 TSLA_PL,
        "risk":               TSLA_RISK,
        "source":             TSLA_MARKET_SNAPSHOT,
        "query":              "analyse tsla stock should i buy or sell",
        "agent2_confidence":  "0.0",
    },
    {
        "ticker":             "NVDA",
        "output":             NVDA_RECOMMENDATION,
        "snapshot":           NVDA_SNAPSHOT,
        "decision":           NVDA_DECISION,
        "pl":                 NVDA_PL,
        "risk":               NVDA_RISK,
        "source":             NVDA_MARKET_SNAPSHOT,
        "query":              "analyse NVIDIA stock can we make it on hold",
        "agent2_confidence":  "0.0",
    },
]

QUALITATIVE_LABELS = {"LOW", "MEDIUM", "HIGH"}


def source_to_context(snapshot, decision, pl, risk, source):
    context = [snapshot, decision, pl, risk]
    context += [f"{k}: {v}" for k, v in source.items()]
    return context


def check_confidence_conversion(output: str, numeric_confidence: str, ticker: str):
    """Flag if Agent 5 replaced the numeric confidence with a qualitative label."""
    # Look for 'Confidence' line in the output
    lines = [l for l in output.splitlines() if "Confidence" in l]
    converted = False
    for line in lines:
        for label in QUALITATIVE_LABELS:
            if label in line and numeric_confidence not in line:
                converted = True
                print(f"  CONFIDENCE CONVERSION FAIL — {ticker}: "
                      f"Agent 2 emitted {numeric_confidence}, Agent 5 shows '{label}'.")
                break

    if not converted:
        has_numeric = re.search(r'\b' + re.escape(numeric_confidence) + r'\b', output)
        if has_numeric:
            print(f"  CONFIDENCE CONVERSION PASS — {ticker}: numeric {numeric_confidence} preserved.")
        else:
            print(f"  CONFIDENCE CHECK INCONCLUSIVE — {ticker}: neither numeric nor known qualitative label found.")


def run():
    results = []

    for case in CASES:
        ticker  = case["ticker"]
        context = source_to_context(
            case["snapshot"], case["decision"], case["pl"], case["risk"], case["source"]
        )

        print(f"\n{'='*60}")
        print(f"Agent 5 | {ticker}")
        print("="*60)
        print(f"Output:\n{case['output']}")

        check_confidence_conversion(case["output"], case["agent2_confidence"], ticker)

        test_case = LLMTestCase(
            input=case["query"],
            actual_output=case["output"],
            context=context,
            retrieval_context=context,
        )

        faithfulness     = FaithfulnessMetric(threshold=0.85, verbose_mode=True)
        hallucination    = HallucinationMetric(threshold=0.30, verbose_mode=True)
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
    print("AGENT 5 SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithful':>10} {'Hallucin':>10} {'Relevancy':>11} {'Result':>8}")
    print("-"*60)
    for r in results:
        print(f"{r['ticker']:<8} {r['faithfulness']:>10.2f} {r['hallucination']:>10.2f} "
              f"{r['answer_relevancy']:>11.2f} {'PASS' if r['passed'] else 'FAIL':>8}")
    print("="*60)

    return results


if __name__ == "__main__":
    run()
