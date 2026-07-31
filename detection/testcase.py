# =============================================================================
# ABLATION STUDY — CENTRAL DATA FILE
# EVALCHECK(USER QUERY, AGENT RESPONSE)
# Three queries × five agents = 15 pairs (clean) + 15 degraded = 30 total
# =============================================================================

# ---------------------------------------------------------------------------
# SECTION 1 — USER QUERIES
# ---------------------------------------------------------------------------
QUERIES = {
    "AAPL": "should we buy or sell AAPL stock based on NASDAQ indicators?",
    "NVDA": "analyse NVIDIA stock can we make it on hold",
    "TSLA": "analyse tsla stock should i buy or sell",
}

# ---------------------------------------------------------------------------
# SECTION 2 — ACTUAL LIVE RESPONSES (ADK re-run, post-fix)
# ---------------------------------------------------------------------------
ACTUAL_A1 = {
    "AAPL": """=== MARKET_SNAPSHOT ===
TICKER     : AAPL
PRICE      : $189.5
CHANGE     : 1.2%
RSI        : 72 → OVERBOUGHT
SENTIMENT  : POSITIVE
VOLATILITY : LOW
TREND      : BULLISH
=== END SNAPSHOT ===""",

    "NVDA": """=== MARKET_SNAPSHOT ===
TICKER     : NVDA
PRICE      : $875.0
CHANGE     : 3.5%
RSI        : 61 → NEUTRAL
SENTIMENT  : POSITIVE
VOLATILITY : HIGH
TREND      : BULLISH
=== END SNAPSHOT ===""",

    "TSLA": """=== MARKET_SNAPSHOT ===
TICKER     : TSLA
PRICE      : $245.3
CHANGE     : -2.1%
RSI        : 45 → NEUTRAL
SENTIMENT  : NEGATIVE
VOLATILITY : HIGH
TREND      : BEARISH
=== END SNAPSHOT ==="""
}

ACTUAL_A2 = {
    "AAPL": """=== BUY_SELL_DECISION ===
TICKER               : AAPL
RSI_SIGNAL           : SUPPORTS_SELL
TREND_SIGNAL         : SUPPORTS_BUY
SENTIMENT_SIGNAL     : SUPPORTS_BUY
VOLATILITY_SIGNAL    : NEUTRAL
CHANGE_SIGNAL        : SUPPORTS_BUY
SUPPORTING_BUY_COUNT : 3
SUPPORTING_SELL_COUNT: 1
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.6
DECISION             : BUY
=== END DECISION ===""",

    "NVDA": """=== BUY_SELL_DECISION ===
TICKER               : NVDA
RSI_SIGNAL           : NEUTRAL
TREND_SIGNAL         : SUPPORTS_BUY
SENTIMENT_SIGNAL     : SUPPORTS_BUY
VOLATILITY_SIGNAL    : SUPPORTS_SELL
CHANGE_SIGNAL        : SUPPORTS_BUY
SUPPORTING_BUY_COUNT : 3
SUPPORTING_SELL_COUNT: 1
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.6
DECISION             : BUY
=== END DECISION ===""",

    # HALLUCINATION: CONFIDENCE=0.8 but BUY_COUNT=0 → formula gives 0/5=0.0
    "TSLA": """=== BUY_SELL_DECISION ===
TICKER               : TSLA
RSI_SIGNAL           : NEUTRAL
TREND_SIGNAL         : SUPPORTS_SELL
SENTIMENT_SIGNAL     : SUPPORTS_SELL
VOLATILITY_SIGNAL    : SUPPORTS_SELL
CHANGE_SIGNAL        : SUPPORTS_SELL
SUPPORTING_BUY_COUNT : 0
SUPPORTING_SELL_COUNT: 4
NEUTRAL_COUNT        : 1
CONFIDENCE           : 0.8
DECISION             : SELL
=== END DECISION ==="""
}

