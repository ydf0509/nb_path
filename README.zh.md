# nb_path: 赋予文件系统操作超能力的 Python 路径库

<p align="center">
  <a href="README.md">[English](README.md)</a> | <a href="README.zh.md">[简体中文](README.zh.md)</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/nb-path/"><img src="https://img.shields.io/pypi/v/nb-path.svg" alt="pypi"></a>
  <a href="https://pypi.org/project/nb-path/"><img src="https://img.shields.io/pypi/pyversions/nb-path.svg" alt="pyversions"></a>
  <a href="https://github.com/ydf0509/nb_path"><img src="https://img.shields.io/github/stars/ydf0509/nb_path" alt="github stars"></a>
</p>

`nb_path` 是一个对 Python 标准库 `pathlib.Path` 的超级增强版。它完全继承了 `pathlib` 的所有优雅特性（包括 `/` 操作符），并在此基础上无缝集成了 `shutil` 的高级文件操作、`zipfile` 的压缩解压、`hashlib` 的哈希计算、`importlib` 的动态模块导入，甚至还内置了 `grep` 搜索和 `rsync` 风格的目录同步等强大功能。

它的设计哲学是：**将所有与路径相关的常用操作，都变成路径对象自身的方法，从而实现极致流畅的链式调用。**

## 🆚 与 `pathlib` 对比

`nb_path` 不仅仅是 `pathlib` 的简单封装，而是一个功能强大的超集。

| 功能 (Feature) | `pathlib.Path` | `nb_path.NbPath` | 优势说明 |
| :--- | :---: | :---: | :--- |
| **基本路径操作** | ✅ | ✅ | `nb_path` 完全继承并兼容 `pathlib` 的所有功能 |
| **高级文件/目录操作** | ❌ | ✅ | 内置 `copy_to`, `move_to`, `delete`, `empty` 等方法 |
| **确保父目录存在** | ❌ | ✅ | `ensure_parent()` 方法，避免 `FileNotFoundError` |
| **压缩与解压** | ❌ | ✅ | `zip_to()` 和 `unzip_to()`，轻松处理归档文件 |
| **内容搜索 (grep)** | ❌ | ✅ | `grep()` 方法，在文件或目录中进行高效文本搜索 |
| **目录智能同步** | ❌ | ✅ | `sync_to()` 方法，实现 `rsync` 风格的增量同步 |
| **网络文件下载** | ❌ | ✅ | `download_from_url()` 方法，直接将文件下载到路径 |
| **AI 上下文生成** | ❌ | ✅ | `AiMdGenerator`，为大语言模型构建结构化上下文 |
| **项目根目录发现** | ❌ | ✅ | `find_project_root()` 和 `find_git_root()`，告别路径烦恼 |
| **动态模块导入** | ❌ | ✅ | `import_as_module()`，是插件化开发的利器 |
| **便捷的临时文件/目录** | ❌ | ✅ | `tempfile()` 和 `tempdir()` 上下文管理器，自动清理 |
| **进程安全文件锁** | ❌ | ✅ | `lock()` 上下文管理器，用于并发文件访问 |
| **实用工具集** | ❌ | ✅ | 内置 `hash()`, `size_human()`, `expand()` 等多种便捷工具 |

## ✨ 核心特性

- **完全兼容 `pathlib`**: 无缝迁移，零学习成本。
- **强大的文件/目录操作**: `copy_to`, `move_to`, `delete`, `empty`, `ensure_parent` 等，比 `shutil` 更直观。
- **智能压缩与解压**: `zip_to()` 和 `unzip_to()`，轻松处理 ZIP 文件。
- **内置 `grep` 功能**: `grep()` 方法，可在文件或整个目录中进行高效的文本/正则搜索。
- **目录智能同步**: `sync_to()` 方法，一个轻量级的 `rsync`，可智能同步两个目录。
- **网络文件下载**: `download_from_url()`，直接将文件从 URL 下载到指定路径。
- **AI 驱动开发**: `AiMdGenerator` 类，可将你的整个项目智能打包成一个结构化的 Markdown 文件，极大地增强你与大语言模型（LLM）的协作效率。
- **项目根目录发现**: `find_project_root()` 和 `find_git_root()`，告别烦人的相对路径计算。
- **动态模块导入**: `import_as_module()`，可以将任何 `.py` 文件作为模块动态导入，是插件化开发的利器。
- **便捷的临时文件/目录**: `tempfile()` 和 `tempdir()` 上下文管理器，返回功能完备的 `NbPath` 对象，自动清理。
- **实用工具集**: `hash()`, `size_human()`, `expand()` 等，满足日常开发中的各种小需求。

