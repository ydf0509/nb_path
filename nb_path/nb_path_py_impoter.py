

from nb_path import NbPath
import functools
import sys
import os
import types
import importlib.util

class NbPathPyImporter(NbPath):
    @staticmethod
    @functools.lru_cache()
    def _get_file__module_map():
        file__module_map = {}
        for k, v in sys.modules.items():
            try:
                file__module_map[NbPath(v.__file__).resolve().as_posix()] = v
            except (AttributeError, TypeError):
                pass
        return file__module_map

    def import_as_module(self, module_name: str = None) -> types.ModuleType:
        """Imports the .py file represented by the current path as a module."""
        if not self.is_file() or self.suffix != ".py":
            raise ValueError("This method can only be called on a .py file.")

        with self._lock:
            # self.path.resolve() -> self.resolve()
            path_str = self.resolve().as_posix()
            key = (path_str, module_name)
            if key in self._modules_cache:
                return self._modules_cache[key]

            file__module_map = self._get_file__module_map()
            if path_str in file__module_map:
                module = file__module_map[path_str]
                self._modules_cache[key] = module
                return module

            if module_name is None:
                try:
                    module_name = self.get_module_name()
                    self.logger.info(f"Importing module: {self}")
                except ValueError:
                    self.logger.warning(
                        f"Path '{self}' not in sys.path. Guessing module name."
                    )
                    module_name = self.stem

            module_spec = importlib.util.spec_from_file_location(module_name, self)
            module = importlib.util.module_from_spec(module_spec)
            sys.modules[module_name] = (
                module  # Crucial step: register the new module in sys.modules
            )
            module_spec.loader.exec_module(module)
            self._modules_cache[key] = module
            return module

    def auto_import_pyfiles_in_dir(self, pattern: str = "*.py") -> None:
        """Automatically imports all Python files in the current directory and its subdirectories."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self} is not a directory.")

        caller_file = NbPath(sys._getframe(1).f_code.co_filename).resolve()
        for py_file in self.rglob_files(pattern):
            if py_file.resolve() == caller_file:
                self.logger.warning(
                    f"Skipping import of the calling module itself: {py_file}"
                )
                continue
            # if py_file.name == '__init__.py':
            #     self.logger.debug(f'Skipping import of package initializer: {py_file}')
            #     continue
            try:
                py_file.import_as_module()
            except Exception as e:
                self.logger.error(f"Failed to import module {py_file}: {e}")

    def get_module_name(self) -> str:
        """
        Calculates the Python module name for the current file path based on sys.path.
        e.g., 'D:/.../my_project/utils/tool.py' -> 'utils.tool'
        """
        resolved_self = self.resolve()
        for p_str in sys.path[0:]:
            # Ensure the path in sys.path is a valid directory
            if not p_str or not os.path.isdir(p_str):
                continue
            try:
                # Use resolve() to ensure we are comparing consistent absolute paths
                relative_path = resolved_self.relative_to(NbPath(p_str).resolve())
                # Stop after finding the first matching sys.path entry
                module_path_str = str(relative_path).replace(".py", "")
                return module_path_str.replace("\\", ".").replace("/", ".")
            except ValueError:
                continue
        raise ValueError(f"{self} is not in any directory of sys.path")

    @staticmethod
    @functools.lru_cache()
    def import_module(module_name: str) -> types.ModuleType:
        """A convenient static method for importing a module, e.g., 'a.b.c'."""
        return importlib.import_module(module_name)