# AiMdGenerator AST 元数据演示

这是使用 AST 解析功能生成的 Python 文件元数据

---

## 类: `AiMdGenerator`

**行号**: 8

**文档字符串**:
```
An extremely powerful context generator born for AI collaboration.

This class is designed to revolutionize how developers interact with Large Language
Models (LLMs). It intelligently merges multiple project source files into a single,
well-structured, and context-rich Markdown file, providing the AI with a perfect
```

**继承**: NbPath

**方法统计**:
- 总方法数: 15
- 公有方法: 6
- 私有方法: 9

### 公有方法 (6)

#### `set_project_name(self, project_name: str) -> Str`

*行号: 118*

**说明**: Sets the project name for the current markdown file.

---

#### `add_project_summary(self, project_summary: str) -> Str`

*行号: 129*

**说明**: Adds a project summary to the current markdown file.

---

#### `auto_merge_from_python_project_some_files(self, project_root) -> Str`

*行号: 177*

**说明**: 自动合并项目根目录下的 readme.md 或者ReADME.md 以及setup.py 和 pyproject.toml ，如果有就添加

---

#### `merge_from_files(self, project_root: Subscript, relative_file_name_list: Subscript, as_title: str) -> Str`

*行号: 200*

**说明**: Merges the content of the given files into the current markdown file.

---

#### `merge_from_dir(self, project_root: Subscript, relative_dir_name: str, as_title: str, should_include_suffixes: Subscript, excluded_dir_name_list: Subscript, excluded_file_name_list: Subscript, use_gitignore: bool, dry_run: bool, include_ast_metadata: bool) -> Str`

*行号: 257*

**说明**: Merges the content of the given directory into the current file.

---

#### `merge_from_files_with_metadata(self, project_root: Subscript, relative_file_name_list: Subscript, as_title: str, include_ast_metadata: bool) -> Str`

*行号: 695*

**说明**: 合并文件内容到 Markdown，对于 Python 文件会额外生成 AST 元数据

---