## 🚀 安装

```bash
pip install nb-path
```

## ⚡ 快速上手：优雅的链式调用

想象一下这个常见的自动化任务：下载一个 ZIP 包，解压，找到特定文件，处理其内容，然后保存到项目的 `output` 目录。

使用 `nb_path`，整个过程可以一气呵成：

```python
from nb_path import NbPath

# 模拟一个数据源 URL
MOCK_URL = "https://example.com/data.zip" 

# 在一个临时的、会自动清理的工作区中执行所有操作
with NbPath.tempdir(prefix="data-processing-") as workspace:
    print(f"创建临时工作区: {workspace}")

    # 核心操作：下载 -> 解压 -> 在解压目录中查找 -> 读取 -> 处理
    unzipped_dir = (
        (workspace / "downloaded.zip")
        .download_from_url(MOCK_URL, overwrite=True)
        .unzip_to(workspace / "unzipped")
    )

    processed_content = (
        unzipped_dir.rglob_files("data.txt")[0].read_text().upper()
    )

    # 将处理结果保存到项目的输出目录
    output_file = (
        (NbPath.self_py_dir() / "output" / "report.txt")
        .ensure_parent()
        .write_text(processed_content)
    )

    print(f"处理完成，结果已保存至: {output_file}")

print("临时工作区已自动清理。")
```

这个例子完美展示了 `nb_path` 的核心优势：**高内聚、高可读、高效率**。

## 🤖 AI 协作神器: `AiMdGenerator`

在 AI 时代，向大语言模型（LLM）提供完整、结构化的上下文，是获得高质量回答的关键。`AiMdGenerator` 正是为此而生的革命性工具。

它将手动复制粘贴代码这一繁琐、易错的过程，变成了一行优雅的链式调用。它能智能地将你的项目文档、源代码、测试用例打包成一个组织良好的 Markdown 文件，这正是 AI 最喜欢的格式。

**为什么这是 AI 协作的“游戏规则改变者”？**

- **提供上帝视角**: 生成的 Markdown 包含文件清单和清晰的边界，使 AI 能立即理解你的项目架构。
- **信息完整性**: AI 得到的是完整、准确的源代码，避免了因手动操作导致的信息丢失。
- **增强安全性**: `use_gitignore=True` 功能是一个至关重要的安全屏障，它会自动排除 `.env` 等包含敏感信息的文件。

下面展示了如何将你的整个项目打包，以便进行 AI 代码审查：

```python
from nb_path import AiMdGenerator

# 将文档、源码、测试打包成一个文件，提供给 AI
(
    AiMdGenerator("project_context_for_ai.md")
    .clear_text()  # 清空旧文件
    .merge_from_files(
        relative_file_name_list=["README.md"],
         project_root="/path/to/your/proj",
        as_title="项目文档",
    )
    .merge_from_dir(
         project_root="/path/to/your/proj",
        relative_dir_name="nb_path", # 主源码目录
        as_title="项目源码",
        use_gitignore=True,  # 自动使用 .gitignore 规则
        should_include_suffixes=[".py"],
    )
    .merge_from_dir(
         project_root="/path/to/your/proj",
        relative_dir_name="tests", # 测试目录
        as_title="项目测试",
        use_gitignore=True,
        should_include_suffixes=[".py"],
        excluded_dir_name_list=["tests/markdown_gen_files"],
    )
)
```

现在，你只需将生成的 `project_context_for_ai.md` 文件提供给你最喜欢的 LLM，就能获得远比以前更深入、更准确的分析。

