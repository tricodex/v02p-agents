"""Core configuration and settings."""
from typing import Dict, List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class RiskLimits(BaseModel):
    """Risk management limits."""
    max_position_size: float = Field(default=0.4, ge=0, le=1)
    max_portfolio_var: float = Field(default=0.15, ge=0)
    max_concentration: float = Field(default=0.5, ge=0, le=1)
    min_liquidity_score: float = Field(default=0.7, ge=0, le=1)

class PortfolioConfig(BaseModel):
    """Portfolio configuration."""
    target_assets: List[str]
    target_allocation: Dict[str, float]
    rebalancing_threshold: float = Field(default=0.02, ge=0, le=1)
    max_single_trade_size: Decimal = Field(default=Decimal("10000"))
    auto_rebalancing: bool = Field(default=True)
    risk_limits: Optional[RiskLimits] = None

class Settings(BaseModel):
    """Application settings."""
    CDP_API_KEY_NAME: str 
    CDP_API_KEY_PRIVATE_KEY: str
    NETWORK_ID: str = "base-sepolia"
    MOCK_PRICES: bool = True
    DEBUG: bool = True