ACTUAL_A3 = {
    "AAPL": """=== PROFIT_LOSS_ANALYSIS ===
TICKER          : AAPL
VOLATILITY_USED : LOW
CURRENT_PRICE   : $189.5
UPSIDE_TARGET   : $200.87 (+6%)
DOWNSIDE_TARGET : $183.81 (-3%)
=== END P&L ===""",

    "NVDA": """=== PROFIT_LOSS_ANALYSIS ===
TICKER          : NVDA
VOLATILITY_USED : HIGH
CURRENT_PRICE   : $875.0
UPSIDE_TARGET   : $980.00 (+12%)
DOWNSIDE_TARGET : $822.50 (-6%)
=== END P&L ===""",

    "TSLA": """=== PROFIT_LOSS_ANALYSIS ===
TICKER          : TSLA
VOLATILITY_USED : HIGH
CURRENT_PRICE   : $245.3
UPSIDE_TARGET   : $274.74 (+12%)
DOWNSIDE_TARGET : $230.58 (-6%)
=== END P&L ==="""
}

ACTUAL_A4 = {
    "AAPL": """RISK ASSESSMENT: AAPL
Volatility : LOW
Beta       : 1.1 → moderate risk
RISK RATING: MEDIUM""",

    "NVDA": """RISK ASSESSMENT: NVDA
Volatility : HIGH
Beta       : 1.7 → higher risk
RISK RATING: HIGH""",

    "TSLA": """RISK ASSESSMENT: TSLA
Volatility : HIGH
Beta       : 2.3 → higher risk
RISK RATING: HIGH"""
}

ACTUAL_A5 = {
    "AAPL": """INVESTMENT RECOMMENDATION: AAPL
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : MEDIUM
P&L Upside     : $200.87
P&L Downside   : $183.81
FINAL DECISION : BUY
Confidence     : 0.6
Reason         : The decision to buy AAPL is supported by a bullish trend and positive sentiment. Despite an overbought RSI indicating potential for a pullback, the overall analysis favors a buy action based on multiple supporting signals.""",

    "NVDA": """INVESTMENT RECOMMENDATION: NVDA
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : HIGH
P&L Upside     : $980.00
P&L Downside   : $822.50
FINAL DECISION : BUY
Confidence     : 0.6
Reason         : The recommendation to buy NVDA is based on a bullish trend and positive sentiment. Although the high volatility poses a greater risk, the overall analysis leans towards a buy decision supported by multiple signals.""",

    # HALLUCINATION: Confidence 0.8 cascaded from Agent 2 TSLA bug
    "TSLA": """INVESTMENT RECOMMENDATION: TSLA
Market Trend   : BEARISH
Decision       : SELL
Confidence     : 0.8
Risk Level     : HIGH
P&L Upside     : $274.74
P&L Downside   : $230.58
FINAL DECISION : SELL
Confidence     : 0.8
Reason         : The decision to sell TSLA is supported by a bearish trend and negative sentiment. With all indicators suggesting selling and a high risk rating, this aligns with a cautious approach in the current market conditions."""
}

# ---------------------------------------------------------------------------
# SECTION 3 — REFERENCE ANSWERS (expected correct outputs)
# ---------------------------------------------------------------------------
REF_A5 = {
    "AAPL": """INVESTMENT RECOMMENDATION: AAPL
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : MEDIUM
P&L Upside     : $200.87
P&L Downside   : $183.82
FINAL DECISION : BUY
Confidence     : 0.6
Reason         : AAPL shows bullish trend with positive sentiment and +1.2% change. RSI at 72 indicates overbought conditions but 3 of 5 indicators support a buy. Low volatility and beta of 1.1 indicate moderate risk.""",

    "NVDA": """INVESTMENT RECOMMENDATION: NVDA
Market Trend   : BULLISH
Decision       : BUY
Confidence     : 0.6
Risk Level     : HIGH
P&L Upside     : $980.0
P&L Downside   : $822.5
FINAL DECISION : BUY
Confidence     : 0.6
Reason         : NVDA shows bullish trend with positive sentiment and +3.5% change. 3 of 5 indicators support a buy. High volatility (beta=1.7) is a risk factor but confidence threshold is met.""",

    "TSLA": """INVESTMENT RECOMMENDATION: TSLA
Market Trend   : BEARISH
Decision       : SELL
Confidence     : 0.0
Risk Level     : HIGH
P&L Upside     : $274.74
P&L Downside   : $230.58
FINAL DECISION : SELL
Confidence     : 0.0
Reason         : TSLA shows bearish trend with negative sentiment and -2.1% change. Zero buy indicators detected across all 5 signals. High volatility and beta of 2.3 confirm elevated risk."""
}

