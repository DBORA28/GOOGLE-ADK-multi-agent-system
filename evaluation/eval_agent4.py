"""
eval_agent4.py — DeepEval baseline for Agent 4 (risk_agent)

What this tests:
  - Whether risk assessment values match get_risk_metrics tool output (sources.py)
  - Tool-call verification flag: NVDA output was produced WITHOUT a tool call —
    the fabrication is flagged before DeepEval even runs.

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.eval_agent4
"""

from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

from evaluation.eval_data.agent4_outputs import AAPL_RISK, TSLA_RISK, NVDA_RISK
from evaluation.eval_data.agent1_outputs import AAPL_SNAPSHOT, TSLA_SNAPSHOT, NVDA_SNAPSHOT
from evaluation.eval_data.sources import (
    AAPL_MARKET_SNAPSHOT, AAPL_RISK_METRICS,
    TSLA_MARKET_SNAPSHOT, TSLA_RISK_METRICS,
    NVDA_MARKET_SNAPSHOT, NVDA_RISK_METRICS,
)

CASES = [
    {
        "ticker":        "AAPL",
        "output":        AAPL_RISK,
        "snapshot":      AAPL_SNAPSHOT,
        "source":        AAPL_MARKET_SNAPSHOT,
        "risk_source":   AAPL_RISK_METRICS,
        "query":         "analyse APPLE stock based on NASDAQ indicators",
        "tool_called":   True,
    },
    {
        "ticker":        "TSLA",
        "output":        TSLA_RISK,
        "snapshot":      TSLA_SNAPSHOT,
        "source":        TSLA_MARKET_SNAPSHOT,
        "risk_source":   TSLA_RISK_METRICS,
        "query":         "analyse tsla stock should i buy or sell",
        "tool_called":   True,
    },
    {
        "ticker":        "NVDA",
        "output":        NVDA_RISK,
        "snapshot":      NVDA_SNAPSHOT,
        "source":        NVDA_MARKET_SNAPSHOT,
        "risk_source":   NVDA_RISK_METRICS,
        "query":         "analyse NVIDIA stock can we make it on hold",
        "tool_called":   True,   # fixed: get_risk_metrics now called in trace
    },
]


def source_to_context(snapshot: str, source: dict, risk: dict) -> list[str]:
    context = [snapshot]
    context += [f"{k}: {v}" for k, v in source.items()]
    context += [f"{k}: {v}" for k, v in risk.items()]
    return context


def check_tool_call(tool_called: bool, ticker: str):
    if not tool_called:
        print(f"  !! TOOL-CALL FABRICATION — {ticker}: get_risk_metrics was NOT called.")
        print(f"     Agent 4 generated risk values from parametric knowledge (no tool grounding).")
        print(f"     Values may match by coincidence — this is still ungrounded generation.")
    else:
        print(f"  TOOL-CALL CHECK PASS — {ticker}: get_risk_metrics was called.")


def run():
    results = []

    for case in CASES:
        ticker  = case["ticker"]
        context = source_to_context(case["snapshot"], case["source"], case["risk_source"])

        print(f"\n{'='*60}")
        print(f"Agent 4 | {ticker}")
        print("="*60)
        print(f"Output:\n{case['output']}")

        check_tool_call(case["tool_called"], ticker)

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

        # For NVDA: even if scores look OK (values match by coincidence), tool not called = FAIL
        tool_ok = case["tool_called"]
        passed  = faithfulness.score >= 0.85 and hallucination.score <= 0.30 and tool_ok

        print(f"\nFaithfulness  : {faithfulness.score:.2f}  | Reason: {faithfulness.reason}")
        print(f"Hallucination : {hallucination.score:.2f}  | Reason: {hallucination.reason}")
        print(f"Tool Called   : {'YES' if tool_ok else 'NO  ← FAIL override'}")
        print(f"Result        : {'PASS' if passed else 'FAIL'}")

        results.append({
            "ticker":        ticker,
            "faithfulness":  faithfulness.score,
            "hallucination": hallucination.score,
            "tool_called":   tool_ok,
            "passed":        passed,
        })

    print(f"\n{'='*60}")
    print("AGENT 4 SUMMARY")
    print("="*60)
    print(f"{'Ticker':<8} {'Faithful':>10} {'Hallucin':>10} {'ToolCall':>10} {'Result':>8}")
    print("-"*60)
    for r in results:
        print(f"{r['ticker']:<8} {r['faithfulness']:>10.2f} {r['hallucination']:>10.2f} "
              f"{'YES' if r['tool_called'] else 'NO':>10} {'PASS' if r['passed'] else 'FAIL':>8}")
    print("="*60)

    return results


if __name__ == "__main__":
    run()
