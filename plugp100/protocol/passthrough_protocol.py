import logging
from time import time
from typing import Optional, Any

import aiohttp

from plugp100.common.credentials import AuthCredential
from plugp100.common.functional.tri import Try
from plugp100.common.transport.securepassthrough_transport import (
    Session,
    SecurePassthroughTransport,
)
from plugp100.common.utils.http_client import AsyncHttp
from plugp100.protocol.tapo_protocol import TapoProtocol
from plugp100.requests.tapo_request import TapoRequest
from plugp100.responses.tapo_exception import TapoException, TapoError
from plugp100.responses.tapo_response import TapoResponse

logger = logging.getLogger(__name__)


class PassthroughProtocol(TapoProtocol):
    def __init__(
        self,
        auth_credential: AuthCredential,
        host: str,
        port: Optional[int] = 80,
        http_session: Optional[aiohttp.ClientSession] = None,
        auto_recover_expired_session: bool = False,
    ):
        super().__init__(host, port)
        self._url = f"http://{host}:{port}/app"
        self._http = AsyncHttp(
            aiohttp.ClientSession() if http_session is None else http_session
        )
        self._auto_recover_expired_session = auto_recover_expired_session
        self._passthrough = SecurePassthroughTransport(self._http)
        self._session: Optional[Session] = None
        self._credential = auth_credential

    async def send_request(
        self, request: TapoRequest, retry: int = 3
    ) -> Try[TapoResponse[dict[str, Any]]]:
        login_response = (
            await self._login_with_version(retry=retry)
            if self._session is None or self._session.token is None
            else Try.of(True)
        )
        if login_response.is_success():
            request.with_terminal_uuid(
                self._session.terminal_uuid
            ).with_request_time_millis(round(time() * 1000))
            response = await self._passthrough.send(request, self._session)
            if retry > 0 and isinstance(response.error(), TapoException):
                if response.error().error_code == TapoError.ERR_SESSION_TIMEOUT.value:
                    self._session.invalidate()
                    logger.warning(
                        "Session timeout, invalidate it, retrying with new session"
                    )
                    return await self.send_request(request, retry - 1)
                elif response.error().error_code == TapoError.ERR_DEVICE.value:
                    self._session.invalidate()
                    logger.warning(
                        "Error device, probably exceeding rate limit, retrying with new session"
                    )
                    return await self.send_request(request, retry - 1)
            else:
                return response
        else:
            return login_response

    async def close(self):
        await self._http.close()
        self._session = None

    async def _login_with_version(
        self, use_v2: bool = False, retry: int = 3
    ) -> Try[True]:
        session_or_error = await self._passthrough.handshake(self._url)
        if session_or_error.is_success():
            self._session = session_or_error.get()
            if not self._session.is_handshake_session_expired():
                login_request = TapoRequest.login(
                    self._credential, v2=use_v2
                ).with_request_time_millis(round(time() * 1000))
                token = (await self._passthrough.send(login_request, self._session)).map(
                    lambda x: x.result["token"]
                )
                if token.is_success():
                    self._session.token = token.get()
                return token.map(lambda _: True)
            else:
                return await self._login_with_version(use_v2=use_v2)

        return session_or_error.map(lambda _: True)