# ---------------------------------------------------------------------------
# SECTION 4 — CONTEXTS (what each agent was allowed to read from)
# ---------------------------------------------------------------------------
_AAPL_TOOL = "ticker: AAPL, price: 189.5, change_perc: 1.2, rsi: 72, sentiment: POSITIVE, volatility: LOW, trend: BULLISH"
_NVDA_TOOL = "ticker: NVDA, price: 875.0, change_perc: 3.5, rsi: 61, sentiment: POSITIVE, volatility: HIGH, trend: BULLISH"
_TSLA_TOOL = "ticker: TSLA, price: 245.3, change_perc: -2.1, rsi: 45, sentiment: NEGATIVE, volatility: HIGH, trend: BEARISH"
_AAPL_RISK = "ticker: AAPL, volatility: LOW, beta: 1.1"
_NVDA_RISK = "ticker: NVDA, volatility: HIGH, beta: 1.7"
_TSLA_RISK = "ticker: TSLA, volatility: HIGH, beta: 2.3"

CONTEXTS = {
    "A1_AAPL": _AAPL_TOOL,
    "A1_NVDA": _NVDA_TOOL,
    "A1_TSLA": _TSLA_TOOL,
    "A2_AAPL": ACTUAL_A1["AAPL"],
    "A2_NVDA": ACTUAL_A1["NVDA"],
    "A2_TSLA": ACTUAL_A1["TSLA"],
    "A3_AAPL": ACTUAL_A1["AAPL"] + "\n" + ACTUAL_A2["AAPL"],
    "A3_NVDA": ACTUAL_A1["NVDA"] + "\n" + ACTUAL_A2["NVDA"],
    "A3_TSLA": ACTUAL_A1["TSLA"] + "\n" + ACTUAL_A2["TSLA"],
    "A4_AAPL": _AAPL_RISK,
    "A4_NVDA": _NVDA_RISK,
    "A4_TSLA": _TSLA_RISK,
    "A5_AAPL": ACTUAL_A1["AAPL"] + "\n" + ACTUAL_A2["AAPL"] + "\n" + ACTUAL_A3["AAPL"] + "\n" + ACTUAL_A4["AAPL"],
    "A5_NVDA": ACTUAL_A1["NVDA"] + "\n" + ACTUAL_A2["NVDA"] + "\n" + ACTUAL_A3["NVDA"] + "\n" + ACTUAL_A4["NVDA"],
    "A5_TSLA": ACTUAL_A1["TSLA"] + "\n" + ACTUAL_A2["TSLA"] + "\n" + ACTUAL_A3["TSLA"] + "\n" + ACTUAL_A4["TSLA"],
}

# ---------------------------------------------------------------------------
# SECTION 5 — ALL ACTUAL RESPONSES FLAT (15 pairs for hallucination methods)
# ---------------------------------------------------------------------------
ACTUAL_RESPONSES = {
    "A1_AAPL": ACTUAL_A1["AAPL"], "A1_NVDA": ACTUAL_A1["NVDA"], "A1_TSLA": ACTUAL_A1["TSLA"],
    "A2_AAPL": ACTUAL_A2["AAPL"], "A2_NVDA": ACTUAL_A2["NVDA"], "A2_TSLA": ACTUAL_A2["TSLA"],
    "A3_AAPL": ACTUAL_A3["AAPL"], "A3_NVDA": ACTUAL_A3["NVDA"], "A3_TSLA": ACTUAL_A3["TSLA"],
    "A4_AAPL": ACTUAL_A4["AAPL"], "A4_NVDA": ACTUAL_A4["NVDA"], "A4_TSLA": ACTUAL_A4["TSLA"],
    "A5_AAPL": ACTUAL_A5["AAPL"], "A5_NVDA": ACTUAL_A5["NVDA"], "A5_TSLA": ACTUAL_A5["TSLA"],
}

