from abc import ABC, abstractmethod
from typing import Any, TypeVar

import requests
from cachetools import TTLCache, cached

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from definitions import (
    CACHE_TTL,
    CURRENCY_CACHE_MAX_SIZE,
    GECKO_CURRENCY_BASE_URL,
    INITIAL_USD_RATE,
)

# Cache
cache: TTLCache[Any, float] = TTLCache(maxsize=CURRENCY_CACHE_MAX_SIZE, ttl=CACHE_TTL)
TCurrencyApiClient = TypeVar("TCurrencyApiClient", bound="CurrencyApiClient")


class ICurrencyApiClient(ABC):
    @abstractmethod
    def get_btc_to_usd_rate(self) -> float:
        pass


class CurrencyApiClient(ICurrencyApiClient):
    def __init__(
        self,
        url: str = GECKO_CURRENCY_BASE_URL,
        logger: ILogger = ConsoleLogger("CurrencyApiClient"),
    ) -> None:
        self.base_url = url
        self.logger = logger
        self.last_execution_result = INITIAL_USD_RATE

    @cached(cache)
    def get_btc_to_usd_rate(self) -> float:
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            result = float(data["bitcoin"]["usd"])
            self.last_execution_result = result
            return result
        except Exception as e:
            self.logger.error(f"Error fetching BTC to USD rate: {e}")
            return self.last_execution_result


class NullCurrencyApiClient(ICurrencyApiClient):
    def __init__(self) -> None:
        pass

    def get_btc_to_usd_rate(self) -> float:
        return 0.0
