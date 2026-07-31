STOCK_DB = {

    "AAPL": {
        "price": 189.5, "change_perc": 1.2, "volume": 58_000_000,
        "revenue_growth": 8.2, "profit_margin": 25.3,
        "debt_to_equity": 1.8, "earnings_growth": 11.0,
        "volatility": "LOW", "beta": 1.1,
        "news": ["Apple hits all-time high", "iPhone 16 demand strong"]
    },
    "NVDA": {
        "price": 875.0, "change_perc": 3.5, "volume": 42_000_000,
        "revenue_growth": 122.0, "profit_margin": 55.0,
        "debt_to_equity": 0.4, "earnings_growth": 168.0,
        "volatility": "HIGH", "beta": 1.7,
        "news": ["NVDA wins $10B AI chip contract", "Data center demand surges"]
    },
    "TSLA": {
        "price": 245.3, "change_perc": -2.1, "volume": 120_000_000,
        "revenue_growth": 9.0, "profit_margin": 5.5,
        "debt_to_equity": 0.6, "earnings_growth": -34.0,
        "volatility": "HIGH", "beta": 2.3,
        "news": ["Tesla misses delivery estimates", "Elon Musk sells shares"]
    },
}


def get_stock_price(ticker: str) -> dict:
    """Returns current price, daily change percentage, and trading volume for a stock ticker."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    d = STOCK_DB[ticker]
    return {
        "ticker": ticker,
        "price": d["price"],
        "change_perc": d["change_perc"],
        "volume": d["volume"],
    }


def get_fundamentals(ticker: str) -> dict:
    """Returns fundamental financial data: revenue growth, profit margin, debt-to-equity ratio, and earnings growth for a stock ticker."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    d = STOCK_DB[ticker]
    return {
        "ticker": ticker,
        "revenue_growth_pct": d["revenue_growth"],
        "profit_margin_pct": d["profit_margin"],
        "debt_to_equity": d["debt_to_equity"],
        "earnings_growth_pct": d["earnings_growth"],
    }


def get_technical_indicators(ticker: str) -> dict:
    """Returns technical analysis signal based on price and daily change percentage for a stock ticker."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    d = STOCK_DB[ticker]
    return {
        "ticker": ticker,
        "price": d["price"],
        "change_perc": d["change_perc"],
        "trend": "BULLISH" if d["change_perc"] > 0 else "BEARISH",
    }


def get_risk_metrics(ticker: str) -> dict:
    """Returns risk metrics: volatility level and beta coefficient for a stock ticker."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    d = STOCK_DB[ticker]
    return {
        "ticker": ticker,
        "volatility": d["volatility"],
        "beta": d["beta"],
    }


def get_stock_news(ticker: str) -> dict:
    """Returns latest news headlines for a stock ticker."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    return {
        "ticker": ticker,
        "headlines": STOCK_DB[ticker]["news"],
    }


def check_price_alert(ticker: str, threshold_price: float) -> dict:
    """Checks if a stock price has dropped below a given threshold price. Returns alert_triggered=True if price is below threshold."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    current = STOCK_DB[ticker]["price"]
    triggered = current <= threshold_price
    return {
        "ticker": ticker,
        "current_price": current,
        "threshold": threshold_price,
        "alert_triggered": triggered,
        "message": (
            f"ALERT: {ticker} at ${current} dropped below threshold ${threshold_price}"
            if triggered
            else f"OK: {ticker} at ${current} is above threshold ${threshold_price}"
        ),
    }


def stop_monitoring(tool_context) -> dict:
    """Signals the LoopAgent to stop iterating. Call when confidence threshold is met or alert fires."""
    tool_context.actions.escalate = True
    return {"action": "STOP_LOOP", "status": "Monitoring stopped by agent decision."}


def validate_decision_support(decision: str, confidence: float) -> dict:
    """Validates that a BUY/SELL/HOLD decision has sufficient confidence. Returns valid=True if confidence >= 0.6."""
    valid = confidence >= 0.6
    return {
        "decision": decision.upper(),
        "confidence": confidence,
        "valid": valid,
        "message": (
            f"Decision {decision.upper()} accepted with confidence {confidence:.2f}"
            if valid
            else f"Decision {decision.upper()} rejected — confidence {confidence:.2f} below 0.6 threshold"
        ),
    }


def calculate_pl_range(current_price: float, upside_pct: float, downside_pct: float) -> dict:
    """Calculates profit/loss price targets given a current price and upside/downside percentages."""
    upside_target = round(current_price * (1 + upside_pct / 100), 2)
    downside_target = round(current_price * (1 - downside_pct / 100), 2)
    return {
        "current_price": current_price,
        "upside_pct": upside_pct,
        "downside_pct": downside_pct,
        "upside_target": upside_target,
        "downside_target": downside_target,
    }


def get_market_snapshot(ticker: str) -> dict:
    """Returns full market snapshot for any supported ticker: RSI, MA, volume, sentiment, volatility."""
    ticker = ticker.upper()
    if ticker not in STOCK_DB:
        return {"error": f"Ticker {ticker} not found. Available: AAPL, NVDA, TSLA"}
    d = STOCK_DB[ticker]
    rsi_map = {"AAPL": 72, "NVDA": 61, "TSLA": 45}
    return {
        "ticker": ticker,
        "price": d["price"],
        "change_perc": d["change_perc"],
        "volume": d["volume"],
        "rsi": rsi_map.get(ticker, 50),
        "ma_20": round(d["price"] * 0.995, 2),
        "ma_50": round(d["price"] * 0.956, 2),
        "sentiment": "POSITIVE" if d["change_perc"] > 0 else "NEGATIVE",
        "volatility": d["volatility"],
        "trend": "BULLISH" if d["change_perc"] > 0 else "BEARISH",
    }
