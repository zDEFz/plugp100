## This script allow to build wheels dependecy which is not available through pypi
## or arm CPU like armv7
import os
import platform
import sys

from ci_build_utils import get_compiled_requirements_from_ci, merge_requirements, read_requirements_file, \
    intersect_contains_string

REQUIREMENTS = read_requirements_file('requirements.txt')


def get_requirements_to_compile(requirements: [str]) -> [str]:
    if is_armv7():
        return intersect_contains_string(requirements, read_requirements_file('compile_armv7.txt'))
    else:
        return []


def is_armv7() -> bool:
    return platform.machine() in ("armv7l", "armv7")


def requirements_filename_by_arch() -> str:
    if is_armv7():
        return f"requirements-armv7.txt"
    else:
        return "requirements.txt"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage ci_build_wheels.py <wheels_target_folder> <url_to_folder>")
        exit(-1)

    current_arch = platform.machine().lower()
    wheels_target_folder = os.path.join(sys.argv[1], current_arch)
    hosting_url = f"{sys.argv[2]}{current_arch}/"
    pip_cache_dir = sys.argv[3] if len(sys.argv) > 3 else None
    new_requirements_file = requirements_filename_by_arch()

    print(f"""Detected {current_arch}.\nUsing wheels folder: {wheels_target_folder}.\nUsing URL: {hosting_url}""")

    print(f"Extracting requirements to compile. Wheels folder: {wheels_target_folder}.")
    requirements_to_compile = get_requirements_to_compile(REQUIREMENTS)
    print(f"Found {len(requirements_to_compile)} wheels to compile.")

    print("Building wheels...")
    cache_dir_command = f'--cache-dir {pip_cache_dir}' if pip_cache_dir else ''
    os.system(f"pip wheel {' '.join(requirements_to_compile)} -w {wheels_target_folder} {cache_dir_command}")

    print("Generating requirements from wheels folder")
    compiled_wheels_requirements = get_compiled_requirements_from_ci(wheels_target_folder, hosting_url)

    print(f"Creating new requirements.txt as {new_requirements_file}")
    merged_requirements = merge_requirements(REQUIREMENTS, compiled_wheels_requirements)
    with open(new_requirements_file, 'w') as file:
        file.writelines('\n'.join(merged_requirements))
