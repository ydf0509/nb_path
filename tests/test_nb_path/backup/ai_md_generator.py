

from nb_path import NbPath
import typing
import os
import fnmatch

class AiMdGenerator(NbPath):
    """
    An extremely powerful context generator born for AI collaboration.

    This class is designed to revolutionize how developers interact with Large Language
    Models (LLMs). It intelligently merges multiple project source files into a single,
    well-structured, and context-rich Markdown file, providing the AI with a perfect
    and comprehensive project snapshot.

    The benefits for large AI models are immense:
    1.  **Provides a God's-eye View**: Through a file manifest, clear file boundaries,
        and relative paths, the AI can easily construct the project's overall
        architecture and understand file dependencies and relationships, rather than
        fumbling in the dark.
    2.  **Ensures Information Integrity and Accuracy**: The AI receives complete,
        unabridged source file content, avoiding the chaos, omissions, or context
        loss caused by manual copy-pasting. This enables it to provide more precise
        analysis and suggestions.
    3.  **Enhances Security**: The built-in `use_gitignore` feature is a critical
        security barrier. It automatically ignores files containing sensitive
        information (like API keys or database passwords) such as `.env` or local
        configs, allowing you to share code without fear of accidental leaks.

    Its core methods, `merge_from_files` and `merge_from_dir`, offer extreme
    flexibility. Combined with the elegant chainable calls of `nb_path`, creating a
    high-quality AI context is transformed from a tedious, error-prone manual task
    into a single, delightful line of code.

    Example:
        >>> # Imagine you want an AI to review your entire project
        >>> (
        ...     AiMdGenerator("project_context_for_ai.md")
        ...     .delete()  # Clear the old file
        ...     .merge_from_files(
        ...         relative_file_name_list=["README.md"],
        ...         project_root=".",
        ...         as_title="Project Documentation",
        ...     )
        ...     .merge_from_dir(
        ...         project_root="/path/to/your/project",
        ...         relative_dir_name="nb_path", # The main source code directory
        ...         as_title="Project Source Code",
        ...         use_gitignore=True,  # Automatically use .gitignore rules
        ...         should_include_suffixes=[".py", ".md"], # Only include specified file types
        ...     )
        ...     .merge_from_dir(
        ...         project_root="/path/to/your/project",
        ...         relative_dir_name="tests", # The tests directory
        ...         as_title="Project Tests",
        ...         use_gitignore=True,
        ...         should_include_suffixes=[".py"],
        ...         excluded_dir_name_list=["tests/markdown_gen_files", "tests/temps_sync"],
        ...     )
        ... )
    """

    """cn description
    一个极其强大的、为 AI 协作而生的上下文生成器。

    此类旨在彻底改变开发者与大语言模型（LLM）的交互方式。它能够智能地将多个项目源文件
    合并成一个结构清晰、上下文丰富的单一 Markdown 文件，从而为 AI 提供一个完美、全面的项目快照。

    对 AI 大模型的好处是巨大的：
    1.  **提供上帝视角**：通过文件清单、清晰的文件边界和相对路径，AI 能够轻松构建出项目的
        整体架构，理解文件间的依赖和引用关系，而不是盲人摸象。
    2.  **确保信息的完整与准确**：AI 得到的是未经删减的、完整的源文件内容，避免了因手动
        复制粘贴导致的格式混乱、内容遗漏或上下文缺失，从而能给出更精准的分析和建议。
    3.  **提升安全性**：内置的 `use_gitignore` 功能是一道关键的安全屏障。它能自动忽略
        `.env`、本地配置等包含敏感信息（如 API 密钥、数据库密码）的文件，让你在分享代码
        时无需担心意外泄露秘密。

    其核心方法 `merge_from_files` 和 `merge_from_dir` 提供了极高的灵活性，结合 `nb_path`
    优雅的链式调用，使得创建一个高质量的 AI 上下文从繁琐、易错的手工劳动，变成了一行
    赏心悦目的代码。

    """

    suffix__lang_map = {
        ".py": "python",
        ".md": "markdown",
        ".txt": "text",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".html": "html",
        ".css": "css",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".vue": "vue",
        ".php": "php",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "h",
        ".hpp": "hpp",
        ".cs": "csharp",
        ".vb": "vb",
        ".sql": "sql",
        ".bat": "batch",
        ".sh": "shell",
        ".ps1": "powershell",
        ".psm1": "powershell",
        ".psd1": "powershell",
        ".pssc": "powershell",
        ".psscx": "powershell",
    }

    def _generate_markdown_header(self, as_title: str, file_text_list: list) -> list:
        """生成包含文件树和文件列表的 Markdown 头部"""
        str_list = [f"# markdown content namespace: {as_title} \n\n"]

        # 1. 生成文件树
        str_list.append("## File Tree\n\n")
        str_list.append("```\n")
        tree = {}
        sorted_paths = sorted([item[1] for item in file_text_list])
        for path in sorted_paths:
            parts = path.split('/')
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

        def format_tree(node, prefix=""):
            lines = []
            entries = sorted(node.keys())
            for i, entry in enumerate(entries):
                connector = "├── " if i < len(entries) - 1 else "└── "
                lines.append(f"{prefix}{connector}{entry}")
                if node[entry]:
                    extension = "│   " if i < len(entries) - 1 else "    "
                    lines.extend(format_tree(node[entry], prefix + extension))
            return lines

        str_list.extend(format_tree(tree))
        str_list.append("\n```\n\n---\n\n")

        # 2. 生成文件列表
        str_list.append("## Included Files\n\n")
        for _, relative_file_name_posix, _, _ in file_text_list:
            str_list.append(f"- `{relative_file_name_posix}`\n")
        str_list.append("\n---\n\n")

        return str_list

    def merge_from_files(
        self,
        project_root: typing.Union[os.PathLike, str],
        relative_file_name_list: typing.List[str],
        as_title: str,
    ) -> "AiMdGenerator":
        """Merges the content of the given files into the current markdown file.
        the current markdown file will be used to upload to ai model for code review and learning.
        """
        file_text_list = []
        project_root_path = NbPath(project_root).resolve()
        for relative_file_name in relative_file_name_list:
            file = (project_root_path / relative_file_name).resolve()
            if file.is_file() and file.is_text():
                relative_file_name_posix = file.relative_to(
                    project_root_path
                ).as_posix()
                try:
                    text = file.read_text()
                except Exception as e:
                    self.logger.error(f"Error reading file {file}: {e}")
                    text = ""
                file_text_list.append(
                    [file, relative_file_name_posix, file.suffix, text]
                )
                self.logger.debug(f"need merged file: {file}")
            else:
                raise ValueError(f"File {file} is not a text file.")
        str_list = []
        if file_text_list:
            # 调用新函数生成头部
            str_list.extend(self._generate_markdown_header(as_title, file_text_list))


        for file, relative_file_name_posix, suffix, text in file_text_list:
            # 2. Remove the debug print statement.
            # print(f'file: {file}, relative_file_name_posix: {relative_file_name_posix}, suffix: {suffix}, text: {text}')
            str_list.append(f"### code file start: {relative_file_name_posix} \n")
            # 3. Handle .md files separately to ensure their content is rendered correctly.
            #    Other file types are wrapped in code blocks.
            if suffix == ".md":
                str_list.append(text + "\n")
            else:
                lang = self.suffix__lang_map.get(suffix, "text")
                str_list.append(f"```{lang}\n{text}\n```\n")

            str_list.append(f"**code file end: {relative_file_name_posix}**\n")
            str_list.append("---\n\n")

        # with self.open(mode="a", encoding="utf-8") as f:
        #     f.write("\n".join(str_list))
        self.append_text('\n'.join(str_list))
        self.ensure_utf8_bom()
        return self
        
        
    def merge_from_dir(
        self,
        project_root: typing.Union[os.PathLike, str],
        relative_dir_name: str,
        as_title: str,
        should_include_suffixes: typing.List[str] = [],
        excluded_dir_name_list: typing.List[str] = [],
        excluded_file_name_list: typing.List[str] = [],
        use_gitignore: bool = True,
        dry_run: bool = False,
    ) -> "AiMdGenerator":
        """Merges the content of the given directory into the current file."""
        project_root_path = NbPath(project_root).resolve()
        target_dir_path = (project_root_path / relative_dir_name).resolve()

        # Use sets for efficient lookups
        excluded_dir_paths = {
            (project_root_path / d).resolve() for d in excluded_dir_name_list
        }
        excluded_file_paths = {
            (project_root_path / f).resolve() for f in excluded_file_name_list
        }

        ignore_patterns = []
        if use_gitignore:
            try:
                gitignore_path = project_root_path.find_git_root() / ".gitignore"
                if gitignore_path.is_file():
                    self.logger.debug(f"Using .gitignore rules from: {gitignore_path}")
                    with open(gitignore_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                # Gitignore patterns always use forward slashes.
                                # We will compare against the posix version of the relative path
                                # for cross-platform reliability.
                                ignore_patterns.append(line)
            except FileNotFoundError:
                self.logger.warning("use_gitignore is True, but no .git/ or .gitignore file found.")

        relative_paths_to_include = []
        for path_obj in target_dir_path.rglob("*"):
            # Automatically exclude directories starting with a dot at the project root
            try:
                first_part = path_obj.relative_to(project_root_path).parts[0]
                if first_part.startswith('.'):
                    continue
            except (ValueError, IndexError):
                continue
            # Check if the path is within any of the excluded directories
            is_in_excluded_dir = any(
                path_obj == excluded_dir or excluded_dir in path_obj.parents
                for excluded_dir in excluded_dir_paths
            )
            if is_in_excluded_dir:
                continue

            # Check if the path matches any gitignore patterns.
            # Convert the relative path to a posix-style string for reliable matching.
            relative_to_root = path_obj.relative_to(project_root_path)
            relative_posix_path = relative_to_root.as_posix()
            # Use fnmatch for robust gitignore-style pattern matching.
            is_ignored = False
            for p in ignore_patterns:
                # If a pattern does not contain a slash, it matches in any directory.
                # e.g., 'test_git_ignore1.py' should match 'nb_path/example_dir/test_git_ignore1.py'
                if '/' not in p.strip('/'):
                    p_glob = f"**/{p.strip('/')}"
                else:
                    p_glob = p
                if fnmatch.fnmatch(relative_posix_path, p_glob) or fnmatch.fnmatch(relative_posix_path, p):
                    is_ignored = True
                    break
            if is_ignored:
                self.logger.debug(f"Ignoring {relative_to_root} due to .gitignore rule.")
                continue

            if path_obj.is_file():
                # Check if the file itself is excluded
                if path_obj.resolve() in excluded_file_paths:
                    continue
                # Check if the file is a text file
                if not path_obj.is_text():
                    continue
                # Check if the suffix is in the inclusion list (if the list is not empty)
                if (
                    should_include_suffixes
                    and path_obj.suffix not in should_include_suffixes
                ):
                    continue
                relative_paths_to_include.append(
                    path_obj.relative_to(project_root_path).as_posix()
                )

        if dry_run:
            print("\n--- [DRY RUN] AiMdGenerator Execution Plan ---")
            print(f"\n✅ {len(relative_paths_to_include)} files would be INCLUDED in '{self.name}':")
            for p in sorted(relative_paths_to_include):
                print(f"  - {p}")
            print("\n--- End of DRY RUN ---")
            return self
        else:
            return self.merge_from_files(project_root, relative_paths_to_include, as_title)
