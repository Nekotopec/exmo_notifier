from .base import PublicExmoCoreApi
from typing import List, Union


class ExmoPublicApiException(Exception):
    """Exception of Exmo public api"""
    pass


class BadResolution(ExmoPublicApiException):
    """Resolution not in allowed resolution values."""


class PublicExmoApi(PublicExmoCoreApi):
    """
    This API does not require authorization and can be accessed using the
    GET or POST methods.
    """

    _resolution_allowed_values = {
        1, 5, 15, 30, 45, 60, 120, 180, 240, 'D', 'W', 'M',
    }

    async def trades(self, pairs: List[str]) -> dict:
        """List of the deals on currency pairs.

        Args:
            pairs: one or various currency pairs separated by commas
        """

        method = 'trades'
        data = {'pair': ','.join(pairs)}
        return await self._make_post(method, data)

    async def order_book(self, pairs: List[str], limit: int = None) -> dict:
        """The book of current orders on the currency pair.

        Args:
            pairs: one or various currency pairs separated by commas
            limit: the number of displayed positions (default: 100, max: 1000)
        """

        method = 'order_book'
        data = {
            'pair': ','.join(pairs),
        }

        if limit:
            data['limit'] = limit

        return await self._make_post(method, data)

    async def ticker(self) -> dict:
        """Statistics on prices and volume of trades by currency pairs."""

        method = 'ticker'
        return await self._make_post(method)

    async def pair_settings(self) -> dict:
        """Currency pairs settings."""

        method = 'pair_settings'
        return await self._make_post(method)

    async def currency(self) -> dict:
        """Currencies list."""

        method = 'currency'
        return await self._make_post(method)

    async def currency_list_extended(self) -> dict:
        """Extended list of currencies."""

        method = 'currency/list/extended'
        return await self._make_get(method)

    async def required_amount(self, pair: str,
                              quantity: Union[float, int]) -> dict:
        """
        Calculating the sum of buying a certain amount of currency for
        the particular currency pair.

        Args:
            pair: currency pair
            quantity: quantity to buy
        """

        method = 'required_amount'
        data = {
            'pair': pair,
            'quantity': quantity
        }
        return await self._make_post(method, data)

    async def candles_history(self,
                              pair: str,
                              resolution: Union[int, str],
                              from_: int,
                              to: int):
        """Get candles history.

        Args:
            pair: currency pair
            resolution: discreteness of candles, possible values: 1, 5, 15, 30,
                45, 60, 120, 180, 240, D, W, M
            from_: beginning of period
            to: end of period
        """

        if resolution not in self._resolution_allowed_values:
            raise BadResolution(
                f'`resolution` must be one of {self._resolution_allowed_values}'
            )
        method = 'candles_history'
        data = {
            'symbol': pair,
            'resolution': resolution,
            'from': from_,
            'to': to

        }
        return await self._make_get(method, data)

    async def payments_providers_crypto_list(self):
        """Crypto providers list."""

        method = 'payments/providers/crypto/list'
        return await self._make_get(method)
