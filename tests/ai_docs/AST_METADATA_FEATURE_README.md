# AiMdGenerator AST 元数据功能说明

## 🎯 功能概述

`AiMdGenerator` 现在支持使用 Python 的 AST (Abstract Syntax Tree) 模块自动解析 Python 文件,提取结构化元数据,包括:

- 📦 **导入信息**: 所有 import 和 from...import 语句
- 🏛️ **类定义**: 类名、继承关系、装饰器、文档字符串
- 🔧 **函数/方法**: 函数名、参数列表、类型注解、返回值类型、装饰器
- 📝 **文档字符串**: 模块、类、函数的完整文档
- 🎨 **属性和装饰器**: 类属性、@property 装饰器等

## 💡 为什么需要 AST 元数据?

### 问题：传统方式的局限

传统的文件合并只是简单地将代码内容复制到 Markdown,AI 需要:
1. ❌ 逐行阅读大量代码才能理解结构
2. ❌ 容易遗漏关键的类型信息和继承关系
3. ❌ 难以快速定位特定的函数或类
4. ❌ 容易产生幻觉,误解代码结构

### 解决方案：结构化元数据

使用 AST 元数据后,AI 能够:
1. ✅ 快速浏览文件的整体结构（目录式）
2. ✅ 准确理解类型注解和函数签名
3. ✅ 清楚看到继承关系和装饰器
4. ✅ 高效定位和推理,减少幻觉
5. ✅ 更适合构建 RAG 知识库

## 🚀 使用方法

### 方法 1: 使用 `merge_from_files_with_metadata`

```python
from nb_path import AiMdGenerator

(
    AiMdGenerator("output.md")
    .set_project_name("my_project")
    .clear_text()
    .merge_from_files_with_metadata(
        project_root="/path/to/project",
        relative_file_name_list=["src/main.py", "src/utils.py"],
        as_title="Project Core Files",
        include_ast_metadata=True,  # 启用 AST 元数据
    )
)
```

### 方法 2: 使用 `merge_from_dir` (推荐)

```python
from nb_path import AiMdGenerator

(
    AiMdGenerator("output.md")
    .set_project_name("my_project")
    .clear_text()
    .merge_from_dir(
        project_root="/path/to/project",
        relative_dir_name="src",
        as_title="Source Code",
        use_gitignore=True,
        should_include_suffixes=[".py"],
        include_ast_metadata=True,  # 启用 AST 元数据（默认为 True）
    )
)
```

### 禁用 AST 元数据

如果只想要原始代码,不需要元数据:

```python
.merge_from_dir(
    ...
    include_ast_metadata=False,  # 禁用 AST 元数据
)
```

## 📊 生成的元数据格式

### 对于每个 Python 文件,会生成以下结构:

```markdown
### 📄 Python File Metadata: `src/example.py`

#### 📝 Module Docstring
```
模块的文档字符串
```

#### 📦 Imports
- `import os`
- `from typing import List, Dict`
- `from pathlib import Path`

#### 🏛️ Classes (2)

##### 📌 `class MyClass(BaseClass)`
*Line: 15*

**Docstring:**
```
这是一个示例类
用于演示 AST 元数据功能
```

**Public Methods (3):**
- `def __init__(self, name: str, age: int = 0) -> None`
  - *初始化方法*
- `def process_data(self, data: List[str]) -> Dict[str, Any]`
  - *处理数据*
- `async def fetch_data(self, url: str) -> bytes`
  - *异步获取数据*

**Properties (1):**
- `@property name -> str`

#### 🔧 Public Functions (2)

- `def helper_function(x: int, y: int = 10) -> int` `@lru_cache`
  - *Line: 45*
  - *辅助函数*
```

## 🎨 实际示例

### 生成前（传统方式）

```markdown
--- **start of file: src/example.py** ---
```python
class MyClass(BaseClass):
    def __init__(self, name):
        self.name = name
    
    def process_data(self, data):
        ...
```
--- **end of file: src/example.py** ---
```

AI 需要完整阅读代码才能理解 `MyClass` 的结构。

