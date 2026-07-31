# Ground truth source data — exact values returned by tools
# These are what every agent should have cited. Used as context in DeepEval test cases.

AAPL_MARKET_SNAPSHOT = {
    "ticker": "AAPL",
    "price": 189.5,
    "change_perc": 1.2,
    "volume": 58000000,
    "rsi": 72,
    "ma_20": 188.55,
    "ma_50": 181.16,
    "sentiment": "POSITIVE",
    "volatility": "LOW",
    "beta": 1.1,
    "trend": "BULLISH",
}

NVDA_MARKET_SNAPSHOT = {
    "ticker": "NVDA",
    "price": 875.0,
    "change_perc": 3.5,
    "volume": 42000000,
    "rsi": 61,
    "ma_20": 870.63,
    "ma_50": 836.5,
    "sentiment": "POSITIVE",
    "volatility": "HIGH",
    "beta": 1.7,
    "trend": "BULLISH",
}

TSLA_MARKET_SNAPSHOT = {
    "ticker": "TSLA",
    "price": 245.3,
    "change_perc": -2.1,
    "volume": 120000000,
    "rsi": 45,
    "ma_20": 244.17,
    "ma_50": 234.51,
    "sentiment": "NEGATIVE",
    "volatility": "HIGH",
    "beta": 2.3,
    "trend": "BEARISH",
}

AAPL_RISK_METRICS = {
    "ticker": "AAPL",
    "volatility": "LOW",
    "beta": 1.1,
}

NVDA_RISK_METRICS = {
    "ticker": "NVDA",
    "volatility": "HIGH",
    "beta": 1.7,
}

TSLA_RISK_METRICS = {
    "ticker": "TSLA",
    "volatility": "HIGH",
    "beta": 2.3,
}