# ---------------------------------------------------------------------------
# SECTION 6 — DEGRADED VARIANTS (controlled corruptions for ablation)
# ---------------------------------------------------------------------------
DEGRADED = {
    # Agent 1: swap field values
    "A1_AAPL_d": ACTUAL_A1["AAPL"].replace("RSI        : 72 → OVERBOUGHT", "RSI        : 45 → NEUTRAL"),
    "A1_NVDA_d": ACTUAL_A1["NVDA"].replace("VOLATILITY : HIGH", "VOLATILITY : LOW"),
    "A1_TSLA_d": "\n".join(l for l in ACTUAL_A1["TSLA"].splitlines() if "SENTIMENT" not in l),

    # Agent 2: break count / confidence
    "A2_AAPL_d": ACTUAL_A2["AAPL"].replace("SUPPORTING_BUY_COUNT : 3", "SUPPORTING_BUY_COUNT : 1"),
    "A2_NVDA_d": ACTUAL_A2["NVDA"].replace("CONFIDENCE           : 0.6", "CONFIDENCE           : 0.9"),
    "A2_TSLA_d": ACTUAL_A2["TSLA"],  # already hallucinated: CONFIDENCE 0.8 when formula gives 0.0

    # Agent 3: wrong tier percentages
    "A3_AAPL_d": ACTUAL_A3["AAPL"].replace("UPSIDE_TARGET   : $200.87 (+6%)", "UPSIDE_TARGET   : $212.24 (+12%)"),
    "A3_NVDA_d": ACTUAL_A3["NVDA"].replace("DOWNSIDE_TARGET : $822.50 (-6%)", "DOWNSIDE_TARGET : $848.75 (-3%)"),
    "A3_TSLA_d": ACTUAL_A3["TSLA"].replace("CURRENT_PRICE   : $245.3", "CURRENT_PRICE   : $189.5"),

    # Agent 4: wrong beta value (original pre-fix hallucination)
    "A4_AAPL_d": ACTUAL_A4["AAPL"].replace("Beta       : 1.1 → moderate risk", "Beta       : 0.8 → lower risk"),
    "A4_NVDA_d": ACTUAL_A4["NVDA"].replace("RISK RATING: HIGH", "RISK RATING: MEDIUM"),
    "A4_TSLA_d": ACTUAL_A4["TSLA"].replace("Beta       : 2.3 → higher risk", "Beta       : 1.9 → higher risk"),

    # Agent 5: confidence as word, off-topic addition, wrong decision
    "A5_AAPL_d": ACTUAL_A5["AAPL"].replace("Confidence     : 0.6", "Confidence     : MEDIUM"),
    "A5_NVDA_d": ACTUAL_A5["NVDA"] + "\nNote: Gold prices are also rising globally.",
    "A5_TSLA_d": ACTUAL_A5["TSLA"],  # already hallucinated: Confidence 0.8 cascaded
}

# ---------------------------------------------------------------------------
# SECTION 7 — LABELS (1=clean, 0=degraded/hallucinated)
# ---------------------------------------------------------------------------
LABELS = {
    "A1_AAPL": 1, "A1_NVDA": 1, "A1_TSLA": 1,
    "A2_AAPL": 1, "A2_NVDA": 1, "A2_TSLA": 0,  # natural hallucination
    "A3_AAPL": 1, "A3_NVDA": 1, "A3_TSLA": 1,
    "A4_AAPL": 1, "A4_NVDA": 1, "A4_TSLA": 1,
    "A5_AAPL": 1, "A5_NVDA": 1, "A5_TSLA": 0,  # cascaded hallucination
    # degraded
    "A1_AAPL_d": 0, "A1_NVDA_d": 0, "A1_TSLA_d": 0,
    "A2_AAPL_d": 0, "A2_NVDA_d": 0, "A2_TSLA_d": 0,
    "A3_AAPL_d": 0, "A3_NVDA_d": 0, "A3_TSLA_d": 0,
    "A4_AAPL_d": 0, "A4_NVDA_d": 0, "A4_TSLA_d": 0,
    "A5_AAPL_d": 0, "A5_NVDA_d": 0, "A5_TSLA_d": 0,
}

