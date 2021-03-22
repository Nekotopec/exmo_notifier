from aiohttp import ClientSession


class BaseExmoApi:
    """Base exmo api class."""

    _url = 'https://api.exmo.com/v1.1/{}'

    def __init__(self, session: ClientSession):
        self._session = session

    async def _make_post(self, method: str, data: dict = None) -> dict:
        """Make post request to exmo api."""
        url = self._url.format(method)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = await self._session.post(url, headers=headers, data=data)
        return await response.json()

    async def _make_get(self, method: str, data: dict = None) -> dict:
        """Make get request to exmo api."""
        url = self._url.format(method)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = await self._session.get(url, headers=headers, params=data)
        return await response.json()
