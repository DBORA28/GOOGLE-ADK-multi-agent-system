# =============================================================================
# HALLUCINATION METHOD 2 — NLI Contradiction Score
# Compares: Each response sentence  ↔  Context (NLI entailment check)
# Metric   : contradiction_rate = CONTRADICTED sentences / total sentences
# Threshold: contradiction rate <= 0.15  (lower = better = less hallucination)
# Model    : cross-encoder/nli-deberta-v3-small (local, no API)
# =============================================================================
import os, csv, statistics
import nltk
from collections import defaultdict
from transformers import pipeline
from evaluation.ablation.testcase import ACTUAL_RESPONSES, DEGRADED, CONTEXTS, LABELS

nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/hall_nli.csv")
THRESH = 0.15   # contradiction rate must be LOW

print("Loading NLI model (cross-encoder/nli-deberta-v3-small)...")
nli = pipeline("text-classification",
               model="cross-encoder/nli-deberta-v3-small",
               device=-1,
               top_k=None)

def nli_contradiction_rate(response, context):
    sentences = nltk.sent_tokenize(response.strip())
    if not sentences:
        return 0.0
    contradictions = 0
    ctx_short = context[:512]
    for sent in sentences:
        results = nli({"text": ctx_short, "text_pair": sent[:256]})
        # results is a list of dicts with 'label' and 'score'
        labels_map = {r["label"].upper(): r["score"] for r in results}
        contradiction_score = labels_map.get("CONTRADICTION", 0.0)
        # flag as contradiction if score > 0.5
        if contradiction_score > 0.5:
            contradictions += 1
    return round(contradictions / len(sentences), 4)

# Build all pairs
all_pairs = {}
for pid, resp in ACTUAL_RESPONSES.items():
    all_pairs[pid] = {"response": resp, "context": CONTEXTS[pid], "label": LABELS.get(pid, 1)}
for key, resp in DEGRADED.items():
    base = "_".join(key.split("_")[:2])
    all_pairs[key] = {"response": resp, "context": CONTEXTS.get(base, ""), "label": 0}

rows = []
total = len(all_pairs) * RUNS
done  = 0
for run in range(1, RUNS + 1):
    print(f"Run {run}/{RUNS}...")
    for pid, pair in all_pairs.items():
        s    = nli_contradiction_rate(pair["response"], pair["context"])
        rows.append({"pair": pid, "label": pair["label"], "run": run, "score": s})
        done += 1

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*65)
print("HALLUCINATION M2: NLI CONTRADICTION RATE (lower = better)")
print("="*65)
print(f"{'Pair':<16} {'Label':<8} {'Contradiction%':<16} {'Pass (<=0.15)'}")
print("-"*55)
for pid, pair in all_pairs.items():
    sc = by_pair[pid]; m = statistics.mean(sc)
    label = pair["label"]
    print(f"{pid:<16} {'clean' if label==1 else 'degrad':<8} {m:<16.4f} {'PASS' if m<=THRESH else 'FAIL'}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
# For NLI: degraded should have HIGHER contradiction → separation = deg_mean - clean_mean
sep = statistics.mean(deg) - statistics.mean(clean)
print(f"\nSeparation score (deg-clean) : {sep:.4f}  (positive = method detects hallucinations)")
print(f"Results saved to             : {OUT}")
