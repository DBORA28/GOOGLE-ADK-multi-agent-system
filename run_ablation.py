# =============================================================================
# MASTER RUNNER — Full Ablation Study
# Runs all 8 evaluation scripts and writes final comparison report
# =============================================================================
import os, csv, glob, statistics, datetime

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
REPORT_PATH = os.path.join(RESULTS_DIR, "ablation_report.md")

BANNER = "="*70

def run_all():
    print(BANNER)
    print("  ABLATION STUDY — FULL RUN")
    print(f"  Date: {datetime.date.today()}")
    print(BANNER)

    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    # ── SIMILARITY METHODS ────────────────────────────────────────────────────
    print("\n\n[1/7] Similarity M1: TF-IDF Cosine")
    from evaluation.ablation import sim_cosine      # noqa: F401

    print("\n\n[2/7] Similarity M2: FAISS + nDCG")
    from evaluation.ablation import sim_faiss       # noqa: F401

    print("\n\n[3/7] Similarity M3: BERTScore")
    from evaluation.ablation import sim_bertscore   # noqa: F401

    print("\n\n[4/7] Similarity M4: ROUGE")
    from evaluation.ablation import sim_rouge       # noqa: F401

    # ── HALLUCINATION METHODS ─────────────────────────────────────────────────
    print("\n\n[5/7] Hallucination M1: Groundedness")
    from evaluation.ablation import hall_groundedness  # noqa: F401

    print("\n\n[6/7] Hallucination M3: Embedding Context")
    from evaluation.ablation import hall_embedding  # noqa: F401

    print("\n\n[7/7] Tool Trajectory Score")
    from evaluation.ablation import tool_trajectory  # noqa: F401

    # ── FINAL COMPARISON TABLE ────────────────────────────────────────────────
    print(f"\n\n{BANNER}")
    print("  ABLATION STUDY — FINAL COMPARISON TABLE")
    print(BANNER)

    METHOD_META = {
        "sim_cosine":        ("Similarity",    "TF-IDF Cosine",          ">=0.30",  "clean-deg"),
        "sim_faiss":         ("Similarity",    "FAISS + nDCG",           ">=0.70",  "clean-deg"),
        "sim_bertscore":     ("Similarity",    "BERTScore F1",           ">=0.75",  "clean-deg"),
        "sim_rouge":         ("Similarity",    "ROUGE-1",                ">=0.40",  "clean-deg"),
        "hall_groundedness": ("Hallucination", "Groundedness",           ">=0.75",  "clean-deg"),
        "hall_embedding":    ("Hallucination", "Embedding Context",      ">=0.60",  "clean-deg"),
        "hall_nli":          ("Hallucination", "NLI Contradiction Rate", "<=0.15",  "deg-clean"),
    }

    print(f"\n{'Method':<28} {'Category':<14} {'Clean Mean':<13} {'Deg Mean':<12} {'Separation':<13} {'Threshold'}")
    print("-"*92)

    report_lines = [
        "# Ablation Study Report",
        f"\nDate: {datetime.date.today()}",
        "\n## Comparison Table\n",
        f"| Method | Category | Clean Mean | Degraded Mean | Separation | Threshold |",
        "|---|---|---|---|---|---|",
    ]

    for csv_key, (category, label, threshold, sep_dir) in METHOD_META.items():
        csv_path = os.path.join(RESULTS_DIR, f"{csv_key}.csv")
        if not os.path.exists(csv_path):
            print(f"  [SKIPPED] {label} — result file not found")
            continue

        clean_scores, deg_scores = [], []
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                if "score" in row:
                    sc = float(row["score"])
                    if int(row["label"]) == 1:
                        clean_scores.append(sc)
                    else:
                        deg_scores.append(sc)

        if not clean_scores or not deg_scores:
            continue

        mc  = round(statistics.mean(clean_scores), 4)
        md  = round(statistics.mean(deg_scores),   4)
        sep = round((mc - md) if sep_dir == "clean-deg" else (md - mc), 4)

        print(f"{label:<28} {category:<14} {mc:<13} {md:<12} {sep:<13} {threshold}")
        report_lines.append(f"| {label} | {category} | {mc} | {md} | {sep} | {threshold} |")

    # Tool trajectory (separate file format)
    traj_path = os.path.join(RESULTS_DIR, "tool_trajectory.csv")
    if os.path.exists(traj_path):
        scores = []
        with open(traj_path) as f:
            for row in csv.DictReader(f):
                if row.get("ticker") and row["ticker"] != "average":
                    scores.append(float(row["score"]))
        if scores:
            avg = round(statistics.mean(scores), 4)
            print(f"{'Tool Trajectory Avg':<28} {'Agent Eval':<14} {avg:<13} {'N/A':<12} {'N/A':<13} {'>=0.85'}")
            report_lines.append(f"| Tool Trajectory Avg | Agent Eval | {avg} | N/A | N/A | >=0.85 |")

    report_lines += [
        "\n## Selection Criteria",
        "\n- **Best Similarity method** = highest separation score among S1–S4",
        "- **Best Hallucination method** = highest separation score among H1–H3",
        "- **Minimum viable separation** = 0.10",
        "- **Strong candidate** = separation > 0.20",
    ]

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(report_lines))

    print(f"\nFull report saved to: {REPORT_PATH}")
    print(BANNER)


if __name__ == "__main__":
    run_all()
