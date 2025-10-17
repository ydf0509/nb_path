"""
nb_path.py - An enhanced path manipulation module that integrates pathlib, shutil, and importlib functionalities.
"""

from contextlib import contextmanager
import hashlib
import importlib.util
import logging
from logging import getLogger
import functools
import zipfile
import os
import shutil
import sys
import threading
import types
import typing
from pathlib import Path, WindowsPath, PosixPath
import tempfile
import re
from collections import namedtuple



# --- Key Change 1: Dynamically select the correct base class ---
# Depending on the current operating system, inherit from WindowsPath or PosixPath.
# This is the standard pattern for subclassing pathlib.Path.
_Base = WindowsPath if sys.platform == "win32" else PosixPath


class NbPath(_Base, ):
    """
    NbPath is an enhanced version of the pathlib.Path object.
    It inherits all the functionality of Path (including the use of the '/' operator)
    and additionally integrates advanced file operations from shutil, dynamic module loading
    from importlib, and more.
    """
    _modules_cache = {}
    _lock = threading.Lock()
    logger = getLogger(name='NbPath')
    # Define a clear result type, which is better than returning a tuple
    GrepResult = namedtuple('GrepResult', ['path', 'line_number', 'line_content', 'match', 'context_lines'])


    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)
    def ensure_parent(self) -> 'NbPath':
        """
        Ensures that the parent directory of the current path exists, creating it if it doesn't.
        Supports chained calls.
        
        Example:
            NbPath('data/reports/2023/sales.csv').ensure_parent().write_text('...')
        """
        # self.path.parent -> self.parent
        parent_dir = self.parent
        parent_dir.mkdir(parents=True, exist_ok=True)
        return self

    def touch(self, mode: int = 0o666, exist_ok: bool = True, create_parent: bool = True):
        """
        Creates an empty file, similar to the Unix 'touch' command.
        :param mode: File permissions, defaults to 0o666.
        :param exist_ok: If True, do not raise an error if the file already exists.
        :param create_parent: If True, automatically create parent directories if they don't exist.
        """
        if create_parent:
            self.ensure_parent()
        
        # Call the parent class's touch implementation
        super().touch(mode=mode, exist_ok=exist_ok)
        return self

    def empty(self) -> 'NbPath':
        """Empties a directory of all its files and subdirectories, but keeps the directory itself."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self} is not a directory.")
        for item in self.iterdir():
            # Elegantly reuse our own delete method
            NbPath(item).delete(missing_ok=True)
        return self

    def delete(self, missing_ok: bool = True) -> None:
        """
        Deletes a file or a directory. If it's a directory, it's deleted recursively.
        :param missing_ok: If True, do not raise an error if the path does not exist.
        """
        try:
            if self.is_file() or self.is_symlink():
                self.unlink()
                self.logger.debug(f"Deleted file: {self}")
            elif self.is_dir():
                shutil.rmtree(self)
                self.logger.debug(f"Deleted directory tree: {self}")
        except FileNotFoundError:
            if not missing_ok:
                raise
        return self

    # The read_text and write_text methods are already provided by the parent class, so they don't need to be overridden.
    # However, keeping them is a good choice for the convenience of setting a default encoding.
    def read_text(self, encoding: str = 'utf-8', errors: str = None) -> str:
        return super().read_text(encoding=encoding, errors=errors)

    def write_text(self, data: str, encoding: str = 'utf-8', errors: str = None) -> int:
        return super().write_text(data, encoding=encoding, errors=errors)


    def size(self) -> int:
        """Returns the file size in bytes. Returns 0 if it is a directory."""
        if self.is_file():
            return self.stat().st_size
        return 0

    def size_human(self) -> str:
        """Returns a human-readable file size string (e.g., '1.23 MB')."""
        size_bytes = self.size()
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def copy_to(self, destination: typing.Union[os.PathLike, str], dirs_exist_ok: bool = True) -> 'NbPath':
        """
        Copies the file or directory to the specified location.
        - If destination is a directory, copies the source into that directory.
        - If destination is a file path, copies and renames the source.
        :param destination: The target path.
        :param dirs_exist_ok: (For directories only) If True, allows merging if the destination directory exists. (Python 3.8+)
        :return: A new NbPath object pointing to the destination.
        """
        dest_path = Path(destination)
        if self.is_file():
            shutil.copy2(self, dest_path)
            return self.__class__(dest_path)
        elif self.is_dir():
            dest_path_final = dest_path if not dest_path.is_dir() else dest_path / self.name
            if sys.version_info >= (3, 8):
                shutil.copytree(self, dest_path_final, dirs_exist_ok=dirs_exist_ok)
            else: # Compatibility for older Python versions
                if dest_path_final.exists():
                     raise FileExistsError(f"Destination directory {dest_path_final} already exists.")
                shutil.copytree(self, dest_path_final)
            return self.__class__(dest_path_final)
        raise FileNotFoundError(f"Source path {self} does not exist or is not a file/directory.")

    def move_to(self, destination: typing.Union[os.PathLike, str]) -> 'NbPath':
        """Moves the file or directory to the specified location."""
        # str(self.path) -> str(self)
        moved_path_str = shutil.move(str(self), str(destination))
        return self.__class__(moved_path_str)

    def sync_to(self,
                destination: typing.Union[os.PathLike, str],
                delete_extraneous: bool = False,
                ignore_patterns: typing.List[str] = None):
        """
        Intelligently synchronizes this directory to a destination directory (like rsync).

        It only copies new or modified files, making it highly efficient for repeated runs.

        Args:
            destination: The target directory to sync to.
            delete_extraneous: If True, deletes files in the destination that do not
                               exist in the source directory (Mirroring). Defaults to False.
            ignore_patterns: A list of glob patterns to ignore during sync,
                             e.g., ['*.pyc', '__pycache__'].
        """
        if not self.is_dir():
            raise NotADirectoryError(f"Source '{self}' is not a directory.")

        dest_path = NbPath(destination)
        dest_path.mkdir(exist_ok=True)
        
        source_files = {p.relative_to(self) for p in self.rglob_files('*')}
        dest_files = {p.relative_to(dest_path) for p in dest_path.rglob_files('*')}

        # 1. Copy new or modified files
        for rel_path in source_files:
            source_file = self / rel_path
            dest_file = dest_path / rel_path

            # Simple ignore logic
            if ignore_patterns and any(rel_path.match(p) for p in ignore_patterns):
                continue

            if not dest_file.exists() or source_file.stat().st_mtime > dest_file.stat().st_mtime:
                self.logger.debug(f"Syncing: {source_file} -> {dest_file}")
                dest_file.ensure_parent()
                shutil.copy2(source_file, dest_file)

        # 2. Delete extraneous files if requested
        if delete_extraneous:
            for rel_path in (dest_files - source_files):
                dest_file = dest_path / rel_path
                self.logger.debug(f"Deleting extraneous file: {dest_file}")
                dest_file.delete(missing_ok=True)

    
    def download_from_url(self, url: str, overwrite: bool = False, **kwargs) -> 'NbPath':
        """
        Downloads a file from a URL to the path represented by this object.
        :param url: The URL of the file to download.
        :param overwrite: If True, overwrites the file if it already exists.
        :param kwargs: Additional arguments to pass to `requests.get` (e.g., headers, timeout).
        :return: An NbPath object pointing to the downloaded file.
        """
        try:
            import requests
            from tqdm import tqdm
        except ImportError:
            raise ImportError("requests and tqdm are required. Please run 'pip install requests tqdm'.")


        dest_path = self
        if dest_path.is_dir():
            file_name = url.split('/')[-1]
            dest_path = dest_path / file_name

        
        if dest_path.exists() and not overwrite:
            self.logger.warning(f"File {dest_path} already exists. Skipping download.")
            return dest_path

        dest_path.ensure_parent()

        with requests.get(url, stream=True, **kwargs) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            with open(dest_path, 'wb') as f, tqdm(
                total=total_size, unit='iB', unit_scale=True, desc=dest_path.name
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    bar.update(size)
        return dest_path

    def expand(self) -> 'NbPath':
        """
        Expands user and environment variables in the path (~, $VAR, %VAR%).
        Example:
            NbPath('~/.config').expand() -> /home/user/.config
            NbPath('$HOME/.config').expand() -> /home/user/.config
        """
        # os.path.expanduser only handles ~
        # os.path.expandvars only handles $VAR or %VAR%
        # We need to combine both.
        s = os.path.expanduser(str(self))
        s = os.path.expandvars(s)
        return self.__class__(s)

    @classmethod
    def self_py_file(cls) -> 'NbPath':
        return cls(__file__)
    
    @classmethod
    def self_py_dir(cls) -> 'NbPath':
        return cls.self_py_file().parent
        
    def find_git_root(self) -> 'NbPath':
        """
        Traverses upwards from the current path to find the root of the Git project.
        The root is defined as the directory containing the '.git' directory.

        This is a convenient shortcut for `find_project_root(markers=['.git'])`.

        :return: An NbPath object of the Git project root.
        :raises FileNotFoundError: If the '.git' directory is not found by searching upwards.

        print(f'find_git_root: {NbPath().find_git_root()}')
        """
        try:
            # Directly call the more generic method for clear intent
            return self.find_project_root(markers=['.git'])
        except FileNotFoundError as e:
            # Provide a more specific error message
            raise FileNotFoundError(f"Git root could not be found by searching upwards from {self}") from e

    def find_project_root(self, markers: typing.List[str] = None) -> 'NbPath':
        """
        Traverses upwards from the current path to find the project root directory.
        The root is defined as a directory containing any of the specified marker files/directories.

        This is a powerful and generic tool for non-Git projects or scenarios requiring custom markers.
        For Git projects, using the more explicit `.find_git_root()` method is recommended.

        :param markers: A list of marker files/directories. If None, a default list of common markers is used.
        :return: An NbPath object of the project root.
        :raises FileNotFoundError: If no marker is found by searching upwards.
        """
        if markers is None:
            markers = [
                'pyproject.toml', 'setup.py', 'requirements.txt', '.env', 
                'manage.py', 'venv', '.venv', '.idea', '.vscode'
            ]
        
        current = self.resolve()
        while True:
            for marker in markers:
                if (current / marker).exists():
                    self.logger.debug(f"Project root found at: {current} (marker: '{marker}')")
                    return current

            if current == current.parent:  # Reached the filesystem root (e.g., '/' or 'C:\\')
                break
            current = current.parent

        raise FileNotFoundError(f"Project root could not be found by searching upwards from {self} using markers: {markers}")

    
    def zip_to(self, destination: typing.Union[os.PathLike, str], overwrite: bool = False):
        """
        Compresses the current file or directory into a ZIP file.
        :param destination: The path for the destination ZIP file.
        :param overwrite: If True, overwrites the destination file if it already exists.
        """
        dest_path = NbPath(destination)
        if dest_path.exists() and not overwrite:
            raise FileExistsError(f"Destination ZIP file already exists: {dest_path}")

        with zipfile.ZipFile(dest_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            if self.is_file():
                zf.write(self, self.name)
            elif self.is_dir():
                for file in self.rglob('*'):
                    zf.write(file, file.relative_to(self))
        
        return dest_path
    
    def unzip_to(self,destination: typing.Union[os.PathLike, str] = '.'):
        """
        Extracts a ZIP file to a specified directory.
        :param destination: The directory to extract the files to.
        :return: An NbPath object of the destination directory.
        """
        dest_path = NbPath(destination)
        dest_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(self, 'r') as zf:
            zf.extractall(dest_path)
        return dest_path
        
    def rglob_files(self, pattern: str) -> typing.List['NbPath']:
        """Recursively finds all matching files and returns a list of NbPath objects."""
        # self.path.rglob -> self.rglob
        return [p for p in self.rglob(pattern) if p.is_file()]

    def rglob_dirs(self, pattern: str) -> typing.List['NbPath']:
        """Recursively finds all matching directories and returns a list of NbPath objects."""
        return [p for p in self.rglob(pattern) if p.is_dir()]

    
    def grep(self,
             pattern: str,
             file_pattern: str = '*',
             is_regex: bool = True,
             ignore_case: bool = False,
             encoding: str = 'utf-8',
             context: typing.Union[int, typing.Tuple[int, int]] = None) -> typing.Generator[GrepResult, None, None]:
        """
        Searches for a pattern within files, similar to the command-line 'grep'.

        This method is a powerful generator that yields results as they are found,
        making it memory-efficient for searching through large directories. It now supports
        displaying context lines around each match.

        It can be called on a directory to search recursively, or on a single file.

        Args:
            pattern (str): The string or regex pattern to search for.
            file_pattern (str, optional): A glob pattern to filter which files to search.
                                          Only used when calling grep on a directory. Defaults to '*'.
            is_regex (bool, optional): If True (default), treats 'pattern' as a regular expression.
                                       If False, performs a simple string search.
            ignore_case (bool, optional): If True, performs a case-insensitive search. Defaults to False.
            encoding (str, optional): The file encoding to use. Defaults to 'utf-8'.
            context (int or tuple, optional): If specified, includes context lines around the match.
                                              - An `int` `n` shows `n` lines before and `n` lines after.
                                              - A `tuple` `(before, after)` shows `before` lines before and `after` lines after.
                                              Defaults to None.

        Yields:
            GrepResult: A named tuple for each match, containing `(path, line_number, line_content, match, context_lines)`.
                        The `match` attribute is the matched string or regex match object. `context_lines` is a list of `(line_num, line_text)` tuples.

        Example:
            >>> # 1. Search for a simple string in all .py files in a directory
            >>> src_dir = NbPath('./src')
            >>> for result in src_dir.grep("my_function", file_pattern='*.py', is_regex=False):
            ...     print(f"{result.path.name}:{result.line_number}: {result.line_content.strip()}")

            >>> # 2. Use a regex to find all API endpoints in a single file
            >>> api_file = NbPath('api/routes.py')
            >>> for result in api_file.grep(r"@app\.route\(['\"](.*?)['\"]\)"):
            ...     print(f"Found endpoint: {result.match.group(1)}")
            
            >>> # 3. Search with 2 lines of context before and after
            >>> for result in src_dir.grep("important_logic", context=2):
            ...     for num, line in result.context_lines:
            ...         prefix = ">>" if num == result.line_number else "  "
            ...         print(f"{prefix} {num:4d}: {line.rstrip()}")
        """
        files_to_search = [self] if self.is_file() else self.rglob_files(file_pattern)

        re_flags = re.IGNORECASE if ignore_case else 0
        
        if is_regex:
            try:
                compiled_pattern = re.compile(pattern, re_flags)
            except re.error as e:
                raise ValueError(f"Invalid regular expression: {pattern}") from e
        else:
            search_str = pattern.lower() if ignore_case else pattern

        # Parse context parameter
        before, after = 0, 0
        if context is not None:
            if isinstance(context, int):
                before = after = context
            elif isinstance(context, tuple) and len(context) == 2:
                before, after = context
            else:
                raise ValueError("`context` must be an integer or a tuple of two integers (before, after).")

        for file in files_to_search:
            try:
                with file.open('r', encoding=encoding, errors='ignore') as f:
                    lines_buffer = []
                    if before > 0:
                        from collections import deque
                        lines_buffer = deque(maxlen=before)

                    for line_num, line in enumerate(f, 1):
                        match_found = False
                        match_result = None

                        if is_regex:
                            # Use search to find the first match to trigger context collection
                            match_obj = compiled_pattern.search(line)
                            if match_obj:
                                match_found = True
                                match_result = match_obj
                        else:
                            line_to_search = line.lower() if ignore_case else line
                            if search_str in line_to_search:
                                match_found = True
                                match_result = pattern

                        if match_found:
                            context_lines = list(lines_buffer)
                            context_lines.append((line_num, line))
                            
                            # Read 'after' lines
                            for _ in range(after):
                                try:
                                    after_line = next(f)
                                    context_lines.append((line_num + 1 + _, after_line))
                                except StopIteration:
                                    break
                            
                            yield self.GrepResult(file, line_num, line, match_result, context_lines)
                        
                        if before > 0:
                            lines_buffer.append((line_num, line))

            except Exception as e:
                self.logger.warning(f"Could not grep file {file}: {e}")


    def hash(self, algorithm: str = 'sha256') -> str:
        """Calculates the hash of the file's content."""
        hasher = hashlib.new(algorithm)
        with self.open('rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()


    @classmethod
    @contextmanager
    def tempfile(cls, suffix: str = None, prefix: str = None, dir: typing.Union[os.PathLike, str] = None, text: bool = False) -> typing.Generator['NbPath', None, None]:
        """Creates a temporary file as a context manager, returning an NbPath object.

        This is a powerful, object-oriented replacement for parts of Python's `tempfile` module.
        The temporary file is created securely and is guaranteed to be deleted upon exiting
        the `with` block.

        Args:
            suffix (str, optional): If specified, the file name will end with that suffix. Defaults to None.
            prefix (str, optional): If specified, the file name will begin with that prefix. Defaults to None.
            dir (os.PathLike or str, optional): If specified, the file will be created in that directory.
                                                If not specified, a default temporary directory is used.
            text (bool, optional): If True, the file is opened in text mode. If False (default),
                                   it's opened in binary mode. This only affects the initial file object
                                   and does not restrict subsequent operations on the NbPath object.

        Yields:
            NbPath: An NbPath object pointing to the newly created temporary file.

        Example:
            >>> # Example 1: Basic usage for a temporary data file
            >>> with NbPath.tempfile(suffix=".txt") as tmp_file:
            ...     print(f"Temporary file created at: {tmp_file}")
            ...     print(f"Is it an NbPath object? {isinstance(tmp_file, NbPath)}")
            ...     tmp_file.write_text("Hello, world!")
            ...     assert tmp_file.read_text() == "Hello, world!"
            ... # The file is automatically deleted here.
            >>> print(f"Does the file still exist? {tmp_file.exists()}")
            Temporary file created at: .../tmpxxxxx.txt
            Is it an NbPath object? True
            Does the file still exist? False

            >>> # Example 2: In a unit test
            >>> def test_process_data():
            ...     with NbPath.tempfile(prefix="test_data_") as input_file:
            ...         input_file.write_json({"id": 1, "value": 42})
            ...         result = process_data_from_file(input_file) # Your function to test
            ...         assert result == "processed_42"
        """
        # Using NamedTemporaryFile with delete=False is a common pattern to get a safe, unique filename.
        # It allows us to close the file immediately, avoiding file locking issues on Windows,
        # and manage its lifecycle with our own robust logic.
        fp = tempfile.NamedTemporaryFile(
            suffix=suffix, prefix=prefix, dir=dir, delete=False, mode='w' if text else 'w+b'
        )
        fp.close()  # Close the file handle immediately. We only wanted the unique name.
        
        temp_path = cls(fp.name)
        
        try:
            yield temp_path
        finally:
            # Robustly delete the file if it still exists upon exit.
            if temp_path.exists():
                try:
                    temp_path.delete()
                except Exception as e:
                    cls.logger.error(f"Failed to delete temporary file {temp_path}: {e}")

    @classmethod
    @contextmanager
    def tempdir(cls, suffix: str = None, prefix: str = None, dir: typing.Union[os.PathLike, str] = None) -> typing.Generator['NbPath', None, None]:
        """Creates a temporary directory as a context manager, returning an NbPath object.

        This is a superior, object-oriented alternative to `tempfile.TemporaryDirectory`.
        The directory and all its contents are recursively deleted upon exiting the `with` block.

        Args:
            suffix (str, optional): If specified, the directory name will end with that suffix. Defaults to None.
            prefix (str, optional): If specified, the directory name will begin with that prefix. Defaults to None.
            dir (os.PathLike or str, optional): If specified, the directory will be created in that directory.
                                                If not specified, a default temporary directory is used.

        Yields:
            NbPath: An NbPath object pointing to the newly created temporary directory.

        Example:
            >>> # Example 1: Creating a temporary workspace
            >>> with NbPath.tempdir(prefix="my_app_") as tmp_dir:
            ...     print(f"Temporary directory created at: {tmp_dir}")
            ...     print(f"Is it an NbPath object? {isinstance(tmp_dir, NbPath)}")
            ...     
            ...     # You can immediately use all NbPath features
            ...     config_file = (tmp_dir / "conf" / "config.json").ensure_parent()
            ...     config_file.write_json({"setting": "enabled"})
            ...     
            ...     data_file = tmp_dir / "data.csv"
            ...     data_file.write_text("id,value\n1,100")
            ...
            ...     assert (tmp_dir / "conf" / "config.json").is_file()
            ... # The directory and all its contents are automatically deleted here.
            >>> print(f"Does the directory still exist? {tmp_dir.exists()}")
            Temporary directory created at: .../my_app_xxxxxx
            Is it an NbPath object? True
            Does the directory still exist? False
        """
        # The standard library's TemporaryDirectory is already robust. We just wrap it
        # to yield our enhanced NbPath object instead of a plain string.
        with tempfile.TemporaryDirectory(suffix=suffix, prefix=prefix, dir=dir) as temp_dir_str:
            yield cls(temp_dir_str)




class NbPathPyImporter(NbPath):
    @staticmethod
    @functools.lru_cache()
    def _get_file__module_map():
        file__module_map = {}
        for k, v in sys.modules.items():
            try:
                file__module_map[Path(v.__file__).resolve().as_posix()] = v
            except (AttributeError, TypeError):
                pass
        return file__module_map

    def import_as_module(self, module_name: str = None) -> types.ModuleType:
        """Imports the .py file represented by the current path as a module."""
        if not self.is_file() or self.suffix != '.py':
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
                    self.logger.info(f'Importing module: {self}')
                except ValueError:
                    self.logger.warning(f"Path '{self}' not in sys.path. Guessing module name.")
                    module_name = self.stem

            module_spec = importlib.util.spec_from_file_location(module_name, self)
            module = importlib.util.module_from_spec(module_spec)
            sys.modules[module_name] = module # Crucial step: register the new module in sys.modules
            module_spec.loader.exec_module(module)
            self._modules_cache[key] = module
            return module

    def auto_import_pyfiles_in_dir(self, pattern: str = '*.py') -> None:
        """Automatically imports all Python files in the current directory and its subdirectories."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self} is not a directory.")
            
        caller_file = NbPath(sys._getframe(1).f_code.co_filename).resolve()
        for py_file in self.rglob_files(pattern):
            if py_file.resolve() == caller_file:
                self.logger.warning(f'Skipping import of the calling module itself: {py_file}')
                continue
            try:
                
                py_file.import_as_module()
            except Exception as e:
                self.logger.error(f'Failed to import module {py_file}: {e}')

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
                relative_path = resolved_self.relative_to(Path(p_str).resolve())
                # Stop after finding the first matching sys.path entry
                module_path_str = str(relative_path).replace('.py', '')
                return module_path_str.replace('\\', '.').replace('/', '.')
            except ValueError:
                continue
        raise ValueError(f'{self} is not in any directory of sys.path')

    @staticmethod
    @functools.lru_cache()
    def import_module(module_name: str) -> types.ModuleType:
        """A convenient static method for importing a module, e.g., 'a.b.c'."""
        return importlib.import_module(module_name)


if __name__ == '__main__':
    # --- Testing the new NbPath class ---
    from nb_log import get_logger
    get_logger('NbPath').setLevel(logging.DEBUG)

    print(type(NbPath('/')))
    print(type(NbPath(__file__)))
    print(type(NbPath(__file__).parent))
    print(type(NbPath(__file__).parent / 'a.txt'))

    cur_dir = NbPath(__file__).parent
    print(type(cur_dir))
    cur_file = NbPath(__file__)
    print(NbPath(cur_file))

    print(NbPath(cur_dir,'adir','bdir','c.txt'))

    print(repr(NbPath().resolve()))
    print(NbPath().resolve())

    print(repr(Path().resolve()))
    print(Path().resolve())

    print(NbPath.self_py_file())
    print(NbPath.self_py_dir())
    print(NbPath.self_py_file().hash())
    

    print(list(cur_dir.rglob_files('*.py', )))
    

    NbPath(r'D:\codes\nb_path\tests\temps').zip_to(NbPath(r'D:\codes\nb_path\tests','temps_zip.zip'),overwrite=True)
    print(NbPath(r'D:\codes\nb_path\tests','temps_zip.zip').unzip_to(NbPath('d:/codes/nb_path/tests','temps_zip_dir')))
    
    print(NbPath('~/.config').expand())

    print(f'find_git_root: {NbPath().find_git_root()}')
    print(f'find_project_root: {repr(NbPath().find_project_root())}')


    print(NbPath('d:/codes/nb_path/tests','baidu.html').download_from_url(
          'https://www.baidu.com',overwrite=True))
    
    print(NbPath('d:/codes/nb_path/tests','baidu.html').size_human())


    print(NbPathPyImporter(r'D:\codes\nb_path\tests\m1.py').import_as_module())

    NbPathPyImporter(r'D:\codes\nb_path\tests\pacb').auto_import_pyfiles_in_dir()

    print(NbPathPyImporter(r'D:\codes\nb_path\tests\m1.py').get_module_name())

  

    src_dir = NbPath('d:/codes/nb_path')
    for result in src_dir.grep("error", file_pattern='*.py', is_regex=False,):
          print(f"{result.path.name}:{result.line_number}: {result.line_content.strip()}")

    for result in src_dir.grep("error", context=5, file_pattern='*.py', is_regex=False):
          print("-" * 20)
          for num, line_text in result.context_lines:
                prefix = ">>" if num == result.line_number else "  "
                sys.stdout.write(f"{prefix} {num:4d}: {line_text.rstrip()}\n")



    