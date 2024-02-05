from abc import ABC, abstractmethod

from bitcoinwallet.core.service.currency_api_client import ICurrencyApiClient


class ICurrencyConversionService(ABC):
    @abstractmethod
    def btc_to_usd(self, btc_amount: float) -> float:
        pass

    @abstractmethod
    def usd_to_btc(self, usd_amount: float) -> float:
        pass


class CurrencyConversionService(ICurrencyConversionService):
    def __init__(self, api_client: ICurrencyApiClient):
        self.api_client = api_client

    def btc_to_usd(self, btc_amount: float) -> float:
        rate = self.api_client.get_btc_to_usd_rate()
        return btc_amount * rate

    def usd_to_btc(self, usd_amount: float) -> float:
        rate = self.api_client.get_btc_to_usd_rate()
        return usd_amount / rate if rate else 0
