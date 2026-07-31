"""
run_baseline.py — Run all 5 agent evals and write results/baseline_scores.md

How to run:
  cd /Users/ayush.rai/ADK
  python3 -m evaluation.run_baseline
"""

import asyncio
import datetime

from evaluation.eval_agent1 import run as run_a1
from evaluation.eval_agent2 import run as run_a2
from evaluation.eval_agent3 import run as run_a3
from evaluation.eval_agent4 import run as run_a4
from evaluation.eval_agent5 import run as run_a5

AGENT_RUNNERS = [
    ("Agent 1 — market_indicator_agent",  run_a1),
    ("Agent 2 — decision_llm_agent",      run_a2),
    ("Agent 3 — profit_loss_agent",       run_a3),
    ("Agent 4 — risk_agent",              run_a4),
    ("Agent 5 — recommendation_agent",    run_a5),
]


def format_score(v):
    if v is None:
        return "N/A"
    return f"{v:.2f}"


def write_baseline_md(all_results: dict):
    lines = [
        "# Baseline Evaluation Scores",
        f"",
        f"Run date : {datetime.date.today()}",
        f"Model    : openai/gpt-4o-mini",
        f"Session  : f175f729 (ADK session.db)",
        f"",
    ]

    for agent_name, results in all_results.items():
        lines.append(f"## {agent_name}")
        lines.append("")

        has_relevancy = any("answer_relevancy" in r for r in results)
        has_tool      = any("tool_called" in r for r in results)

        if has_tool:
            lines.append(f"| Ticker | Faithfulness | Hallucination | ToolCalled | Result |")
            lines.append(f"|--------|-------------|--------------|------------|--------|")
            for r in results:
                tool = "YES" if r.get("tool_called") else "NO"
                lines.append(
                    f"| {r['ticker']} | {format_score(r.get('faithfulness'))} "
                    f"| {format_score(r.get('hallucination'))} | {tool} "
                    f"| {'PASS' if r['passed'] else 'FAIL'} |"
                )
        elif has_relevancy:
            lines.append(f"| Ticker | Faithfulness | Hallucination | Relevancy | Result |")
            lines.append(f"|--------|-------------|--------------|-----------|--------|")
            for r in results:
                lines.append(
                    f"| {r['ticker']} | {format_score(r.get('faithfulness'))} "
                    f"| {format_score(r.get('hallucination'))} "
                    f"| {format_score(r.get('answer_relevancy'))} "
                    f"| {'PASS' if r['passed'] else 'FAIL'} |"
                )
        else:
            lines.append(f"| Ticker | Faithfulness | Hallucination | Result |")
            lines.append(f"|--------|-------------|--------------|--------|")
            for r in results:
                lines.append(
                    f"| {r['ticker']} | {format_score(r.get('faithfulness'))} "
                    f"| {format_score(r.get('hallucination'))} "
                    f"| {'PASS' if r['passed'] else 'FAIL'} |"
                )

        lines.append("")

    lines += [
        "## Known Hallucinations (pre-fix baseline)",
        "",
        "| # | Agent | Ticker | Type | Description |",
        "|---|-------|--------|------|-------------|",
        "| 1 | A1 | TSLA, NVDA | Format violation | Extra markdown text appended after `=== END SNAPSHOT ===` |",
        "| 2 | A2 | AAPL, TSLA, NVDA | Structural omission | Missing EVIDENCE_CITED, count fields — confidence unverifiable |",
        "| 3 | A2 | TSLA, NVDA | Value fabrication | CONFIDENCE=0.0 emitted — no grounding in tool output |",
        "| 4 | A3 | AAPL | Arithmetic error | 12% upside applied to LOW volatility stock (correct: 6%) |",
        "| 5 | A4 | NVDA | Tool-call fabrication | get_risk_metrics not called; values generated from parametric memory |",
        "| 6 | A5 | AAPL, TSLA, NVDA | Type conversion | Numeric confidence (0.x) silently converted to qualitative (LOW/MEDIUM) |",
        "",
    ]

    path = "evaluation/results/baseline_scores.md"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nBaseline scores written to {path}")


def main():
    all_results = {}
    for agent_name, runner in AGENT_RUNNERS:
        print(f"\n{'#'*60}")
        print(f"# {agent_name}")
        print(f"{'#'*60}")
        results = runner()
        all_results[agent_name] = results

    write_baseline_md(all_results)

    # Overall pass/fail count
    total = sum(len(v) for v in all_results.values())
    passed = sum(r["passed"] for v in all_results.values() for r in v)
    print(f"\nOverall: {passed}/{total} passed across all agents.")


if __name__ == "__main__":
    main()
