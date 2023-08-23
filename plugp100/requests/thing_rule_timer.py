import dataclasses
from typing import Any


@dataclasses.dataclass
class ThingRuleTimer(object):
    delay: int
    desired_states: dict[str, Any]
    enable: bool
    remain: int
