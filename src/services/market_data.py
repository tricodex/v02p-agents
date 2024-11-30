"""Market data service for price feeds."""
from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime
import aiohttp
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class PriceData(BaseModel):
    """Price data model."""
    price: Decimal
    timestamp: datetime
    volume_24h: Optional[Decimal]
    change_24h: Optional[float]
    source: str

class MarketDataService:
    """Service for fetching market data."""
    
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self._session: Optional[aiohttp.ClientSession] = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
    
    async def get_price_data(self, asset_id: str) -> PriceData:
        """Get current price for an asset."""
        try:
            if self.mock_mode:
                return self._get_mock_price(asset_id)
            
            await self._ensure_session()
            
            # Map asset IDs to CoinGecko IDs
            cg_id = {
                'ETH': 'ethereum',
                'BTC': 'bitcoin',
                'USDC': 'usd-coin'
            }.get(asset_id.upper())
            
            if not cg_id:
                raise ValueError(f"Unknown asset: {asset_id}")
                
            # Fetch from CoinGecko
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': cg_id,
                'vs_currencies': 'usd',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true'
            }
            
            async with self._session.get(url, params=params) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch price: {await response.text()}")
                    
                data = await response.json()
                coin_data = data[cg_id]
                
                return PriceData(
                    price=Decimal(str(coin_data['usd'])),
                    timestamp=datetime.utcnow(),
                    volume_24h=Decimal(str(coin_data['usd_24h_vol'])),
                    change_24h=float(coin_data['usd_24h_change']),
                    source='coingecko'
                )
                
        except Exception as e:
            logger.error(f"Error fetching price for {asset_id}: {str(e)}")
            raise
    
    def _get_mock_price(self, asset_id: str) -> PriceData:
        """Get mock price data for development."""
        mock_prices = {
            "ETH": {"price": "2000", "change": 5.2, "volume": "1000000000"},
            "BTC": {"price": "40000", "change": 3.1, "volume": "5000000000"},
            "USDC": {"price": "1", "change": 0.0, "volume": "10000000000"}
        }
        
        price_data = mock_prices.get(asset_id.upper(), {
            "price": "0",
            "change": 0.0,
            "volume": "0"
        })
        
        return PriceData(
            price=Decimal(price_data["price"]),
            timestamp=datetime.utcnow(),
            volume_24h=Decimal(price_data["volume"]),
            change_24h=price_data["change"],
            source="mock"
        )
        
    async def close(self):
        """Close any open connections."""
        if self._session and not self._session.closed:
            await self._session.close()