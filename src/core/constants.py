"""Shared constants."""

SUPPORTED_ASSETS = {
    "ETH": {
        "name": "Ethereum",
        "decimals": 18,
        "min_trade_size": "0.01"
    },
    "USDC": {
        "name": "USD Coin",
        "decimals": 6,
        "min_trade_size": "10"
    },
    "BTC": {
        "name": "Bitcoin",
        "decimals": 8,
        "min_trade_size": "0.001"
    }
}

DEFAULT_SLIPPAGE = 0.01  # 1%
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds