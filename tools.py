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


