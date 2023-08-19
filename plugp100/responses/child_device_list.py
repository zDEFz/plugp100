import base64
from dataclasses import dataclass
from typing import Any, Set, Callable, List, TypeVar

Child = TypeVar("Child")


@dataclass
class ChildDeviceList(object):
    child_device_list: list[dict[str, Any]]
    start_index: int
    sum: int

    @staticmethod
    def try_from_json(**kwargs):
        return ChildDeviceList(
            kwargs.get('child_device_list', []),
            kwargs.get('start_index', 0),
            kwargs.get('sum', 0)
        )

    def get_device_ids(self) -> Set[str]:
        return {child.get('device_id') for child in self.child_device_list if child.get('device_id', None) is not None}

    def get_children(self, parse: Callable[[dict[str, Any]], Child]) -> List[Child]:
        return list(map(lambda x: parse(x), self.child_device_list))


@dataclass
class PowerStripChild:
    brightness: int
    device_id: str
    original_device_id: str
    overheat: str
    position: int
    slotNumber: int
    device_on: bool
    nickname: str

    @staticmethod
    def try_from_json(**kwargs):
        return PowerStripChild(
            brightness=kwargs.get('brightness', 0),
            device_id=kwargs.get('device_id', ''),
            original_device_id=kwargs.get('original_device_id', ''),
            overheat=kwargs.get('overheat_status', 0),
            position=kwargs.get('position', -1),
            slotNumber=kwargs.get('slot_number', -1),
            device_on=kwargs.get('device_on', False),
            nickname=base64.b64decode(kwargs["nickname"]).decode("UTF-8"),

        )