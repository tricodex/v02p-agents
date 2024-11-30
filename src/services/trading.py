"""Trading execution service."""
from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime
import logging
from pydantic import BaseModel
from cdp import Wallet
from ..core.constants import DEFAULT_SLIPPAGE, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

class TradeResult(BaseModel):
    """Result of trade execution."""
    status: str  # 'completed', 'failed'
    transaction_hash: Optional[str]
    transaction_link: Optional[str]
    execution_price: Optional[Decimal]
    amount: Decimal
    side: str
    asset_id: str
    gas_used: Optional[Decimal]
    error_message: Optional[str]
    timestamp: datetime = datetime.utcnow()

class TradingService:
    """Service for executing trades using CDP."""
    
    def __init__(self, wallet: Wallet):
        self.wallet = wallet
        
    async def execute_trade(
        self,
        asset_id: str,
        amount: str,
        side: str,
        max_slippage: float = DEFAULT_SLIPPAGE
    ) -> TradeResult:
        """Execute a trade using CDP AgentKit.
        
        Args:
            asset_id: Asset to trade (e.g. 'ETH', 'USDC')
            amount: Amount to trade as string
            side: 'buy' or 'sell'
            max_slippage: Maximum acceptable slippage
            
        Returns:
            TradeResult with execution details
        """
        try:
            # Execute trade
            if side.lower() == "buy":
                trade = await self.wallet.trade(
                    amount=amount,
                    from_asset_id="usdc",
                    to_asset_id=asset_id.lower()
                )
            else:
                trade = await self.wallet.trade(
                    amount=amount,
                    from_asset_id=asset_id.lower(), 
                    to_asset_id="usdc"
                )
            
            # Wait for confirmation
            result = await trade.wait()
            
            return TradeResult(
                status="completed",
                transaction_hash=result.transaction.transaction_hash,
                transaction_link=result.transaction.transaction_link,
                execution_price=result.execution_price,
                amount=Decimal(amount),
                side=side,
                asset_id=asset_id,
                gas_used=result.gas_used
            )
            
        except Exception as e:
            logger.error(f"Trade execution failed: {str(e)}")
            return TradeResult(
                status="failed",
                amount=Decimal(amount),
                side=side,
                asset_id=asset_id,
                error_message=str(e)
            )
    
    async def check_balances(self, asset_ids: list[str]) -> Dict[str, Decimal]:
        """Check balances for multiple assets."""
        balances = {}
        for asset_id in asset_ids:
            try:
                balance = await self.wallet.balance(asset_id.lower())
                balances[asset_id] = balance
            except Exception as e:
                logger.error(f"Error getting balance for {asset_id}: {str(e)}")
                balances[asset_id] = Decimal(0)
        return balances