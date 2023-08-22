from plugp100.api.tapo_client import TapoClient
from plugp100.common.functional.either import Either
from plugp100.common.utils.json_utils import Json
from plugp100.requests.tapo_request import TapoRequest
from plugp100.responses.device_usage_info import DeviceUsageInfo


class _BaseTapoDevice:
    def __init__(self, api: TapoClient, address: str):
        self._api = api
        self._address = address

    async def login(self) -> Either[True, Exception]:
        return await self._api.login(self._address)

    async def get_device_usage(self) -> Either[DeviceUsageInfo, Exception]:
        """
        The function `get_device_usage` retrieves the usage information of a device and returns it as a JSON object or an
        exception.
        @return: an `Either` object, which can contain either a `Json` object or an `Exception`.
        """
        return (
            await self._api.execute_raw_request(TapoRequest.get_device_usage())
        ) | DeviceUsageInfo.try_from_json

    async def raw_command(self, method: str, params: Json) -> Either[Json, Exception]:
        """Execute raw command with given parameters.

        This is useful for testing new commands and payloads.
        """
        return await self._api.execute_raw_request(
            TapoRequest(method=method, params=params)
        )

    async def get_state_as_json(self) -> Either[Json, Exception]:
        return await self._api.get_device_info()