### 生成后（包含 AST 元数据）

```markdown
--- **start of file: src/example.py** ---

### 📄 Python File Metadata: `src/example.py`

#### 🏛️ Classes (1)

##### 📌 `class MyClass(BaseClass)`
*Line: 10*

**Public Methods (2):**
- `def __init__(self, name: str) -> None`
- `def process_data(self, data: List[Dict]) -> ProcessedData`
  - *处理输入数据并返回结构化结果*

---

```python
class MyClass(BaseClass):
    def __init__(self, name):
        self.name = name
    
    def process_data(self, data):
        ...
```
--- **end of file: src/example.py** ---
```

AI 可以先通过元数据了解结构,再根据需要查看具体实现。

## 🛠️ 技术细节

### Python 版本兼容性

- ✅ Python 3.7+: 使用手工 AST 遍历
- ✅ Python 3.8+: 同上
- ✅ Python 3.9+: 使用 `ast.unparse()` 获得更准确的类型注解

### 提取的信息

1. **函数/方法**:
   - 名称、行号
   - 参数列表（含类型注解和默认值）
   - 返回值类型注解
   - 装饰器列表
   - 文档字符串
   - 是否是异步函数
   - 是否是公有方法（不以 `_` 开头）

2. **类**:
   - 名称、行号
   - 基类（继承关系）
   - 装饰器
   - 文档字符串
   - 公有/私有方法列表
   - Property 属性列表
   - 类变量

3. **导入**:
   - import 语句
   - from...import 语句
   - 别名（as）

## 🔍 适用场景

### 1. AI 代码审查
让 AI 快速理解项目结构,提供更准确的建议

### 2. 代码文档生成
自动生成 API 文档级别的结构化描述

### 3. RAG 知识库构建
结构化的元数据更适合向量化和检索

### 4. 代码分析工具
快速分析项目的类和函数分布

### 5. 学习和理解新项目
通过元数据快速了解项目架构

## 📋 完整示例

```python
from nb_path import AiMdGenerator

# 为 nb_time 项目生成带 AST 元数据的文档
(
    AiMdGenerator("nb_time_analysis.md")
    .set_project_name("nb_time")
    .clear_text()
    .add_project_summary(
        "nb_time 是一个优雅的时间处理库,支持链式调用和时区转换。"
    )
    .auto_merge_from_python_project_some_files(
        project_root="/path/to/nb_time"
    )
    .merge_from_dir(
        project_root="/path/to/nb_time",
        relative_dir_name="nb_time",
        as_title="nb_time Source Code with Metadata",
        use_gitignore=True,
        should_include_suffixes=[".py"],
        include_ast_metadata=True,  # 启用 AST 元数据
    )
    .show_textfile_info()
)
```

## 🎯 性能考虑

- AST 解析速度很快,对于中等项目（< 1000 个文件）几乎感觉不到延迟
- 生成的 Markdown 文件会比原来大约增加 20-30%
- 元数据放在代码内容之前,不影响阅读完整代码

## ⚙️ 配置选项

```python
# 完整的配置示例
.merge_from_dir(
    project_root="/path/to/project",
    relative_dir_name="src",
    as_title="Source Code",
    should_include_suffixes=[".py", ".md"],  # 只处理特定后缀
    excluded_dir_name_list=["tests", "__pycache__"],  # 排除目录
    excluded_file_name_list=["setup.py"],  # 排除文件
    use_gitignore=True,  # 遵守 .gitignore 规则
    dry_run=False,  # 是否只显示将要处理的文件
    include_ast_metadata=True,  # 是否包含 AST 元数据
)
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进 AST 元数据功能!

## 📝 更新日志

### v1.0.0 (2025-01-17)
- ✨ 新增 AST 元数据提取功能
- ✨ 支持类、函数、方法的完整解析
- ✨ 兼容 Python 3.7+
- ✨ 自动生成结构化的 Markdown 元数据
- ✨ 新增 `merge_from_files_with_metadata` 方法
- ✨ 为 `merge_from_dir` 添加 `include_ast_metadata` 参数

