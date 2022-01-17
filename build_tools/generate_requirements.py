import os
import subprocess
import sys

from ci_build_utils import get_compiled_requirements_from_ci, merge_requirements, \
    read_requirements_file

SUPPORTED_ARCHITECTURES = ["armv6l", "armv7l", "amd64", "aarch64", "x86"]


def get_current_wheels_commit_sha() -> str:
    return subprocess.check_output(f"git rev-parse wheels", shell=True, text=True).strip()


def get_compiled_architectures(wheels_branch_folder: str) -> [str]:
    return list(filter(lambda folder: folder in SUPPORTED_ARCHITECTURES, os.listdir(wheels_branch_folder)))


# e.g. url = https://github.com/petretiandrea/plugp100/raw/
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage ci_build_wheels.py <git_wheels_folder> <url_to_branch>")
        exit(-1)

    git_wheels_folder = sys.argv[1]
    commit_sha = get_current_wheels_commit_sha()

    branch_url = f"{sys.argv[2]}{commit_sha}/"
    architectures = get_compiled_architectures(git_wheels_folder)

    requirements = read_requirements_file('requirements.txt')

    print(f"Using base branch url as: ${branch_url}")
    for architecture in architectures:
        print(f"Generating requirements file for {architecture}...")
        new_requirements_file = f"requirements-{architecture}.txt"
        arch_wheels_folder = os.path.join(git_wheels_folder, architecture)
        arch_hosting_url = f"{branch_url}{architecture}/"
        compiled_wheels_requirements = get_compiled_requirements_from_ci(arch_wheels_folder, arch_hosting_url)

        print(f"Creating new requirements.txt as {new_requirements_file}")
        merged_requirements = merge_requirements(requirements, compiled_wheels_requirements)
        with open(new_requirements_file, 'w') as file:
            file.writelines('\n'.join(merged_requirements))

    print("Done.")