### 为什么不直接在 IDE 中提问 AI，而是要生成 Markdown 文件？

这是一个非常深刻的问题，触及了当前 AI 辅助编程的核心痛点。

在编程 IDE（如 Cursor、Trace）中，AI 助手为了控制高昂的 Token 成本，通常不会一次性阅读你项目的所有代码。它们可能会采取分块阅读的策略（例如，每 200 行作为一个代码块），这意味着要完整理解一个功能，AI 可能需要进行多次、零散的阅读。这种机制旨在防止用户一次性提交数万行代码导致费用失控，但其代价是 AI 的上下文是碎片化的，容易产生“幻觉”或给出不准确的回答。

而 `AiMdGenerator` 解决了这个问题。它生成的单一、结构化的 Markdown 文件，可以被上传到拥有超大上下文窗口（如 Google AI Studio 中 Gemini 模型的 100万 Token 上下文）的强大模型中。这使得 AI 能够：

- **一次性全量阅读**: AI 可以完整地、一次性地加载整个项目的上下文，形成全局视角，而不是管中窥豹。
- **推理能力更强，幻觉更少**: 拥有了完整的上下文，AI 的推理链条不会中断，能够准确理解冷门第三方库的用法和复杂框架的内部逻辑，从而给出极其准确、几乎没有幻觉的回答和代码建议。

简而言之，`AiMdGenerator` 是将你的项目代码“喂”给最强大脑（如 Gemini）的最佳方式，是实现高质量 AI 辅助开发的关键一步。

## 📖 API 使用指南

以下是 `nb_path` 主要功能的详细介绍和示例。

### 1. 文件与目录操作

```python
from nb_path import NbPath

# 确保父目录存在，然后创建一个空文件
p = NbPath("data/reports/2024/sales.csv").ensure_parent().touch()

# 复制文件
p_copy = p.copy_to("data/reports/2024/sales_backup.csv")

# 移动文件
p_moved = p_copy.move_to("data/archive/sales_2024.csv")

# 删除文件
p_moved.delete()

# 创建一个目录并清空它
report_dir = NbPath("data/reports").empty()

# 递归删除整个目录树
report_dir.delete()
```

### 2. 文本与数据读写

`nb_path` 继承了 `pathlib` 的 `read_text`/`write_text` 和 `read_bytes`/`write_bytes`，并为文本操作默认使用 `utf-8` 编码。

```python
p = NbPath("config.txt")

# 写入文本
p.write_text("setting=enabled")

# 读取文本
content = p.read_text()
print(content)  # "setting=enabled"
```

### 3. 搜索与发现

#### 递归查找文件/目录

```python
src_dir = NbPath("./my_project")

# 查找所有 Python 文件
py_files = src_dir.rglob_files("*.py")

# 查找所有名为 'tests' 的目录
test_dirs = src_dir.rglob_dirs("tests")
```

#### `grep`：在文件中搜索内容

这是 `nb_path` 的一个“杀手级”功能。
```python
import sys
project_dir = NbPath("./my_project")

# 1. 在所有 .py 文件中搜索字符串 "import requests"
for result in project_dir.grep("import requests", file_pattern="*.py", is_regex=False):
    print(f"{result.path.name}:{result.line_number}: {result.line_content.strip()}")

# 2. 使用正则表达式查找所有 Flask 路由
for result in project_dir.grep(r"@app\.route\(['\"](.*?)['\"]\)", file_pattern="*.py"):
    print(f"发现路由: {result.match.group(1)}")

# 3. 搜索时显示前后各2行上下文
for result in project_dir.grep("important_logic", context=2, file_pattern="*.py"):
    print("-" * 20)
    for num, line_text in result.context_lines:
        prefix = ">>" if num == result.line_number else "  "
        sys.stdout.write(f"{prefix} {num:4d}: {line_text.rstrip()}\n")
```

### 4. 项目与路径导航

