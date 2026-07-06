# Stock Research Agent — Google ADK Multi-Agent System

A production-style multi-agent stock research pipeline built with **Google Agent Development Kit (ADK) v2.1**. Given a natural-language query like *"Should I buy NVIDIA today?"*, the system runs five specialized agents sequentially — each one feeding its structured output into the next — and returns a final investment recommendation grounded entirely in tool-fetched data, not LLM training memory.

---

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  root_agent  (Agent — sequential orchestrator)          │
│                                                         │
│  ┌──────────────────────┐                               │
│  │ A1: market_indicator │  extracts ticker, fetches     │
│  │      _agent          │  snapshot via tool            │
│  └──────────┬───────────┘                               │
│             │  === MARKET_SNAPSHOT ===                  │
│  ┌──────────▼───────────┐                               │
│  │ decision_loop        │  LoopAgent — retries until    │
│  │  └─ A2: decision     │  confidence ≥ 0.6 or          │
│  │        _llm_agent    │  max_iterations reached       │
│  └──────────┬───────────┘                               │
│             │  === BUY_SELL_DECISION ===                │
│  ┌──────────▼───────────┐                               │
│  │ A3: profit_loss      │  calculates upside/downside   │
│  │      _agent          │  price targets via tool       │
│  └──────────┬───────────┘                               │
│             │  === PROFIT_LOSS_ANALYSIS ===             │
│  ┌──────────▼───────────┐                               │
│  │ A4: risk_agent       │  fetches beta + volatility    │
│  │                      │  via tool, rates risk         │
│  └──────────┬───────────┘                               │
│             │  RISK ASSESSMENT                          │
│  ┌──────────▼───────────┐                               │
│  │ A5: recommendation   │  synthesizes all prior        │
│  │      _agent          │  outputs — no tools, no LLM   │
│  │                      │  knowledge, copy-only         │
│  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
    │
    ▼
INVESTMENT RECOMMENDATION: NVDA
Decision   : BUY
Confidence : 0.6
Risk Level : HIGH
...
```

**Supported tickers:** AAPL · NVDA · TSLA

---

## Agent Breakdown

| Agent | File | Role | Tools |
|-------|------|------|-------|
| A1 — market_indicator_agent | `market_indicatorA1.py` | Extract ticker from query, fetch live snapshot | `get_market_snapshot` |
| A2 — decision_llm_agent | `decsionmakerA2.py` | Score indicators, produce BUY/SELL/HOLD + confidence | `stop_monitoring` |
| A3 — profit_loss_agent | `PROFITLOSSa4.py` | Calculate upside/downside price targets | `calculate_pl_range` |
| A4 — risk_agent | `risk3.py` | Fetch beta, assess investment risk tier | `get_risk_metrics` |
| A5 — recommendation_agent | `recommend5.py` | Final synthesis — reads all prior outputs, no tools | — |

All agents share a single conversation session. Each agent's structured output block (e.g. `=== MARKET_SNAPSHOT ===`) becomes part of the conversation history that downstream agents read. No explicit variable passing — the **conversation is the data bus**.

---

## Project Structure

```
ADK/
├── STOCK_RESEARCH_TEST/          # Main multi-agent pipeline
│   ├── agent.py                  # Entry point — root_agent definition
│   ├── market_indicatorA1.py     # Agent 1
│   ├── decsionmakerA2.py         # Agent 2
│   ├── PROFITLOSSa4.py           # Agent 3
│   ├── risk3.py                  # Agent 4
│   ├── recommend5.py             # Agent 5
│   ├── tools.py                  # All tool function definitions
│   └── __init__.py
│
├── evaluation/                   # DeepEval hallucination testing harness
│   ├── eval_agent1.py            # Per-agent evaluation scripts (1–5)
│   ├── eval_agent2.py
│   ├── eval_agent3.py
│   ├── eval_agent4.py
│   ├── eval_agent5.py
│   ├── run_baseline.py           # Runs all evals and prints summary
│   ├── inline_eval.py
│   ├── eval_data/                # Ground-truth tool outputs + agent outputs
│   │   ├── sources.py
│   │   ├── agent1_outputs.py
│   │   ├── agent2_outputs.py
│   │   ├── agent3_outputs.py
│   │   ├── agent4_outputs.py
│   │   └── agent5_outputs.py
│   └── ablation/                 # Ablation study — NLI, embedding, ROUGE, BERTScore
│       ├── run_ablation.py
│       ├── hall_nli.py
│       ├── hall_embedding.py
│       ├── hall_groundedness.py
│       ├── sim_rouge.py
│       ├── sim_cosine.py
│       ├── sim_bertscore.py
│       ├── sim_faiss.py
│       └── tool_trajectory.py
│
├── stock_research/               # Earlier single-agent version (reference)
├── my_agent/                     # Minimal ADK hello-world example
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone and create virtual environment

