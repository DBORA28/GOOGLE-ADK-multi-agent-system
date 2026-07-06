# =============================================================================
# HALLUCINATION METHOD 3 — Embedding Context Similarity
# Compares: Agent Response  ↔  Context (semantic grounding via embeddings)
# Metric   : cosine similarity between response embedding and context embedding
# Threshold: >= 0.60
# Model    : all-MiniLM-L6-v2 (local, no API)
# =============================================================================
import os, csv, statistics
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from evaluation.ablation.testcase import ACTUAL_RESPONSES, DEGRADED, CONTEXTS, LABELS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/hall_embedding.csv")
THRESH = 0.60

model = SentenceTransformer("all-MiniLM-L6-v2")

def score(response, context):
    embs = model.encode([response, context], show_progress_bar=False)
    return round(float(cosine_similarity([embs[0]], [embs[1]])[0][0]), 4)

# Build all pairs
all_pairs = {}
for pid, resp in ACTUAL_RESPONSES.items():
    all_pairs[pid] = {"response": resp, "context": CONTEXTS[pid], "label": LABELS.get(pid, 1)}
for key, resp in DEGRADED.items():
    base = "_".join(key.split("_")[:2])
    all_pairs[key] = {"response": resp, "context": CONTEXTS.get(base, ""), "label": 0}

rows = []
for run in range(1, RUNS + 1):
    for pid, pair in all_pairs.items():
        s = score(pair["response"], pair["context"])
        rows.append({"pair": pid, "label": pair["label"], "run": run, "score": s})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*65)
print("HALLUCINATION M3: EMBEDDING CONTEXT SIMILARITY")
print("="*65)
print(f"{'Pair':<16} {'Label':<8} {'Mean':<10} {'StdDev':<10} {'Pass (>=0.60)'}")
print("-"*60)
for pid, pair in all_pairs.items():
    sc = by_pair[pid]
    m  = statistics.mean(sc)
    sd = statistics.stdev(sc) if len(sc) > 1 else 0.0
    label = pair["label"]
    print(f"{pid:<16} {'clean' if label==1 else 'degrad':<8} {m:<10.4f} {sd:<10.4f} {'PASS' if m>=THRESH else 'FAIL'}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
sep   = statistics.mean(clean) - statistics.mean(deg)
print(f"\nSeparation score : {sep:.4f}")
print(f"Results saved to : {OUT}")
