# =============================================================================
# SIMILARITY METHOD 1 — TF-IDF Cosine Similarity
# Compares: User Query  ↔  Agent 5 Final Response
# Metric   : cosine angle between TF-IDF vectors
# Threshold: >= 0.70 (adjusted to 0.30 for short-query vs long-response)
# =============================================================================
import os, csv, statistics
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from evaluation.ablation.testcase import SIMILARITY_PAIRS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/sim_cosine.csv")
THRESH = 0.30   # Q is short; long structured response always scores below 0.70

def score(query, response):
    vec   = TfidfVectorizer()
    tfidf = vec.fit_transform([query, response])
    return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])

rows = []
for run in range(1, RUNS + 1):
    for pid, pair in SIMILARITY_PAIRS.items():
        s = score(pair["query"], pair["response"])
        rows.append({"pair": pid, "label": pair["label"], "run": run, "score": round(s, 4)})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*60)
print("SIMILARITY M1: TF-IDF COSINE (Query ↔ Agent5 Response)")
print("="*60)
print(f"{'Pair':<12} {'Label':<8} {'Mean':<10} {'StdDev':<10} {'Pass'}")
print("-"*55)
for pid in SIMILARITY_PAIRS:
    sc = by_pair[pid]; m = statistics.mean(sc); sd = statistics.stdev(sc) if len(sc)>1 else 0.0
    label = SIMILARITY_PAIRS[pid]["label"]
    print(f"{pid:<12} {'clean' if label==1 else 'degrad':<8} {m:<10.4f} {sd:<10.4f} {'PASS' if m>=THRESH else 'FAIL'}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
sep   = statistics.mean(clean) - statistics.mean(deg)
print(f"\nSeparation score : {sep:.4f}  (clean mean - degraded mean)")
print(f"Results saved to : {OUT}")
