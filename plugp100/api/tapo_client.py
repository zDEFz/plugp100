import asyncio
import logging
from time import time
from typing import Optional, Any, cast

import aiohttp

from plugp100.api.light_effect import LightEffect
from plugp100.common.functional.tri import Try, Success, Failure
from plugp100.common.transport.securepassthrough_transport import (
    SecurePassthroughTransport,
    Session,
)
from plugp100.common.utils.http_client import AsyncHttp
from plugp100.common.utils.json_utils import dataclass_encode_json, Json
from plugp100.requests.tapo_request import TapoRequest, MultipleRequestParams
from plugp100.responses.child_device_list import ChildDeviceList
from plugp100.responses.energy_info import EnergyInfo
from plugp100.responses.power_info import PowerInfo
from plugp100.responses.tapo_exception import TapoException, TapoError
from plugp100.responses.tapo_response import TapoResponse

logger = logging.getLogger(__name__)


class TapoClient:
    def __init__(
        self,
        username: str,
        password: str,
        http_session: Optional[aiohttp.ClientSession] = None,
        auto_recover_expired_session: bool = False,
    ):
        self._auto_recover_session = auto_recover_expired_session
        self._username = username
        self._password = password
        self._http = AsyncHttp(
            aiohttp.ClientSession() if http_session is None else http_session
        )
        self._session: Optional[Session] = None
        self._passthrough = SecurePassthroughTransport(self._http)

    async def close(self):
        await self._http.close()

    async def login(self, url: str) -> Try[True]:
        """
        The function `login` attempts to log in to an API using a given address and returns either `True` if successful or
        an `Exception` if there is an error.
        @return: The login method is returning an Either type, which can either be True or an Exception.
        """
        self._session = None
        login_result = await self._login_with_version(
            url, self._username, self._password, use_v2=False
        )
        if login_result.is_failure():
            return await self._login_with_version(
                url, self._username, self._password, use_v2=True
            )
        return login_result

    async def execute_raw_request(self, request: "TapoRequest") -> Try[Json]:
        request.with_terminal_uuid(self._session.terminal_uuid).with_request_time_millis(
            round(time() * 1000)
        )
        return (await self._send_safe_passthrough(request)).map(lambda x: x.result)

    async def get_device_info(self) -> Try[Json]:
        """
        The function `get_device_info` sends a request to retrieve device information and returns the result or an
        exception.
        @return: an `Either` object that contains either a `Json` object or an `Exception`.
        """
        get_info_request = TapoRequest.get_device_info()
        return (await self._send_safe_passthrough(get_info_request)).map(
            lambda x: x.result
        )

    async def get_energy_usage(self) -> Try[EnergyInfo]:
        """
        The function `get_energy_usage` makes a request to get energy usage information and returns either the energy info
        or an exception.
        @return: an `Either` type, which can either contain an `EnergyInfo` object or an `Exception` object.
        """
        get_energy_request = TapoRequest.get_energy_usage()
        response = await self._send_safe_passthrough(get_energy_request)
        return response.map(lambda x: EnergyInfo(x.result))

    async def get_current_power(self) -> Try[PowerInfo]:
        """
        The function `get_current_power` asynchronously retrieves the current power information and returns it as a
        `PowerInfo` object, or an `Exception` if an error occurs.
        @return: an `Either` object that contains either a `PowerInfo` object or an `Exception`.
        """
        get_current_power = TapoRequest.get_current_power()
        response = await self._send_safe_passthrough(get_current_power)
        return response.map(lambda x: PowerInfo(x.result))

    async def set_device_info(self, device_info: Any) -> Try[True]:
        """
        The function `set_device_info` encodes the `device_info` object into JSON format and returns either `True` or an
        `Exception`.

        @param device_info: The `device_info` parameter is an object that contains information about a device. It is passed
        to the `set_device_info` method as an argument
        @return: an `Either` type, which can either be `True` or an `Exception`.
        """
        return await self._set_device_info(dataclass_encode_json(device_info))

    async def set_lighting_effect(self, light_effect: LightEffect) -> Try[True]:
        """
        The function `set_lighting_effect` sets a lighting effect for a device and returns either `True` or an exception.

        @param light_effect: The `light_effect` parameter is of type `LightEffect`. It represents the desired lighting
        effect that you want to set for a device
        @type light_effect: LightEffect
        @return: an `Either` object that contains either a `True` value or an `Exception`.
        """
        request = (
            TapoRequest.set_lighting_effect(light_effect)
            .with_terminal_uuid(self._session.terminal_uuid)
            .with_request_time_millis(round(time() * 1000))
        )
        response = await self._send_safe_passthrough(request)
        return response.map(lambda _: True)

    async def get_child_device_list(self) -> Try[ChildDeviceList]:
        """
        The function `get_child_device_list` retrieves a list of child devices asynchronously and returns either the list or
        an exception.
        @return: an `Either` object, which can contain either a `ChildDeviceList` or an `Exception`.
        """
        request = (
            TapoRequest.get_child_device_list()
            .with_terminal_uuid(self._session.terminal_uuid)
            .with_request_time_millis(round(time() * 1000))
        )
        return (await self._send_safe_passthrough(request)).map(
            lambda x: ChildDeviceList.try_from_json(**x.result)
        )

    async def get_child_device_component_list(self) -> Try[Json]:
        """
        The function `get_child_device_component_list` retrieves a list of child device components asynchronously and
        returns either the JSON response or an exception.
        @return: an `Either` object, which can contain either a `Json` object or an `Exception`.
        """
        request = (
            TapoRequest.get_child_device_component_list()
            .with_terminal_uuid(self._session.terminal_uuid)
            .with_request_time_millis(round(time() * 1000))
        )
        return (await self._send_safe_passthrough(request)).map(lambda x: x.result)

    async def control_child(self, child_id: str, request: TapoRequest) -> Try[Json]:
        """
        The function `control_child` is an asynchronous method that sends a control request to a child device and returns
        the response or an exception.

        @param child_id: The `child_id` parameter is a string that represents the ID of a child device
        @type child_id: str
        @param request: The `request` parameter is an instance of the `TapoRequest` class. It represents a request to be
        sent to the Tapo device.
        @type request: TapoRequest
        @return: an instance of the `Either` class, which can contain either a `Json` object or an `Exception`.
        """
        multiple_request = (
            TapoRequest.multiple_request(MultipleRequestParams([request]))
            .with_terminal_uuid(self._session.terminal_uuid)
            .with_request_time_millis(round(time() * 1000))
        )
        request = TapoRequest.control_child(child_id, multiple_request)
        response = await self._send_safe_passthrough(request)
        if response.is_success():
            try:
                responses = response.get().result["responseData"]["result"]["responses"]
                if len(responses) > 0:
                    return (
                        Success(responses[0]["result"])
                        if "result" in responses[0]
                        else Success(responses[0])
                    )
                else:
                    return Failure(Exception("Empty responses from child"))
            except Exception as e:
                return Failure(e)
        return cast(Failure, response)

    async def _set_device_info(self, device_info: Json) -> Try[True]:
        request = (
            TapoRequest.set_device_info(device_info)
            .with_terminal_uuid(self._session.terminal_uuid)
            .with_request_time_millis(round(time() * 1000))
        )
        response = await self._send_safe_passthrough(request)
        return response.map(lambda _: True)

    async def _send_safe_passthrough(
        self, request: TapoRequest, is_retry: bool = False
    ) -> Try[TapoResponse[dict[str, Any]]]:
        """
        Send a passthrough request by renewing session if expired.
        @param request:
        @return:
        """
        response = await self._passthrough.send(request, self._session)

        if (
            self._auto_recover_session
            and not is_retry
            and isinstance(response.error(), TapoException)
        ):
            if response.error().error_code == TapoError.ERR_SESSION_TIMEOUT.value:
                logger.warning(
                    "Session timeout, invalidate it, trying new login and request"
                )
                return await self.retry_with_new_session(request)
            elif response.error().error_code == TapoError.ERR_DEVICE.value:
                logger.warning(
                    "Error device, probably exceeding rate limit, creating new session"
                )
                return await self.retry_with_new_session(request)

        else:
            return response

    async def _login_with_version(
        self, ip_address: str, username: str, password: str, use_v2: bool = False
    ) -> Try[True]:
        """
        The `login` function performs a handshake with a given URL, and if successful, sends a login request with a username
        and password, returning a token if successful or an exception if not.

        @param ip_address: The `ip_address` parameter is a string that represents the IP ADDRESS of the login endpoint
        @type ip_address: str
        @param use_v2: If should login by using v2 api
        @type use_v2: bool
        @return: The login function returns an Either type, which can either be a Right containing True if the login is
        successful, or a Right containing an Exception if there is an error during the login process.
        """
        session_or_error = await self._passthrough.handshake(ip_address)
        if session_or_error.is_success():
            self._session = session_or_error.get()
            if not self._session.is_handshake_session_expired():
                login_request = (
                    TapoRequest.login_v2(username, password)
                    if use_v2 is True
                    else TapoRequest.login(username, password)
                ).with_request_time_millis(round(time() * 1000))
                token = (await self._send_safe_passthrough(login_request)).map(
                    lambda x: x.result["token"]
                )
                if token.is_success():
                    self._session.token = token.get()
                return token.map(lambda _: True)
            else:
                return await self._login_with_version(
                    ip_address, username, password, use_v2=use_v2
                )

        return session_or_error.map(lambda _: True)

    async def retry_with_new_session(self, request: TapoRequest):
        self._session.invalidate()
        return (await self.login(self._session.ip_address)).flat_map(
            lambda _: asyncio.run(self._send_safe_passthrough(request, is_retry=True))
        )