# ---------------------------------------------------------------------------
# SECTION 8 — SIMILARITY PAIRS (Q vs Agent5 — end-to-end relevance)
# ---------------------------------------------------------------------------
SIMILARITY_PAIRS = {
    "AAPL": {"query": QUERIES["AAPL"], "response": ACTUAL_A5["AAPL"], "reference": REF_A5["AAPL"], "label": 1},
    "NVDA": {"query": QUERIES["NVDA"], "response": ACTUAL_A5["NVDA"], "reference": REF_A5["NVDA"], "label": 1},
    "TSLA": {"query": QUERIES["TSLA"], "response": ACTUAL_A5["TSLA"], "reference": REF_A5["TSLA"], "label": 1},
    # degraded variants
    "AAPL_d": {"query": QUERIES["AAPL"], "response": DEGRADED["A5_AAPL_d"], "reference": REF_A5["AAPL"], "label": 0},
    "NVDA_d": {"query": QUERIES["NVDA"], "response": DEGRADED["A5_NVDA_d"], "reference": REF_A5["NVDA"], "label": 0},
    "TSLA_d": {"query": QUERIES["TSLA"], "response": DEGRADED["A5_TSLA_d"], "reference": REF_A5["TSLA"], "label": 0},
}

# ---------------------------------------------------------------------------
# SECTION 9 — TOOL TRAJECTORIES
# ---------------------------------------------------------------------------
EXPECTED_TRAJECTORY = {
    "AAPL": ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
    "NVDA": ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
    "TSLA": ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
}

# From live ADK run traces
ACTUAL_TRAJECTORY = {
    "AAPL": {
        "tools_called":  ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
        "args": {
            "get_market_snapshot":  {"ticker": "AAPL"},
            "calculate_pl_range":   {"current_price": 189.5, "upside_pct": 6,  "downside_pct": 3},
            "get_risk_metrics":     {"ticker": "AAPL"},
            "stop_monitoring":      {"confidence_valid": True},   # 0.6 = correct
        }
    },
    "NVDA": {
        "tools_called":  ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
        "args": {
            "get_market_snapshot":  {"ticker": "NVDA"},
            "calculate_pl_range":   {"current_price": 875.0, "upside_pct": 12, "downside_pct": 6},
            "get_risk_metrics":     {"ticker": "NVDA"},
            "stop_monitoring":      {"confidence_valid": True},   # 0.6 = correct
        }
    },
    "TSLA": {
        "tools_called":  ["get_market_snapshot", "stop_monitoring", "calculate_pl_range", "get_risk_metrics"],
        "args": {
            "get_market_snapshot":  {"ticker": "TSLA"},
            "calculate_pl_range":   {"current_price": 245.3, "upside_pct": 12, "downside_pct": 6},
            "get_risk_metrics":     {"ticker": "TSLA"},
            "stop_monitoring":      {"confidence_valid": False},  # 0.8 fabricated — BUY_COUNT=0
        }
    },
}

EXPECTED_ARGS = {
    "AAPL": {"get_market_snapshot": {"ticker":"AAPL"}, "calculate_pl_range": {"current_price":189.5,"upside_pct":6,"downside_pct":3},  "get_risk_metrics": {"ticker":"AAPL"}},
    "NVDA": {"get_market_snapshot": {"ticker":"NVDA"}, "calculate_pl_range": {"current_price":875.0,"upside_pct":12,"downside_pct":6}, "get_risk_metrics": {"ticker":"NVDA"}},
    "TSLA": {"get_market_snapshot": {"ticker":"TSLA"}, "calculate_pl_range": {"current_price":245.3,"upside_pct":12,"downside_pct":6}, "get_risk_metrics": {"ticker":"TSLA"}},
}
