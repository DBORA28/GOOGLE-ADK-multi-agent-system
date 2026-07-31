# =============================================================================
# SIMILARITY METHOD 2 — FAISS Vector Search
# Compares: Agent5 Response  ↔  Reference Answer Index
# Metric   : nDCG@k — does the response retrieve its own reference at rank 1?
# Threshold: nDCG >= 0.70 (rank-1 hit = 1.0, rank-2 = 0.63, rank-3 = 0.50)
# =============================================================================
import os, csv, math, statistics
from collections import defaultdict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from evaluation.ablation.testcase import SIMILARITY_PAIRS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/sim_faiss.csv")
THRESH = 0.70

model    = SentenceTransformer("all-MiniLM-L6-v2")
pair_ids = list(SIMILARITY_PAIRS.keys())
ref_tickers   = ['APPL', 'NVDA', 'TSLA']
refs        = [SIMILARITY_PAIRS[k]["reference"] for k in ref_tickers]
# Map each pair to its correct reference index
TICKER_IDX = {"AAPL": 0, "NVDA": 1, "TSLA": 2,
              "AAPL_d": 0, "NVDA_d": 1, "TSLA_d": 2}

# Build FAISS index over reference answers (built once — deterministic)
ref_embs = model.encode(refs, show_progress_bar=False).astype("float32")
faiss.normalize_L2(ref_embs)
index = faiss.IndexFlatIP(ref_embs.shape[1])
index.add(ref_embs)

def ndcg(response, correct_idx, k=len(pair_ids)):
    emb = model.encode([response], show_progress_bar=False).astype("float32")
    faiss.normalize_L2(emb)
    _, indices = index.search(emb, k)
    rank = list(indices[0]).index(correct_idx) + 1  # 1-based
    return round(1.0 / math.log2(rank + 1), 4)

rows = []
for run in range(1, RUNS + 1):
   for pid in pair_ids:
    s = ndcg(SIMILARITY_PAIRS[pid]["response"], TICKER_IDX[pid])
    rows.append({"pair": pid, "label": SIMILARITY_PAIRS[pid]["label"], "run": run, "score": s})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*60)
print("SIMILARITY M2: FAISS + nDCG (Response retrieves correct reference)")
print("="*60)
print(f"{'Pair':<12} {'Label':<8} {'Mean nDCG':<12} {'Rank-1?'}")
print("-"*50)
for pid in pair_ids:
    sc = by_pair[pid]; m = statistics.mean(sc)
    label = SIMILARITY_PAIRS[pid]["label"]
    rank1 = "YES" if m == 1.0 else "NO"
    print(f"{pid:<12} {'clean' if label==1 else 'degrad':<8} {m:<12.4f} {rank1}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
sep   = statistics.mean(clean) - statistics.mean(deg)
print(f"\nSeparation score : {sep:.4f}")
print(f"Results saved to : {OUT}")
