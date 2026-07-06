# =============================================================================
# HALLUCINATION METHOD 1 — Groundedness (Word Traceability)
# Compares: Agent Response  ↔  Context the agent had access to
# Metric   : fraction of response key-tokens found in context
# Threshold: >= 0.75
# No LLM — pure token matching
# =============================================================================
import os, csv, re, statistics
from collections import defaultdict
from evaluation.ablation.testcase import ACTUAL_RESPONSES, DEGRADED, CONTEXTS, LABELS

RUNS   = 20
OUT    = os.path.join(os.path.dirname(__file__), "results/hall_groundedness.csv")
THRESH = 0.75

# Stop words to ignore during traceability check
STOPWORDS = {"the","a","an","is","are","was","were","be","been","being","have","has",
             "had","do","does","did","will","would","could","should","may","might",
             "to","of","in","for","on","with","at","by","from","as","and","or","but",
             "it","its","this","that","these","those","we","you","i","our","your"}

def key_tokens(text):
    tokens = re.findall(r"\b[a-zA-Z0-9_.]+\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def groundedness_score(response, context):
    resp_tokens = set(key_tokens(response))
    ctx_tokens  = set(key_tokens(context))
    if not resp_tokens:
        return 0.0
    found = resp_tokens & ctx_tokens
    return round(len(found) / len(resp_tokens), 4)

# Build all pairs: 15 clean + 15 degraded
all_pairs = {}
for pid, resp in ACTUAL_RESPONSES.items():
    all_pairs[pid] = {"response": resp, "context": CONTEXTS[pid], "label": LABELS.get(pid, 1)}
for key, resp in DEGRADED.items():
    base = "_".join(key.split("_")[:2])
    all_pairs[key] = {"response": resp, "context": CONTEXTS.get(base, ""), "label": 0}

rows = []
for run in range(1, RUNS + 1):
    for pid, pair in all_pairs.items():
        s = groundedness_score(pair["response"], pair["context"])
        rows.append({"pair": pid, "label": pair["label"], "run": run, "score": s})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pair","label","run","score"])
    w.writeheader(); w.writerows(rows)

by_pair = defaultdict(list)
for r in rows: by_pair[r["pair"]].append(r["score"])

print("\n" + "="*65)
print("HALLUCINATION M1: GROUNDEDNESS (Word Traceability)")
print("="*65)
print(f"{'Pair':<16} {'Label':<8} {'Mean':<10} {'Pass (>=0.75)'}")
print("-"*50)
for pid, pair in all_pairs.items():
    sc = by_pair[pid]; m = statistics.mean(sc)
    label = pair["label"]
    print(f"{pid:<16} {'clean' if label==1 else 'degrad':<8} {m:<10.4f} {'PASS' if m>=THRESH else 'FAIL'}")

clean = [r["score"] for r in rows if r["label"]==1]
deg   = [r["score"] for r in rows if r["label"]==0]
sep   = statistics.mean(clean) - statistics.mean(deg)
print(f"\nSeparation score : {sep:.4f}")
print(f"Results saved to : {OUT}")
