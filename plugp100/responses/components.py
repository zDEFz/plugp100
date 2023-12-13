import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class Components:
    component_list: dict[str, Any]

    @staticmethod
    def try_from_json(data: dict[str, Any]) -> "Components":
        components = data.get("component_list", [])
        return Components({c["id"]: c["ver_code"] for c in components})

    def __contains__(self, item):
        return self.has(item)

    def has(self, component_name: str) -> bool:
        return self.get_version(component_name) is not None

    def get_version(self, component_name: str) -> Optional[int]:
        return self.component_list.get(component_name, None)

    def as_list(self) -> list[str]:
        return [c for c in self.component_list.keys()]
