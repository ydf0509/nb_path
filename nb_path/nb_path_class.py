"""
nb_path.py - An enhanced path manipulation module that integrates pathlib, shutil, and importlib functionalities.
"""


from contextlib import contextmanager
import hashlib
import json
import logging
from logging import getLogger
# from typing_extensions import Self
import zipfile
import os
import shutil
import sys
import threading
import typing
from pathlib import Path, WindowsPath, PosixPath
import tempfile
import re
from collections import namedtuple
import chardet

from nb_log import nb_log


# --- Key Change 1: Dynamically select the correct base class ---
# Depending on the current operating system, inherit from WindowsPath or PosixPath.
# This is the standard pattern for subclassing pathlib.Path.
_Base = WindowsPath if sys.platform == "win32" else PosixPath


class NbPath(
    _Base,
):
    """
    NbPath is an enhanced version of the pathlib.Path object.
    It inherits all the functionality of Path (including the use of the '/' operator)
    and additionally integrates advanced file operations from shutil, dynamic module loading
    from importlib, and more.
    """

    _modules_cache = {}
    _lock = threading.Lock()
    # logger = getLogger(name="NbPath")
    logger = nb_log.get_logger('NbPath')
    # Define a clear result type, which is better than returning a tuple
    GrepResult = namedtuple(
        "GrepResult", ["path", "line_number", "line_content", "match", "context_lines"]
    )

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def ensure_parent(self)  :
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

    def touch(
        self, mode: int = 0o666, exist_ok: bool = True, create_parent: bool = True
    ):
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

    def empty(self)  :
        """Empties a directory of all its files and subdirectories, but keeps the directory itself."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self} is not a directory.")
        for item in self.iterdir():
            # Elegantly reuse our own delete method
            NbPath(item).delete(missing_ok=True)
        return self

    def delete(self, missing_ok: bool = True) :
        """
        Deletes a file or a directory. If it's a directory, it's deleted recursively.
        :param missing_ok: If True, do not raise an error if the path does not exist.
        """
        try:
            if self.is_file() or self.is_symlink():
                self.unlink()
                self.logger.info(f"Deleted file: {self}")
            elif self.is_dir():
                shutil.rmtree(self)
                self.logger.info(f"Deleted directory tree: {self}")
        except FileNotFoundError:
            if not missing_ok:
                raise
        return self

    def clear_text(self):
        self.write_text("")
        return self
    

    # The read_text and write_text methods are already provided by the parent class, so they don't need to be overridden.
    # However, keeping them is a good choice for the convenience of setting a default encoding.
    def read_text(self, encoding: str = "utf-8", errors: str = None) -> str:
        return super().read_text(encoding=encoding, errors=errors)

    def write_text(self, data: str, encoding: str = "utf-8", errors: str = None) -> int:
        return super().write_text(data, encoding=encoding, errors=errors)

    def chardet_detect(self) -> dict:
        return chardet.detect(self.read_bytes())
    
    def write_text_with_utf8_bom(self, data: str, ) -> int:
        self.write_bytes(b'\xef\xbb\xbf' + data.encode('utf-8'))
        return self
    
    def ensure_utf8_bom(self):
        """
        Sometimes even if the file encoding is UTF-8, some service systems may mistakenly recognize it as another encoding,

        For example:
        during the process of copying/pasting files, 
        some bytes are lost and the copied string from the log is mixed with invisible characters.
        The markdown contains many emojis and emoticons
        """
        if not self.is_text():
            return self
        if self.read_bytes().startswith(b'\xef\xbb\xbf'):
            return self
        self.write_bytes(b'\xef\xbb\xbf' + self.read_bytes())
        return self
 
    def append_text(self, data: str, encoding: str = "utf-8",errors: str = None):
        with self.open(mode='a', encoding=encoding) as f:
            f.write(data)
        return self
     
    def merge_text_from_files(self, file_list: typing.List[typing.Union[os.PathLike, str]], separator: str = "\n") :
        for file in file_list:
            self.append_text(NbPath(file).read_text() + separator)
        return self
        
    def get_textfile_info(self, encoding: str = "utf-8",is_show_info: bool=False) -> dict:
        """
        Efficiently gets information about a text file, including line and character counts.

        This method avoids loading large files into memory at once by reading them line by line,
        making it highly efficient for analyzing large text files.

        Args:
            encoding (str): The encoding format to use for decoding the file. Defaults to 'utf-8'.

        Returns:
            dict: A dictionary containing the following keys:
                  - 'line_count' (int): The total number of lines in the file.
                  - 'char_count' (int): The total number of characters in the file.
                  - 'size_human' (str): The human-readable file size.
                  Returns default values if the path is not a text file.
        """
        if not self.is_file() or not self.is_text():
            return {"line_count": 0, "char_count": 0, "size_human": "0 B"}

        line_count, char_count = 0, 0
        try:
            with self.open("r", encoding=encoding, errors="ignore") as f:
                for line in f:
                    line_count += 1
                    char_count += len(line)
        except Exception as e:
            self.logger.warning(f"Could not get text file info for {self}: {e}")
            return {"line_count": 0, "char_count": 0, "size_human": "0 B"}
        
        info = {"file":str(self),"line_count": line_count, "char_count": char_count, "size_human": self.size_human()}
        if is_show_info:
            self.logger.info(json.dumps(info,ensure_ascii=False))
        return info

    def show_textfile_info(self):
        self.get_textfile_info(is_show_info=True)
        return self

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

    def copy_to(
        self, destination: typing.Union[os.PathLike, str], dirs_exist_ok: bool = True
    )  :
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
            dest_path_final = (
                dest_path if not dest_path.is_dir() else dest_path / self.name
            )
            if sys.version_info >= (3, 8):
                shutil.copytree(self, dest_path_final, dirs_exist_ok=dirs_exist_ok)
            else:  # Compatibility for older Python versions
                if dest_path_final.exists():
                    raise FileExistsError(
                        f"Destination directory {dest_path_final} already exists."
                    )
                shutil.copytree(self, dest_path_final)
            return self.__class__(dest_path_final)
        raise FileNotFoundError(
            f"Source path {self} does not exist or is not a file/directory."
        )

    def move_to(self, destination: typing.Union[os.PathLike, str])  :
        """Moves the file or directory to the specified location."""
        # str(self.path) -> str(self)
        moved_path_str = shutil.move(str(self), str(destination))
        return self.__class__(moved_path_str)

    def sync_to(
        self,
        destination: typing.Union[os.PathLike, str],
        delete_extraneous: bool = False,
        ignore_patterns: typing.List[str] = None,
        dry_run: bool = False,
    ):
        """
        Intelligently synchronizes this directory to a destination directory (like rsync).

        It only copies new or modified files, making it highly efficient for repeated runs.

        Args:
            destination: The target directory to sync to.
            delete_extraneous: If True, deletes files in the destination that do not
                               exist in the source directory (Mirroring). Defaults to False.
            ignore_patterns: A list of glob patterns to ignore during sync,
                             e.g., ['*.pyc', '__pycache__'].
            dry_run: If True, prints the operations that would be performed without
                     actually executing them. Defaults to False.
        """
        if not self.is_dir():
            raise NotADirectoryError(f"Source '{self}' is not a directory.")

        dest_path = NbPath(destination)
        if not dry_run:
            dest_path.mkdir(exist_ok=True)
        else:
            if not dest_path.exists():
                self.logger.info(f"[DRY RUN] Would create directory: {dest_path}")

        source_files = {p.relative_to(self) for p in self.rglob_files("*")}
        dest_files = {p.relative_to(dest_path) for p in dest_path.rglob_files("*")}

        # 1. Copy new or modified files
        for rel_path in source_files:
            source_file = self / rel_path
            dest_file = dest_path / rel_path

            # Simple ignore logic
            if ignore_patterns and any(rel_path.match(p) for p in ignore_patterns):
                continue

            if (
                not dest_file.exists()
                or source_file.stat().st_mtime > dest_file.stat().st_mtime
            ):
                if not dry_run:
                    self.logger.debug(f"Syncing: {source_file} -> {dest_file}")
                    dest_file.ensure_parent()
                    shutil.copy2(source_file, dest_file)
                else:
                    self.logger.info(
                        f"[DRY RUN] Would copy: {source_file} -> {dest_file}"
                    )

        # 2. Delete extraneous files if requested
        if delete_extraneous:
            for rel_path in dest_files - source_files:
                dest_file = dest_path / rel_path
                if not dry_run:
                    self.logger.debug(f"Deleting extraneous file: {dest_file}")
                    dest_file.delete(missing_ok=True)
                else:
                    self.logger.info(
                        f"[DRY RUN] Would delete extraneous file: {dest_file}"
                    )

    def download_from_url(
        self, url: str, overwrite: bool = False, **kwargs
    )  :
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
            raise ImportError(
                "requests and tqdm are required. Please run 'pip install requests tqdm'."
            )

        dest_path = self
        if dest_path.is_dir():
            file_name = url.split("/")[-1]
            dest_path = dest_path / file_name

        if dest_path.exists() and not overwrite:
            self.logger.warning(f"File {dest_path} already exists. Skipping download.")
            return dest_path

        dest_path.ensure_parent()

        with requests.get(url, stream=True, **kwargs) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            with (
                open(dest_path, "wb") as f,
                tqdm(
                    total=total_size, unit="iB", unit_scale=True, desc=dest_path.name
                ) as bar,
            ):
                for chunk in r.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    bar.update(size)
        return dest_path

    def expand(self) :
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
    def self_py_file(cls)  :
        """
        Returns an NbPath object representing the file path of the caller.
        This is a dynamic replacement for `NbPath(__file__)` that works from any module.
        """
        # sys._getframe(0) is the frame of self_py_file itself.
        # sys._getframe(1) is the frame of the caller.
        caller_filename = sys._getframe(1).f_code.co_filename
        return cls(caller_filename)

    @classmethod
    def self_py_dir(cls)  :
        caller_filename = sys._getframe(1).f_code.co_filename
        return cls(caller_filename).parent

    def find_git_root(self)  :
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
            return self.find_project_root(markers=[".git"])
        except FileNotFoundError as e:
            # Provide a more specific error message
            raise FileNotFoundError(
                f"Git root could not be found by searching upwards from {self}"
            ) from e

    def find_project_root(self, markers: typing.List[str] = None)  :
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
                "pyproject.toml",
                "setup.py",
                "requirements.txt",
                ".env",
                "manage.py",
                "venv",
                ".venv",
                ".idea",
                ".vscode",
            ]

        current = self.resolve()
        while True:
            for marker in markers:
                if (current / marker).exists():
                    self.logger.debug(
                        f"Project root found at: {current} (marker: '{marker}')"
                    )
                    return current

            if (
                current == current.parent
            ):  # Reached the filesystem root (e.g., '/' or 'C:\\')
                break
            current = current.parent

        raise FileNotFoundError(
            f"Project root could not be found by searching upwards from {self} using markers: {markers}"
        )

    def zip_to(
        self, destination: typing.Union[os.PathLike, str], overwrite: bool = False
    ):
        """
        Compresses the current file or directory into a ZIP file.
        :param destination: The path for the destination ZIP file.
        :param overwrite: If True, overwrites the destination file if it already exists.
        """
        dest_path = NbPath(destination)
        if dest_path.exists() and not overwrite:
            raise FileExistsError(f"Destination ZIP file already exists: {dest_path}")

        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if self.is_file():
                zf.write(self, self.name)
            elif self.is_dir():
                for file in self.rglob("*"):
                    zf.write(file, file.relative_to(self))

        return dest_path

    def unzip_to(self, destination: typing.Union[os.PathLike, str] = "."):
        """
        Extracts a ZIP file to a specified directory.
        :param destination: The directory to extract the files to.
        :return: An NbPath object of the destination directory.
        """
        dest_path = NbPath(destination)
        dest_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(self, "r") as zf:
            zf.extractall(dest_path)
        return dest_path

    def rglob_files(self, pattern: str) -> typing.List["NbPath"]:
        """Recursively finds all matching files and returns a list of NbPath objects."""
        # self.path.rglob -> self.rglob
        return [p for p in self.rglob(pattern) if p.is_file()]

    def rglob_dirs(self, pattern: str) -> typing.List["NbPath"]:
        """Recursively finds all matching directories and returns a list of NbPath objects."""
        return [p for p in self.rglob(pattern) if p.is_dir()]

    def grep(
        self,
        pattern: str,
        file_pattern: str = "*",
        is_regex: bool = True,
        ignore_case: bool = False,
        encoding: str = "utf-8",
        context: typing.Union[int, typing.Tuple[int, int]] = None,
    ) -> typing.Generator[GrepResult, None, None]:
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
                raise ValueError(
                    "`context` must be an integer or a tuple of two integers (before, after)."
                )

        for file in files_to_search:
            try:
                with file.open("r", encoding=encoding, errors="ignore") as f:
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

                            yield self.GrepResult(
                                file, line_num, line, match_result, context_lines
                            )

                        if before > 0:
                            lines_buffer.append((line_num, line))

            except Exception as e:
                self.logger.warning(f"Could not grep file {file}: {e}")

    def hash(self, algorithm: str = "sha256") -> str:
        """Calculates the hash of the file's content."""
        hasher = hashlib.new(algorithm)
        with self.open("rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    def is_text(self) -> bool:
        """
        Heuristically determines if a file is a text file.
        Returns False if the path is not a file.
        This is the inverse of is_binary().
        """
        if not self.is_file():
            return False
        return not self.is_binary()

    def is_binary(self) -> bool:
        """
        Heuristically determines if a file is binary by checking for null bytes.
        Returns False if the path is not a file.
        """
        if not self.is_file():
            return False
        try:
            with self.open("rb") as f:
                chunk = f.read(1024)  # Read the first 1KB of the file
                return b"\x00" in chunk
        except Exception as e:
            self.logger.warning(f"Could not perform binary check on file {self}: {e}")
            return False

    @contextmanager
    def lock(self, timeout: float = -1):
        """
        Provides a cross-process and cross-thread file lock using the `filelock` library.

        This is a context manager that ensures only one process or thread can exclusively
        access a code block for a given file path at a time. It works by creating a
        separate `.lock` file.

        Args:
            timeout (float): The maximum time in seconds to wait for the lock.
                             A value of -1 means wait indefinitely. Defaults to -1.

        Yields:
            The NbPath object itself, allowing for operations within the locked context.

        Raises:
            ImportError: If the `filelock` library is not installed.
                         Install it with `pip install nb-path[lock]` or `pip install filelock`.
            filelock.Timeout: If the lock could not be acquired within the timeout period.

        Example:
            >>> # Two different processes trying to write to the same file
            >>> counter_file = NbPath('counter.txt')
            >>> with counter_file.lock():
            ...     # This block is now safe from race conditions
            ...     current_value = int(counter_file.read_text() or 0)
            ...     counter_file.write_text(str(current_value + 1))
        """
        try:
            from filelock import FileLock, Timeout
        except ImportError:
            raise ImportError(
                "The 'filelock' library is required for the lock() method. "
                "Please install it with: pip install nb-path[lock]"
            )

        lock_file = self.parent / f"{self.name}.lock"
        file_lock = FileLock(lock_file, timeout=timeout)
        try:
            with file_lock:
                yield self
        except Timeout:
            raise Timeout(f"Could not acquire lock on {self} within {timeout} seconds.")

    @classmethod
    @contextmanager
    def tempfile(
        cls,
        suffix: str = None,
        prefix: str = None,
        dir: typing.Union[os.PathLike, str] = None,
        text: bool = False,
        cleanup: bool = True,
    ) -> typing.Generator["NbPath", None, None]:
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
            cleanup (bool, optional): If True (default), the file is automatically deleted on exiting
                                      the context. If False, the file is kept for debugging.

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
            suffix=suffix,
            prefix=prefix,
            dir=dir,
            delete=False,
            mode="w" if text else "w+b",
        )
        fp.close()  # Close the file handle immediately. We only wanted the unique name.

        temp_path = cls(fp.name)

        try:
            yield temp_path
        finally:
            # Robustly delete the file if it still exists upon exit.
            if cleanup:
                if temp_path.exists():
                    try:
                        temp_path.delete()
                    except Exception as e:
                        cls.logger.error(
                            f"Failed to delete temporary file {temp_path}: {e}"
                        )

    @classmethod
    @contextmanager
    def tempdir(
        cls,
        suffix: str = None,
        prefix: str = None,
        dir: typing.Union[os.PathLike, str] = None,
        cleanup: bool = True,
    ) -> typing.Generator["NbPath", None, None]:
        """
        Creates a temporary directory as a context manager, returning an NbPath object.

        This is a superior, object-oriented alternative to `tempfile.TemporaryDirectory`.
        The directory and all its contents are recursively deleted upon exiting the `with` block.

        Args:
            suffix (str, optional): If specified, the directory name will end with that suffix. Defaults to None.
            prefix (str, optional): If specified, the directory name will begin with that prefix. Defaults to None.
            dir (os.PathLike or str, optional): If specified, the directory will be created in that directory.
                                                If not specified, a default temporary directory is used.
            cleanup (bool, optional): If True (default), the directory and its contents are automatically
                                      deleted on exiting the context. If False, it is kept for debugging.

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
        if cleanup:
            with tempfile.TemporaryDirectory(
                suffix=suffix, prefix=prefix, dir=dir
            ) as temp_dir_str:
                yield cls(temp_dir_str)
        else:
            temp_dir_str = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
            yield cls(temp_dir_str)

    def as_importer(self) :
        """
        Returns an NbPathPyImporter instance of the current path,
        unlocking dynamic module import capabilities.
        """
        from nb_path.nb_path_py_impoter import NbPathPyImporter
        return NbPathPyImporter(self)
