"""
eval_agent3.py — DeepEval baseline for Agent 3 (profit_loss_agent)

What this tests:
  - Whether P&L percentages match the correct volatility tier from sources.py
  - LOW volatility  → upside 6%,  downside 3%
  - HIGH volatility → upside 12%, downside 6%
  - HOLD decision   → P&L must be skipped (no calculate_pl_range call)

Custom arithmetic check flags the AAPL case where Agent 3 applied 12% to a LOW vol stock.

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.eval_agent3
"""

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

from evaluation.eval_data.agent3_outputs import AAPL_PL, TSLA_PL, NVDA_PL
from evaluation.eval_data.agent1_outputs import AAPL_SNAPSHOT, TSLA_SNAPSHOT, NVDA_SNAPSHOT
from evaluation.eval_data.agent2_outputs import AAPL_DECISION, TSLA_DECISION, NVDA_DECISION
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT,
    TSLA_MARKET_SNAPSHOT,
    NVDA_MARKET_SNAPSHOT,
)

VOLATILITY_UPSIDE = {"LOW": 6.0, "HIGH": 12.0}
VOLATILITY_DOWNSIDE = {"LOW": 3.0, "HIGH": 6.0}

CASES = [
    {
        "ticker":   "AAPL",
        "output":   AAPL_PL,
        "decision": AAPL_DECISION,
        "snapshot": AAPL_SNAPSHOT,
        "source":   AAPL_MARKET_SNAPSHOT,
        "query":    "analyse APPLE stock based on NASDAQ indicators",
        "skipped":  False,
    },
    {
        "ticker":   "TSLA",
        "output":   TSLA_PL,
        "decision": TSLA_DECISION,
        "snapshot": TSLA_SNAPSHOT,
        "source":   TSLA_MARKET_SNAPSHOT,
        "query":    "analyse tsla stock should i buy or sell",
        "skipped":  False,
    },
    {
        "ticker":   "NVDA",
        "output":   NVDA_PL,
        "decision": NVDA_DECISION,
        "snapshot": NVDA_SNAPSHOT,
        "source":   NVDA_MARKET_SNAPSHOT,
        "query":    "analyse NVIDIA stock can we make it on hold",
        "skipped":  True,
    },
]


def source_to_context(snapshot: str, decision: str, source: dict) -> list[str]:
    context = [snapshot, decision]
    context += [f"{k}: {v}" for k, v in source.items()]
    return context


def check_pl_arithmetic(output: str, source: dict, ticker: str, skipped: bool):
    if skipped:
        if "SKIPPED" in output.upper() or "N/A" in output.upper():
            print(f"  P&L SKIP CHECK PASS — {ticker}: correctly skipped for HOLD.")
        else:
            print(f"  P&L SKIP CHECK FAIL — {ticker}: expected skip but got P&L output.")
        return

    volatility = source.get("volatility", "")
    expected_upside   = VOLATILITY_UPSIDE.get(volatility)
    expected_downside = VOLATILITY_DOWNSIDE.get(volatility)

    if expected_upside is None:
        print(f"  P&L ARITHMETIC — {ticker}: unknown volatility '{volatility}', skipping check.")
        return

    upside_ok   = f"{expected_upside}%" in output
    downside_ok = f"{expected_downside}%" in output

    if upside_ok and downside_ok:
        print(f"  P&L ARITHMETIC PASS — {ticker}: correct {expected_upside}%/{expected_downside}% for {volatility} volatility.")
    else:
        actual_pct = [p for p in ["6%", "12%", "3%"] if p in output]
        print(f"  P&L ARITHMETIC FAIL — {ticker}: expected {expected_upside}%/{expected_downside}% "
              f"for {volatility} volatility, found {actual_pct} in output.")


def run():
    results = []

    for case in CASES:
        ticker  = case["ticker"]
        context = source_to_context(case["snapshot"], case["decision"], case["source"])

        print(f"\n{'='*60}")
        print(f"Agent 3 | {ticker}")
        print("="*60)
        print(f"Output:\n{case['output']}")

        check_pl_arithmetic(case["output"], case["source"], ticker, case["skipped"])

        if case["skipped"]:
            print(f"  DeepEval skipped — HOLD path has no P&L to score.")
            results.append({"ticker": ticker, "faithfulness": None, "hallucination": None, "passed": True})
            continue

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
    print("AGENT 3 SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithfulness':>14} {'Hallucination':>15} {'Result':>8}")
    print("-"*60)
    for r in results:
        f_str = f"{r['faithfulness']:.2f}" if r["faithfulness"] is not None else "  N/A"
        h_str = f"{r['hallucination']:.2f}" if r["hallucination"] is not None else "  N/A"
        print(f"{r['ticker']:<8} {f_str:>14} {h_str:>15} {'PASS' if r['passed'] else 'FAIL':>8}")
    print("="*60)

    return results


if __name__ == "__main__":
    run()
