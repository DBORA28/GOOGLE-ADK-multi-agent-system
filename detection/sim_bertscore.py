# =============================================================================
# SIMILARITY METHOD 3 — BERTScore
# Compares: Actual Response  ↔  Reference Answer (token-level contextual match)
# Metric   : F1 score using contextual BERT embeddings
# Threshold: F1 >= 0.75
# =============================================================================
import os, csv, statistics
from collections import defaultdict
from bert_score import score as bert_score_fn
from evaluation.ablation.testcase import SIMILARITY_PAIRS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/sim_bertscore.csv")
THRESH = 0.75

pair_ids   = list(SIMILARITY_PAIRS.keys())
actuals    = [SIMILARITY_PAIRS[k]["response"]  for k in pair_ids]
references = [SIMILARITY_PAIRS[k]["reference"] for k in pair_ids]
labels     = [SIMILARITY_PAIRS[k]["label"]     for k in pair_ids]

# BERTScore is deterministic — compute once, replicate across runs
print("Computing BERTScore (runs once per call, replicated for 20 runs)...")
_, _, F1 = bert_score_fn(actuals, references, lang="en", verbose=False)
f1_values = [round(f.item(), 4) for f in F1]

rows = []
for run in range(1, RUNS + 1):
    for i, pid in enumerate(pair_ids):
        rows.append({"pair": pid, "label": labels[i], "run": run, "score": f1_values[i]})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*60)
print("SIMILARITY M3: BERTScore F1 (Actual ↔ Reference Answer)")
print("="*60)
print(f"{'Pair':<12} {'Label':<8} {'BERTScore F1':<15} {'Pass (>=0.75)'}")
print("-"*55)
for i, pid in enumerate(pair_ids):
    m = f1_values[i]
    print(f"{pid:<12} {'clean' if labels[i]==1 else 'degrad':<8} {m:<15.4f} {'PASS' if m>=THRESH else 'FAIL'}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
sep   = statistics.mean(clean) - statistics.mean(deg)
print(f"\nSeparation score : {sep:.4f}")
print(f"Results saved to : {OUT}")
