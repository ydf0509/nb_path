# nb_path: A Python Path Library with Filesystem Superpowers

<p align="center">
  <a href="https://pypi.org/project/nb-path/">[English](README.md)</a> | <a href="README.zh.md">[简体中文](README.zh.md)</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/nb-path/"><img src="https://img.shields.io/pypi/v/nb-path.svg" alt="pypi"></a>
  <a href="https://pypi.org/project/nb-path/"><img src="https://img.shields.io/pypi/pyversions/nb-path.svg" alt="pyversions"></a>
  <a href="https://github.com/ydf0509/nb_path"><img src="https://img.shields.io/github/stars/ydf0509/nb_path" alt="github stars"></a>
</p>

`nb_path` is a super-enhanced version of Python's standard `pathlib.Path`. It fully inherits all the elegant features of `pathlib` (including the `/` operator) and seamlessly integrates advanced file operations from `shutil`, compression/decompression from `zipfile`, hash calculation from `hashlib`, dynamic module loading from `importlib`, and even includes powerful built-in features like `grep` search and `rsync`-style directory synchronization.

Its design philosophy is: **to turn all common path-related operations into methods of the path object itself, enabling an extremely fluid chain of calls.**

## 🆚 Comparison with `pathlib`

`nb_path` is not just a simple wrapper around `pathlib`; it's a powerful superset.

| Feature | `pathlib.Path` | `nb_path.NbPath` | Advantage |
| :--- | :---: | :---: | :--- |
| **Basic Path Operations** | ✅ | ✅ | `nb_path` fully inherits and is compatible with all `pathlib` features |
| **Advanced File/Dir Ops** | ❌ | ✅ | Built-in methods like `copy_to`, `move_to`, `delete`, `empty` |
| **Ensure Parent Exists** | ❌ | ✅ | `ensure_parent()` method prevents `FileNotFoundError` |
| **Compression/Decompression** | ❌ | ✅ | `zip_to()` and `unzip_to()` for easy archive handling |
| **Content Search (grep)** | ❌ | ✅ | `grep()` method for efficient text search in files or directories |
| **Intelligent Dir Sync** | ❌ | ✅ | `sync_to()` method for `rsync`-style incremental synchronization |
| **Network File Download** | ❌ | ✅ | `download_from_url()` method to download a file directly to the path |
| **Project Root Discovery** | ❌ | ✅ | `find_project_root()` and `find_git_root()` to end path headaches |
| **Dynamic Module Import** | ❌ | ✅ | `import_as_module()` is a powerful tool for plugin development |
| **Convenient Temp Files/Dirs** | ❌ | ✅ | `tempfile()` and `tempdir()` context managers with auto-cleanup |
| **Utility Toolkit** | ❌ | ✅ | Built-in utilities like `hash()`, `size_human()`, `expand()` |

## ✨ Core Features

- **Fully `pathlib` Compatible**: Seamless migration, zero learning curve.
- **Powerful File/Directory Operations**: `copy_to`, `move_to`, `delete`, `empty`, `ensure_parent`, etc., are more intuitive than `shutil`.
- **Smart Compression & Decompression**: `zip_to()` and `unzip_to()` for easy handling of ZIP files.
- **Built-in `grep` Functionality**: The `grep()` method allows for efficient text/regex searches in files or entire directories.
- **Intelligent Directory Sync**: The `sync_to()` method, a lightweight `rsync`, can intelligently synchronize two directories.
- **Network File Download**: `download_from_url()` downloads a file from a URL directly to the specified path.
- **Project Root Discovery**: `find_project_root()` and `find_git_root()` eliminate tedious relative path calculations.
- **Dynamic Module Import**: `import_as_module()` can dynamically import any `.py` file as a module, a powerful tool for plugin-based development.
- **Convenient Temp Files/Dirs**: `tempfile()` and `tempdir()` context managers return fully-featured `NbPath` objects and handle cleanup automatically.
- **Utility Toolkit**: `hash()`, `size_human()`, `expand()`, and more to meet various daily development needs.

## 🚀 Installation

```bash
pip install nb-path
```

## ⚡ Quick Start: Elegant Chaining

Imagine this common automation task: download a ZIP archive, extract it, find a specific file, process its content, and then save it to the project's `output` directory.

With `nb_path`, the entire process can be done in one go:

```python
from nb_path import NbPath

# Simulate a data source URL
MOCK_URL = "https://example.com/data.zip" 

# Perform all operations in a temporary, auto-cleaning workspace
with NbPath.tempdir(prefix="data-processing-") as workspace:
    print(f"Created temporary workspace: {workspace}")

    # Core operations: download -> unzip -> find in unzipped dir -> read -> process
    unzipped_dir = (workspace / "downloaded.zip") \
        .download_from_url(MOCK_URL, overwrite=True) \
        .unzip_to(workspace / "unzipped")

    processed_content = unzipped_dir.rglob_files("data.txt")[0] \
        .read_text() \
        .upper()

    # Save the processed result to the project's output directory
    output_file = (NbPath.self_py_dir() / "output" / "report.txt") \
        .ensure_parent() \
        .write_text(processed_content)

    print(f"Processing complete, result saved to: {output_file}")

print("Temporary workspace has been automatically cleaned up.")
```

This example perfectly demonstrates the core advantages of `nb_path`: **high cohesion, high readability, and high efficiency.**

## 📖 API Guide

Here is a detailed guide to the main features of `nb_path` with examples.

### 1. File and Directory Operations

