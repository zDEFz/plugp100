import os

COMPILED_WHEELS_FOLDER = "wheels"


def build_dependency_links() -> [str]:
    return listdir_full_path(os.path.join(os.getcwd(), COMPILED_WHEELS_FOLDER))


def listdir_full_path(folder: str) -> [str]:
    return [os.path.join(folder, file) for file in os.listdir(folder)]
