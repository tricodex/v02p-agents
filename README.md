# v02p-agents

Portfolio Management Agent using CDP AgentKit

## Overview

This project implements an automated portfolio management agent using the Coinbase Developer Platform (CDP) AgentKit. It provides functionality for:

- Portfolio tracking and statistics
- Trade execution
- Automated rebalancing
- Position size management

## Installation

1. Install dependencies using Poetry:
```bash
poetry install
```

2. Set up environment variables:
```bash
export CDP_API_KEY_NAME=your-api-key-name
export CDP_API_KEY_PRIVATE_KEY=your-private-key
```

## Usage

```python
from src.portfolio_agent import PortfolioManager, PortfolioConfig
from cdp_langchain.utils import CdpAgentkitWrapper

# Initialize CDP wrapper
cdp_wrapper = CdpAgentkitWrapper(
    network_id="base-sepolia",
    cdp_api_key_name="your-api-key-name",
    cdp_api_key_private_key="your-api-key-private-key"
)

# Create portfolio config
config = PortfolioConfig(
    target_assets=["ETH", "USDC"],
    target_allocation={"ETH": 0.5, "USDC": 0.5}
)

# Initialize portfolio manager
portfolio_manager = PortfolioManager(cdp_wrapper, config)

# Get portfolio stats
stats = await portfolio_manager.get_portfolio_stats()
print(f"Portfolio value: ${stats['total_value_usd']}")
```

## Features

- Portfolio statistics and tracking
- Automated trade execution
- Portfolio rebalancing
- Position size limits
- Slippage protection

## Development

1. Install development dependencies:
```bash
poetry install --with dev
```

2. Run tests:
```bash
poetry run pytest
```

## License

MIT