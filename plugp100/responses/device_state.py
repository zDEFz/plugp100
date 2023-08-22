import base64
from dataclasses import dataclass
from typing import Optional, Any

import semantic_version

from plugp100.api.light_effect import LightEffect
from plugp100.common.functional.tri import Try


class DeviceState:
    pass


@dataclass
class PlugDeviceState(DeviceState):
    info: "DeviceInfo"
    device_on: bool

    @staticmethod
    def try_from_json(kwargs: dict[str, Any]) -> Try["PlugDeviceState"]:
        return Try.of(
            lambda: PlugDeviceState(
                info=DeviceInfo(**kwargs),
                device_on=kwargs.get("device_on", False),
            )
        )


@dataclass
class LightDeviceState(DeviceState):
    info: "DeviceInfo"
    device_on: bool
    brightness: Optional[int]
    hue: Optional[int]
    saturation: Optional[int]
    color_temp: Optional[int]

    @staticmethod
    def try_from_json(kwargs: dict[str, Any]) -> Try["LightDeviceState"]:
        return Try.of(
            lambda: LightDeviceState(
                info=DeviceInfo(**kwargs),
                device_on=kwargs.get("device_on", False),
                brightness=kwargs.get("brightness", None),
                hue=kwargs.get("hue", None),
                saturation=kwargs.get("saturation", None),
                color_temp=kwargs.get("color_temp", None),
            )
        )


@dataclass
class LedStripDeviceState(DeviceState):
    info: "DeviceInfo"
    device_on: bool
    brightness: Optional[int]
    hue: Optional[int]
    saturation: Optional[int]
    color_temp: Optional[int]
    lighting_effect: Optional[LightEffect]

    @staticmethod
    def try_from_json(kwargs: dict[str, Any]) -> Try["LedStripDeviceState"]:
        return Try.of(
            lambda: LedStripDeviceState(
                info=DeviceInfo(**kwargs),
                device_on=kwargs.get("device_on", False),
                brightness=kwargs.get("brightness", None),
                hue=kwargs.get("hue", None),
                saturation=kwargs.get("saturation", None),
                color_temp=kwargs.get("color_temp", None),
                lighting_effect=LightEffect(**kwargs.get("lighting_effect"))
                if "lighting_effect" in kwargs
                else None,
            )
        )


@dataclass
class DeviceInfo:
    device_id: str
    firmware_version: str
    hardware_version: str
    mac: str
    nickname: str
    model: str
    type: str
    overheated: bool
    signal_level: int
    rssi: int
    friendly_name: str
    is_hardware_v2: bool = property(lambda self: self.hardware_version == "2.0")

    def __init__(self, **kwargs):
        self.device_id = kwargs["device_id"]
        self.firmware_version = kwargs["fw_ver"]
        self.hardware_version = kwargs["hw_ver"]
        self.mac = kwargs["mac"]
        self.nickname = base64.b64decode(kwargs["nickname"]).decode("UTF-8")
        self.model = kwargs["model"]
        self.type = kwargs["type"]
        self.overheated = kwargs.get("overheated", False)
        self.signal_level = kwargs.get("signal_level", 0)
        self.rssi = kwargs.get("rssi", 0)
        self.friendly_name = self.model if self.nickname == "" else self.nickname

    def get_semantic_firmware_version(self) -> semantic_version.Version:
        pieces = self.firmware_version.split("Build")
        try:
            if len(pieces) > 0:
                return semantic_version.Version(pieces[0].strip())
            else:
                return semantic_version.Version("0.0.0")
        except ValueError:
            return semantic_version.Version("0.0.0")


@dataclass
class HubDeviceState(DeviceState):
    info: "DeviceInfo"
    in_alarm: bool

    @staticmethod
    def try_from_json(kwargs: dict[str, Any]) -> Try["HubDeviceState"]:
        return Try.of(
            lambda: HubDeviceState(
                info=DeviceInfo(**kwargs),
                in_alarm=kwargs.get("in_alarm", False),
            )
        )
