from datetime import datetime

from bitcoinwallet.core.service.currency_api_client import ICurrencyApiClient
from definitions import FORMAT, SATOSHIS_PER_BITCOIN


def datetime_now() -> str:
    return datetime.now().strftime(FORMAT)


class CurrencyExchangeUtil:
    @staticmethod
    def bitcoin_to_satoshi(amount_in_btc: float) -> int:
        return int(amount_in_btc * SATOSHIS_PER_BITCOIN)

    @staticmethod
    def satoshi_to_bitcoin(amount_in_satoshi: int) -> float:
        return amount_in_satoshi / SATOSHIS_PER_BITCOIN

    @staticmethod
    def bitcoin_to_usd(
        amount_in_btc: float, btc_usd_currency_src_client: ICurrencyApiClient
    ) -> float:
        return btc_usd_currency_src_client.get_btc_to_usd_rate() * amount_in_btc
