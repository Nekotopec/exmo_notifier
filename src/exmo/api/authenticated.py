from base import AuthenticatedCoreApi
from aiohttp import ClientSession
import asyncio
from settings import EXMO_API_KEY, EXMO_API_SECRET_KEY
from typing import List


class AuthenticateApiException(Exception):
    """Exception of authenticated api."""
    pass


class BadOrderType(AuthenticateApiException):
    """Bad order type exception."""


class AuthenticatedExmoApi(AuthenticatedCoreApi):
    """Exmo authenticated api."""

    TYPES = {'sell', 'buy'}
    EXTENDED_TYPES = TYPES | {'market_buy', 'market_sell', 'market_buy_total',
                              'market_sell_total'}

    def _check_types(self, type_):
        """Check for types of orders."""

        if type_ not in self.TYPES:
            raise BadOrderType('Order type must be one of following values:\n'
                               '    `buy`, `sell`\n'
                               f'   but not {type_}')

    def _check_extended_types(self, type_):
        """Check for extended types."""

        if type_ not in self.EXTENDED_TYPES:
            raise BadOrderType('Order type must be one of following values:\n'
                               '    `buy`, `sell`, `market_buy`, '
                               '`market_sell`, `market_buy_total`, '
                               '`market_sell_total`\n'
                               f'   but not {type_}')

    async def user_info(self):
        """Getting information about user's account."""

        method = 'user_info'
        return await self._make_authenticated_post(method)

    async def order_create(self,
                           pair: str,
                           quantity: float,
                           price: float,
                           type_: str,
                           client_id: int = None):
        """Order creation.

        Args:
            pair (str): currency pair
            quantity (float): quantity for the order
            price (float): price for the order
            type_ (str): type of order, can have the following values:
                'sell', 'buy', 'market_buy', 'market_sell', 'market_buy_total',
                'market_sell_total'
            client_id (int): client id for the order (optional parameter,
                must be a positive integer)
        """

        self._check_extended_types(type_)

        method = 'order_create'
        data = {
            'pair': pair,
            'quantity': quantity,
            'price': price,
            'type': type_
        }
        if client_id is not None:
            data['client_id'] = client_id

        return await self._make_authenticated_post(method, data)

    async def order_cancel(self, order_id: int):
        """Order cancellation.

        Args:
            order_id (int): order identifier
        """

        method = 'order_cancel'
        data = {
            'order_id': order_id
        }
        return await self._make_authenticated_post(method, data)

    async def stop_market_order_create(self,
                                       pair: str,
                                       quantity: float,
                                       trigger_price: float,
                                       type_: str,
                                       client_id: int):
        """Stop market order creation.

        Args:
            pair (str): currency pair
            quantity (float): quantity for the order
            trigger_price (float): price for the order
            type_ (str): type of order, can have the following values:
                'buy', 'sell'
            client_id (int): client id for the order
                (optional parameter, must be a positive integer)
        """

        self._check_types(type_)

        method = 'stop_market_order_create'
        data = {
            'pair': pair,
            'quantity': quantity,
            'trigger_price': trigger_price,
            'type': type_,
            'client_id': client_id
        }
        return await self._make_authenticated_post(method, data)

    async def stop_market_order_cancel(self, parent_order_id: int):
        """Stop market order cancellation.

        Args:
            parent_order_id: stop market order identifier
        """

        method = 'stop_market_order_cancel'
        data = {
            'parent_order_id': parent_order_id
        }
        return await self._make_authenticated_post(method, data)

    async def user_open_orders(self):
        """Getting the list of user’s active orders."""

        method = 'user_open_orders'
        return self._make_authenticated_post(method)

    async def user_trades(self,
                          pair: List[str],
                          limit: int = 100,
                          offset: int = 0):
        """Getting the list of user’s deals.

        Args:
            pair: one or various currency pairs separated by commas
            limit: the number of returned deals (default: 100, maximum: 100)
            offset: last deal offset (default: 0)
        """

        method = 'user_trades'
        data = {
            'pair': ','.join(pair),
            'limit': limit,
            'offset': offset
        }
        return await self._make_authenticated_post(method, data)

    async def user_cancelled_orders(self,
                                    limit: int = 100,
                                    offset: int = 0):
        """Getting the list of user’s cancelled orders.

        Args:
            limit: the number of returned deals (default: 100, maximum: 10 000)
            offset: last deal offset (default: 0)
        """

        method = 'user_cancelled_orders'
        data = {
            'limit': limit,
            'offset': offset
        }
        return await self._make_authenticated_post(method, data)

    async def order_trades(self,
                           order_id: int):
        """Getting the history of deals with the order.

        Args:
            order_id: order identifier
        """

        method = 'order_trades'
        data = {'order_id': order_id}
        return await self._make_authenticated_post(method, data)

    async def deposit_address(self):
        """Getting the list of addresses for cryptocurrency deposit."""

        method = 'deposit_address'
        return await self._make_authenticated_post(method)

    async def withdraw_crypt(self,
                             amount: float,
                             currency: str,
                             address: str,
                             invoice: int = None,
                             transport: str = None):
        """Creation of the task for cryptocurrency withdrawal.
        ATTENTION!!! This API function is available only after request to
        the Technical Support.

        Args:
            amount: Amount of currency to be withdrawn (required)
            currency: Name of the currency to be withdrawn (required)
            address: Withdrawal address (required)
            invoice: Additional identifier (optional)
            transport: The network in which the withdrawal will be made.
                If you do not specify, then the default network will be
                selected. Explanation: some currencies exist in several
                blockchains, and you can specify in which blockchain you want
                to withdraw tokens. (optional)
        """

        method = 'withdraw_crypt'
        data = {
            amount: amount,
            currency: currency,
            address: address,
        }
        if invoice:
            data['invoice'] = invoice
        if transport:
            data['transport'] = transport

        return await self._make_authenticated_post(method, data)

    async def withdraw_get_txid(self, task_id: int):
        """Getting the transaction ID in order to keep track of it on
        blockchain.

        Args:
            task_id: withdrawal task identifier
        """

        method = 'withdraw_get_txid'
        data = {'task_id': task_id}
        return await self._make_authenticated_post(method, data)


async def test():
    async with ClientSession() as session:
        api = AuthenticatedExmoApi(session)
        api.authenticate(api_key=EXMO_API_KEY,
                         api_secret=EXMO_API_SECRET_KEY)
        data = await api.stop_market_order_create()
        print(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(test())
    loop.run_until_complete(task)