```python
# 自动找到当前文件所在的 Git 仓库的根目录
git_root = NbPath(__file__).find_git_root()

# 根据标记文件（如 'pyproject.toml'）找到项目根目录
project_root = NbPath().find_project_root()

# 动态获取调用方的文件路径或目录路径
current_file = NbPath.self_py_file()
current_dir = NbPath.self_py_dir()

# 展开环境变量和用户目录
# NbPath('$HOME/.config/my_app').expand() -> /home/user/.config/my_app
# NbPath('~/.bashrc').expand() -> /home/user/.bashrc
config_path = NbPath("$HOME/.config").expand()
```

### 5. 压缩与解压

```python
assets_dir = NbPath("./assets")

# 将整个目录压缩成一个 ZIP 文件
zip_file = assets_dir.zip_to("assets_archive.zip", overwrite=True)

# 将 ZIP 文件解压到指定目录
unzipped_dir = zip_file.unzip_to("./unzipped_assets")
```

### 6. 网络与同步

#### 从 URL 下载文件

```python
# 下载一个图片并显示进度条
image_path = NbPath("python_logo.png").download_from_url(
    "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png",
    overwrite=True
)
print(f"图片已下载至: {image_path}, 大小: {image_path.size_human()}")
```

#### `sync_to`：智能同步目录

此方法只会复制新增或被修改的文件，非常高效。

```python
source_dir = NbPath("./src")
deploy_dir = NbPath("./deploy")

# 将源目录同步到部署目录
# delete_extraneous=True 会删除部署目录中多余的文件（镜像同步）
source_dir.sync_to(deploy_dir, delete_extraneous=True, ignore_patterns=['*.pyc', '__pycache__'])

# 执行一次“演习”(dry run)，查看将要发生什么，但并不实际修改任何文件
print("\n--- Performing a dry run ---")
source_dir.sync_to(deploy_dir, delete_extraneous=True, dry_run=True)
```

### 7. 临时文件与目录

`nb_path` 提供了比标准库更易用的上下文管理器，并且返回的是 `NbPath` 对象。

```python
# 创建一个临时的配置文件
with NbPath.tempfile(suffix=".txt", prefix="config_") as tmp_file:
    print(f"临时文件: {tmp_file}")
    tmp_file.write_text("temporary setting")
    # 此代码块结束时，文件会被自动删除

# 创建一个临时的插件工作区
with NbPath.tempdir(prefix="plugin_") as tmp_dir:
    print(f"临时目录: {tmp_dir}")
    (tmp_dir / "plugin.py").write_text("print('hello from plugin')")
    # 此代码块结束时，目录及其所有内容会被自动删除

# 为了调试，你可以禁止自动清理
with NbPath.tempdir(cleanup=False) as persistent_tmp_dir:
    persistent_tmp_dir.joinpath("log.txt").write_text("一些调试信息")
    print(f"这个目录将不会被删除: {persistent_tmp_dir}")
assert persistent_tmp_dir.exists()
```

### 8. 动态模块导入 (高级功能)

这是 `nb_path` 最独特的功能之一，对于构建插件系统或动态加载脚本非常有用。

```python
from nb_path import NbPath

# 将任意 .py 文件作为模块导入
my_plugin_module = NbPath("./plugins/my_plugin.py").as_importer().import_as_module()

# 调用插件中的函数
my_plugin_module.run()

# 自动导入一个目录下的所有 .py 文件
plugins_dir = NbPath("./plugins").as_importer().auto_import_pyfiles_in_dir()
```

### 9. 实用工具

```python
p = NbPath("my_large_file.dat")
p.write_bytes(b"0" * 5 * 1024 * 1024) # 写入 5MB 数据

# 获取文件大小（字节）
print(p.size())  # 5242880

# 获取人类可读的文件大小
print(p.size_human())  # "5.0 MB"

# 计算文件哈希值
print(p.hash())  # 'f3a3535...' (sha256)
print(p.hash('md5')) # 'a74f6...' (md5)
```

## 贡献

欢迎任何形式的贡献！如果您有好的想法、功能建议或发现了 Bug，请随时提交 Issues 或 Pull Requests。

## 许可证

本项目基于 MIT License 开源。