```python
from nb_path import NbPath

# Ensure parent directory exists, then create an empty file
p = NbPath("data/reports/2024/sales.csv").ensure_parent().touch()

# Copy the file
p_copy = p.copy_to("data/reports/2024/sales_backup.csv")

# Move the file
p_moved = p_copy.move_to("data/archive/sales_2024.csv")

# Delete the file
p_moved.delete()

# Create a directory and then empty it
report_dir = NbPath("data/reports").empty()

# Recursively delete the entire directory tree
report_dir.delete()
```

### 2. Text and Data I/O

`nb_path` inherits `read_text`/`write_text` and `read_bytes`/`write_bytes` from `pathlib` and defaults to `utf-8` encoding for text operations.

```python
p = NbPath("config.txt")

# Write text
p.write_text("setting=enabled")

# Read text
content = p.read_text()
print(content)  # "setting=enabled"
```

### 3. Search and Discovery

#### Recursively Find Files/Directories

```python
src_dir = NbPath("./my_project")

# Find all Python files
py_files = src_dir.rglob_files("*.py")

# Find all directories named 'tests'
test_dirs = src_dir.rglob_dirs("tests")
```

#### `grep`: Search for Content in Files

This is one of `nb_path`'s "killer features".

```python
project_dir = NbPath("./my_project")

# 1. Search for the string "import requests" in all .py files
for result in project_dir.grep("import requests", file_pattern="*.py", is_regex=False):
    print(f"{result.path.name}:{result.line_number}: {result.line_content.strip()}")

# 2. Use a regular expression to find all Flask routes
for result in project_dir.grep(r"@app\.route\(['\"](.*?)['\"]\)", file_pattern="*.py"):
    print(f"Found route: {result.match.group(1)}")

# 3. Search with 2 lines of context before and after
for result in project_dir.grep("important_logic", context=2, file_pattern="*.py"):
    print("-" * 20)
    for num, line_text in result.context_lines:
        prefix = ">>" if num == result.line_number else "  "
        sys.stdout.write(f"{prefix} {num:4d}: {line_text.rstrip()}\n")
```

### 4. Project and Path Navigation

```python
# Automatically find the root of the Git repository containing the current file
git_root = NbPath(__file__).find_git_root()

# Find the project root based on marker files (e.g., 'pyproject.toml')
project_root = NbPath().find_project_root()

# Expand environment variables and user directories
# NbPath('$HOME/.config/my_app').expand() -> /home/user/.config/my_app
# NbPath('~/.bashrc').expand() -> /home/user/.bashrc
config_path = NbPath("$HOME/.config").expand()
```

### 5. Compression and Decompression

```python
assets_dir = NbPath("./assets")

# Compress the entire directory into a ZIP file
zip_file = assets_dir.zip_to("assets_archive.zip", overwrite=True)

# Extract the ZIP file to a specified directory
unzipped_dir = zip_file.unzip_to("./unzipped_assets")
```

### 6. Network and Synchronization

#### Download a File from a URL

```python
# Download an image and display a progress bar
image_path = NbPath("python_logo.png").download_from_url(
    "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png",
    overwrite=True
)
print(f"Image downloaded to: {image_path}, Size: {image_path.size_human()}")
```

#### `sync_to`: Intelligent Directory Synchronization

This method only copies new or modified files, making it highly efficient.

```python
source_dir = NbPath("./src")
deploy_dir = NbPath("./deploy")

# Synchronize the source directory to the deployment directory
# delete_extraneous=True will delete extra files in the destination (mirroring)
source_dir.sync_to(deploy_dir, delete_extraneous=True, ignore_patterns=['*.pyc', '__pycache__'])
```

### 7. Temporary Files and Directories

`nb_path` provides more user-friendly context managers than the standard library, and they return `NbPath` objects.

```python
# Create a temporary configuration file
with NbPath.tempfile(suffix=".txt", prefix="config_") as tmp_file:
    print(f"Temporary file: {tmp_file}")
    tmp_file.write_text("temporary setting")
    # The file is automatically deleted when this block is exited

# Create a temporary plugin workspace
with NbPath.tempdir(prefix="plugin_") as tmp_dir:
    print(f"Temporary directory: {tmp_dir}")
    (tmp_dir / "plugin.py").write_text("print('hello from plugin')")
    # The directory and all its contents are automatically deleted here
```

### 8. Dynamic Module Import (Advanced Feature)

This is one of the most unique features of `nb_path`, very useful for building plugin systems or dynamically loading scripts.

```python
from nb_path import NbPathPyImporter

# Import any .py file as a module
plugin_path = NbPathPyImporter("./plugins/my_plugin.py")
my_plugin_module = plugin_path.import_as_module()

# Call a function from the plugin
my_plugin_module.run()

# Automatically import all .py files in a directory
plugins_dir = NbPathPyImporter("./plugins")
plugins_dir.auto_import_pyfiles_in_dir()
```

### 9. Utilities

```python
p = NbPath("my_large_file.dat")
p.write_bytes(b"0" * 5 * 1024 * 1024) # Write 5MB of data

# Get file size in bytes
print(p.size())  # 5242880

# Get human-readable file size
print(p.size_human())  # "5.0 MB"

# Calculate file hash
print(p.hash())  # 'f3a3535...' (sha256)
print(p.hash('md5')) # 'a74f6...' (md5)
```

## Contributing

Contributions of any kind are welcome! If you have good ideas, feature suggestions, or have found a bug, please feel free to submit an Issue or Pull Request.

## License

This project is open-sourced under the MIT License.
