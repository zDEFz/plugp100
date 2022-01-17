"""
Script to build wheels which are unavailable from PyPi, caused by unsupported cpu architecture (armv7 and armv6).
"""

import os
import platform
import sys

from ci_build_utils import read_requirements_file, \
    intersect_contains_string

REQUIREMENTS = read_requirements_file('requirements.txt')


def get_requirements_to_compile(requirements: [str]) -> [str]:
    compile_file = f'compile-{platform.machine().lower()}.txt'
    if os.path.exists(compile_file):
        return intersect_contains_string(requirements, read_requirements_file(compile_file))
    else:
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage ci_build_wheels.py <wheels_target_folder> <pip_cache_folder>")
        exit(-1)

    current_arch = platform.machine().lower()
    wheels_target_folder = os.path.join(sys.argv[1], current_arch)
    pip_cache_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"""Detected {current_arch}.\nUsing wheels folder: {wheels_target_folder}.\n""")

    print(f"Extracting requirements to compile.")
    requirements_to_compile = get_requirements_to_compile(REQUIREMENTS)
    print(f"Found {len(requirements_to_compile)} wheels to compile.")

    print("Building wheels...")
    cache_dir_command = f'--cache-dir {pip_cache_dir}' if pip_cache_dir else ''
    os.system(f"pip wheel {' '.join(requirements_to_compile)} -w {wheels_target_folder} {cache_dir_command}")
