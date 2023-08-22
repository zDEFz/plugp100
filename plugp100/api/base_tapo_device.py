from plugp100.api.tapo_client import TapoClient
from plugp100.common.functional.tri import Try
from plugp100.common.utils.json_utils import Json
from plugp100.requests.tapo_request import TapoRequest
from plugp100.responses.device_usage_info import DeviceUsageInfo


class _BaseTapoDevice:
    def __init__(self, api: TapoClient, address: str):
        self._api = api
        self._address = address

    async def login(self) -> Try[True]:
        return await self._api.login(self._address)

    async def get_device_usage(self) -> Try[DeviceUsageInfo]:
        """
        The function `get_device_usage` retrieves the usage information of a device and returns it as a JSON object or an
        exception.
        @return: an `Either` object, which can contain either a `Json` object or an `Exception`.
        """
        return (
            await self._api.execute_raw_request(TapoRequest.get_device_usage())
        ).flat_map(DeviceUsageInfo.try_from_json)

    async def raw_command(self, method: str, params: Json) -> Try[Json]:
        """Execute raw command with given parameters.

        This is useful for testing new commands and payloads.
        """
        return await self._api.execute_raw_request(
            TapoRequest(method=method, params=params)
        )

    async def get_state_as_json(self) -> Try[Json]:
        return await self._api.get_device_info()
