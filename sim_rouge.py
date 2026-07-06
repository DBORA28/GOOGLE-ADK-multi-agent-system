# =============================================================================
# SIMILARITY METHOD 4 — ROUGE Score (ROUGE-1 + ROUGE-L)
# Compares: Actual Response  ↔  Reference Answer (word overlap)
# Metric   : ROUGE-1 F1 (unigram) and ROUGE-L F1 (longest common subsequence)
# Threshold: >= 0.40
# =============================================================================
import os, csv, statistics
from collections import defaultdict
from rouge_score import rouge_scorer
from evaluation.ablation.testcase import SIMILARITY_PAIRS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/sim_rouge.csv")
THRESH = 0.40

scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)

def score(response, reference):
    result = scorer.score(reference, response)
    return {
        "rouge1": round(result["rouge1"].fmeasure, 4),
        "rougeL": round(result["rougeL"].fmeasure, 4),
    }

pair_ids = list(SIMILARITY_PAIRS.keys())
labels   = {k: SIMILARITY_PAIRS[k]["label"] for k in pair_ids}

rows = []
for run in range(1, RUNS + 1):
    for pid in pair_ids:
        pair = SIMILARITY_PAIRS[pid]
        sc   = score(pair["response"], pair["reference"])
        rows.append({"pair": pid, "label": labels[pid], "run": run,
                     "rouge1": sc["rouge1"], "rougeL": sc["rougeL"]})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","rouge1","rougeL"])
    w.writeheader(); w.writerows(rows)

by_r1 = defaultdict(list); by_rL = defaultdict(list)
for r in rows:
    by_r1[r["pair"]].append(r["rouge1"])
    by_rL[r["pair"]].append(r["rougeL"])

print("\n" + "="*65)
print("SIMILARITY M4: ROUGE (Actual ↔ Reference Answer)")
print("="*65)
print(f"{'Pair':<12} {'Label':<8} {'ROUGE-1':<12} {'ROUGE-L':<12} {'Pass'}")
print("-"*60)
for pid in pair_ids:
    r1 = statistics.mean(by_r1[pid]); rL = statistics.mean(by_rL[pid])
    label = labels[pid]
    status = "PASS" if r1 >= THRESH else "FAIL"
    print(f"{pid:<12} {'clean' if label==1 else 'degrad':<8} {r1:<12.4f} {rL:<12.4f} {status}")

clean_r1 = [r["rouge1"] for r in rows if r["label"]==1]
deg_r1   = [r["rouge1"] for r in rows if r["label"]==0]
sep      = statistics.mean(clean_r1) - statistics.mean(deg_r1)
print(f"\nSeparation score (ROUGE-1) : {sep:.4f}")
print(f"Results saved to           : {OUT}")
