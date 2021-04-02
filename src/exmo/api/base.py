from aiohttp import ClientSession
import time
import urllib
import hashlib
import hmac
import asyncio


class BaseExmoApi:
    """Base exmo api class."""

    _url = 'https://api.exmo.com/v1.1/{}'
    _headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self, session: ClientSession = None):
        if session is None:
            session = ClientSession()
        self._session = session
        self._session.headers.update(self._headers)

    async def _close_session(self):
        await self._session.close()

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        task = loop.create_task(self._close_session())
        loop.run_until_complete(task)


class PublicExmoCoreApi(BaseExmoApi):
    """Core class for public api usage."""

    async def _make_post(self, method: str, data: dict = None) -> dict:
        """Make post request to exmo api."""
        url = self._url.format(method)
        response = await self._session.post(url, data=data)
        return await response.json()

    async def _make_get(self, method: str, data: dict = None) -> dict:
        """Make get request to exmo api."""
        url = self._url.format(method)
        response = await self._session.get(url, params=data)
        return await response.json()


class AuthenticatedCoreApi(BaseExmoApi):
    """Core class for authenticated api usage."""

    # Keys for authentication.
    _api_key: str = None
    _api_secret: bytes = None

    # Authentication nonce.
    _nonce: int = None

    def authenticate(self, api_key: str, api_secret: str):
        self._api_key = api_key
        self._api_secret = api_secret.encode('utf-8')
        self._session.headers.update({'Key': self._api_key})
        self._nonce = int(round(time.time() * 1000))

    def _set_nonce(self):
        """Set nonce."""

        self._nonce += 1
        return self._nonce

    def _prepare_data(self, params: dict):
        """Prepare data post parameters for authenticated post request."""

        if params is None:
            params = dict()

        params['nonce'] = self._set_nonce()
        return params

    def _make_sign(self, params):
        """Make sign with post parameters."""
        payload_bytes = urllib.parse.urlencode(params).encode('utf-8')
        sign = hmac.new(self._api_secret, payload_bytes,
                        hashlib.sha512).hexdigest()
        return sign

    async def _make_authenticated_post(self, method, data: dict = None):
        """Make authenticated post request to exmo api."""

        url = self._url.format(method)
        params = self._prepare_data(data)
        sign = self._make_sign(params)
        response = await self._session.post(url,
                                            data=params,
                                            headers={'Sign': sign})
        return await response.json()
