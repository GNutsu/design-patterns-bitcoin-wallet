import requests
from abc import ABC, abstractmethod
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=300)

class ICurrencyApiClient(ABC):
    @abstractmethod
    def get_btc_to_usd_rate(self) -> float:
        pass


class CoinGeckoApiClient(ICurrencyApiClient):
    def __init__(self, url="https://api.coingecko.com/api/v3/simple/price"):
        self.base_url = url


    @cached(cache)
    def get_btc_to_usd_rate(self) -> float:
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }
        response = requests.get(self.base_url
                                , params=params)
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['usd']