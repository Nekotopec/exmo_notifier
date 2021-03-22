from base import BaseExmoApi
from typing import List, Union
import asyncio
from aiohttp import ClientSession


class ExmoPublicApiException(Exception):
    """Exception of Exmo public api"""
    pass


class BadResolution(ExmoPublicApiException):
    """Resolution not in allowed resolution values."""


class PublicExmoApi(BaseExmoApi):
    """
    This API does not require authorization and can be accessed using the
    GET or POST methods.
    """

    _resolution_allowed_values = {
        1, 5, 15, 30, 45, 60, 120, 180, 240, 'D', 'W', 'M',
    }

    async def trades(self, pairs: List[str]) -> dict:
        """List of the deals on currency pairs."""

        method = 'trades'
        data = {'pair': ','.join(pairs)}
        return await self._make_post(method, data)

    async def order_book(self, pairs: List[str], limit: int = None) -> dict:
        """The book of current orders on the currency pair."""

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
        """Get candles history."""
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
