import os
from typing import Optional


def read_requirements_file(filename: str) -> [str]:
    with open(filename) as file:
        return file.read().split("\n")


def get_compiled_requirements_from_ci(folder: str, base_url: str) -> [str]:
    """ Generate a list like requirements.txt file of CI compiled wheels.
    @param folder: The folder where compiled wheels are.
    @param base_url: The base url to access to wheels folder
    @return: A list of pip dependencies which point to base_url

    Example:
        pkcs7@https://base_url/pkcs7-0.1.2-py3-none-any.whl
    """
    wheel_files = os.listdir(folder)
    return [get_wheel_from_filename(os.path.basename(wheel_file), base_url) for wheel_file in wheel_files]


def get_wheel_from_filename(filename: str, base_url: str) -> str:
    """
    Extract wheel requirement from filename
    @param filename: The file of a whl
    @param base_url: The base url to access to this .whl file
    @return: A pip compliant requirements <library_name>@<url>/**.whl.

    Like pkcs7@https://base_url/pkcs7-0.1.2-py3-none-any.whl
    """
    requirement_name = filename.split("-")[0]
    return f"{requirement_name}@{base_url}{filename}"


def merge_requirements(requirements: [str], to_merge_requirements: [str]) -> [str]:
    """
    Merge two pip requirements list.
    @param requirements: Base requirements list.
    @param to_merge_requirements: Requirements list to merge.
    @return: A merged requirements list.
    """
    merged = []
    for requirement in requirements:
        to_merge = find_contains_substring(get_requirement_name(requirement), to_merge_requirements)
        merged.append(to_merge if to_merge is not None else requirement)
    return merged


def find_contains_substring(substring: str, strings: [str]) -> Optional[str]:
    founded = [string for string in strings if substring in string]
    return founded[0] if founded else None


def intersect_contains_string(strings1: [str], strings2: [str]) -> [str]:
    return list(filter(
        lambda requirement: any(string2 in requirement for string2 in strings2),
        strings1
    ))


def get_requirement_name(requirement: str) -> str:
    if "==" in requirement:
        return requirement.split("==")[0]
    else:
        return requirement
