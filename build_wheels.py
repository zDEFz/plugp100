## This script allow to build wheels dependecy which is not available through pypi
## or arm CPU like armv7
import os
import platform

from setup_utils import COMPILED_WHEELS_FOLDER

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = requirements_file.read().split("\n")


def build_unavailable_from_requirements(requirements: [str]) -> [str]:
    if is_armv7():
        return extract_from_requirements(requirements, read_unavailable_names('requirement_unavailable_armv7.txt'))
    else:
        return []


def read_unavailable_names(filename: str) -> [str]:
    with open(filename) as file:
        return file.read().split("\n")


def extract_from_requirements(requirements: [str], unavailable_names: [str]) -> [str]:
    return list(filter(
        lambda requirement: any(unavailable_req in requirement for unavailable_req in unavailable_names),
        requirements
    ))


def is_armv7() -> bool:
    return platform.machine() in ("armv7l", "armv7")


if __name__ == "__main__":
    args = " ".join(build_unavailable_from_requirements(REQUIREMENTS))
    os.system(f"pip wheel {args} -w {COMPILED_WHEELS_FOLDER}")
