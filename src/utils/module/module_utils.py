import importlib
import os
from pathlib import Path
from types import ModuleType
from src.utils.object import object_utils


# 해당 문구로 끝나는 module import
def import_all_modules_ends_with(ends_with: str) -> list[ModuleType]:
    modules: list[ModuleType] = []

    for root, dirs, files in os.walk(Path("./src")):
        for file in files:
            if file.endswith(ends_with):
                # get path
                location_path = Path(os.path.join(root, file))
                # reformat
                import_path = location_path_to_import_path(location_path)
                # import
                modules.append(importlib.import_module(import_path))

    return modules


# 파일 내의 모든 module import
def import_all_modules_in_folder(folder_path: Path) -> list[ModuleType]:
    modules: list[ModuleType] = []
    for root, dirs, files in os.walk(Path(folder_path)):
        for file in files:
            if 'pyc' in file:
                continue
            # get path
            location_path = Path(os.path.join(root, file))
            # reformat
            import_path = location_path_to_import_path(location_path)
            # import
            modules.append(importlib.import_module(import_path))

    return modules


# 파일의 module import
def import_module_of_file(file_path: Path) -> ModuleType:
    # reformat
    import_path = location_path_to_import_path(file_path)
    # import
    return importlib.import_module(import_path)


# 모듈 내의 해당 type 을 모두 만족하는 class 반환
def get_class_matching_types_in_module(module: ModuleType, matching_types: tuple) -> list:
    classes_of_type = []

    for key, value in module.__dict__.items():

        is_type_match = object_utils.is_match_of_types(value, matching_types)
        if not is_type_match:
            continue

        classes_of_type.append(value)

    return classes_of_type


# 파일 위치 명을 import 명으로 변경
def location_path_to_import_path(location_path: Path) -> str:
    location_path = str(location_path)
    location_path = location_path.replace('./', '', 1)
    location_path = location_path.replace('.py', '', 1)
    location_path = location_path.replace('/', '.')
    location_path = location_path.replace('\\', '.')
    return location_path