```bash
git clone https://github.com/<your-username>/stock-research-agent.git
cd stock-research-agent

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

```bash
cp STOCK_RESEARCH_TEST/.env.example STOCK_RESEARCH_TEST/.env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-proj-...
```

> Get an API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 4. Run the agent

```bash
# From the project root
adk run STOCK_RESEARCH_TEST "Should I buy NVIDIA today based on NASDAQ indicators?"
adk run STOCK_RESEARCH_TEST "Analyze whether Apple is a safe investment this week."
adk run STOCK_RESEARCH_TEST "Evaluate buy/sell confidence for Tesla using technical indicators."
```

### 5. Run the evaluation harness

```bash
# Run all 5 agent evaluations
python3 -m evaluation.run_baseline

# Run a single agent evaluation
python3 -m evaluation.eval_agent1
python3 -m evaluation.eval_agent2
```

### 6. Run ablation studies

```bash
python3 -m evaluation.ablation.run_ablation
```

---

## Evaluation Results

Evaluated with [DeepEval](https://github.com/confident-ai/deepeval) using `FaithfulnessMetric` and `HallucinationMetric`.

**Thresholds:** Faithfulness ≥ 0.85 · Hallucination ≤ 0.30

### Pre-fix baseline (FAIL — 6 hallucination types detected)

| Agent | Ticker | Faithfulness | Hallucination | Result |
|-------|--------|-------------|--------------|--------|
| A1 — market_indicator | AAPL | 1.00 | 0.36 | FAIL |
| A1 — market_indicator | TSLA | 0.86 | 0.36 | FAIL |
| A1 — market_indicator | NVDA | 0.71 | 0.45 | FAIL |
| A2 — decision | AAPL | 1.00 | 0.36 | FAIL |
| A2 — decision | NVDA | 1.00 | 0.55 | FAIL |
| A4 — risk | NVDA | 1.00 | 0.29 | PASS |
| A5 — recommendation | TSLA | 0.82 | 0.07 | FAIL |

### Hallucinations found and fixed

| # | Agent | Ticker | Type | Fix Applied |
|---|-------|--------|------|-------------|
| 1 | A1 | TSLA, NVDA | Format violation | Added explicit `Stop after === END SNAPSHOT ===` rule |
| 2 | A2 | All | Structural omission | Added EVIDENCE_CITED block + signal count fields |
| 3 | A2 | TSLA, NVDA | Value fabrication | Added explicit formula: `CONFIDENCE = BUY_COUNT / 5` |
| 4 | A3 | AAPL | Arithmetic error | Added mandatory STEP 1: quote VOLATILITY before selecting tier |
| 5 | A4 | NVDA | Tool-call fabrication | Added `You MUST call get_risk_metrics()` + `Copy beta exactly` |
| 6 | A5 | All | Type conversion | Removed enum from template, added `copy decimal, do not convert` |

---

## Key Design Patterns

### 1. Structured output blocks as contracts
Each agent wraps its output in `=== BLOCK_NAME === ... === END BLOCK ===` markers. Downstream agents parse these blocks reliably without regex or custom parsers — the LLM reads natural text and the markers guarantee structure.

### 2. Evidence-first reasoning
Every agent that reads from a prior agent must quote the values it will use before using them (e.g. `STEP 1 — Copy VOLATILITY from MARKET_SNAPSHOT: [value]`). This grounds the output in actual data before any computation.

### 3. Explicit formulas over vague instructions
`CONFIDENCE = SUPPORTING_BUY_COUNT / 5` beats `"give a confidence score"`. Formulas eliminate the LLM's ability to interpolate from training knowledge.

### 4. Mandatory tool calls
`"You MUST call get_risk_metrics(ticker) before writing any values. This is not optional."` — without this, the LLM uses memorized stock data instead of calling the tool.

### 5. Conversation as memory
No explicit state management. All agents share one ADK session; each agent's output block persists in conversation history and is readable by all downstream agents.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent framework | [Google ADK](https://google.github.io/adk-docs/) v2.1.0 |
| LLM | OpenAI `gpt-4o-mini` (via ADK's LiteLLM routing) |
| Evaluation | [DeepEval](https://github.com/confident-ai/deepeval) v4.0.5 |
| Session storage | SQLite (managed by ADK, `.adk/session.db`) |
| Python | 3.14 |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key — get one at platform.openai.com |

Store in `STOCK_RESEARCH_TEST/.env`. Never commit this file.

---

## Disclaimer

This project is for educational and research purposes only. The stock data used is static/mock data. This is not financial advice.
