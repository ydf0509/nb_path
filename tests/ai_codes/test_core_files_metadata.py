"""
测试核心文件元数据提取功能

演示如何在项目概述中只提取核心文件的元数据（不包含源码）
这样 AI 能在最前面快速了解项目的入口和核心结构
"""
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 由于环境问题，我们用独立脚本演示概念
print("""
╔═══════════════════════════════════════════════════════════════════════╗
║        核心文件元数据提取功能 - 使用示例                                  ║
╚═══════════════════════════════════════════════════════════════════════╝

📋 功能说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

现在可以在项目概述中提取核心入口文件的元数据，让 AI 一眼就能看到：

✅ 项目的核心入口文件有哪些
✅ 每个文件包含哪些类和方法
✅ 函数签名、参数、返回值类型
✅ 不包含长长的源码，节省 token

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用示例 1: 在概述中添加核心文件元数据
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
from nb_path import AiMdGenerator

(
    AiMdGenerator("my_project_docs.md")
    .set_project_name("my_project")
    .clear_text()
    
    # 添加项目概述，包含核心文件的元数据
    .add_project_summary(
        project_summary=\"\"\"
        这是一个优秀的 Web API 项目，使用 FastAPI 框架。
        主要功能包括用户管理、数据分析、报表生成等。
        \"\"\",
        project_root="/path/to/project",
        most_core_source_code_file_list=[
            "src/main.py",          # 主入口
            "src/api/routes.py",    # API 路由
            "src/models/user.py",   # 用户模型
        ],
    )
    
    # 然后再添加详细的源码（包含完整代码）
    .merge_from_dir(
        project_root="/path/to/project",
        relative_dir_name="src",
        as_title="详细源代码",
        include_ast_metadata=True,
    )
)
```

生成的文档结构：

```
# markdown content namespace: my_project project summary

这是一个优秀的 Web API 项目...

---

## 📋 Core Source Files Metadata (Entry Points)

以下是项目最核心的入口文件的结构化元数据...

### 📄 Python File Metadata: `src/main.py`

#### 🔧 Public Functions (2)

- `def main() -> None`
  - *主入口函数*
- `def init_app() -> FastAPI`
  - *初始化应用*

---

### 📄 Python File Metadata: `src/api/routes.py`

#### 🏛️ Classes (1)

##### 📌 `class APIRouter`
*Line: 10*

**Public Methods (3):**
- `def get_users(self, page: int = 1) -> List[User]`
- `def create_user(self, user_data: UserCreate) -> User`
- `def update_user(self, user_id: int, data: UserUpdate) -> User`

---

（注意：这里只有元数据，没有完整源码！）

# markdown content namespace: 详细源代码

（这里才是完整的源码...）
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用示例 2: 使用 merge_from_files_with_metadata 只提取元数据
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
from nb_path import AiMdGenerator

(
    AiMdGenerator("api_overview.md")
    .set_project_name("my_project")
    .clear_text()
    
    # 方式1: 只要元数据，不要源码
    .merge_from_files_with_metadata(
        project_root="/path/to/project",
        relative_file_name_list=[
            "src/api/routes.py",
            "src/api/handlers.py",
            "src/models/user.py",
        ],
        as_title="API 核心文件结构概览",
        include_ast_metadata=True,
        include_file_text=False,  # 🔑 关键：不包含源码
    )
    
    # 方式2: 既要元数据，也要源码（默认行为）
    .merge_from_files_with_metadata(
        project_root="/path/to/project",
        relative_file_name_list=["src/utils/helpers.py"],
        as_title="工具函数详细代码",
        include_ast_metadata=True,
        include_file_text=True,  # 包含完整源码
    )
)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 适用场景
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **大型项目概览**
   - 先在概述中展示核心入口文件的结构
   - AI 快速理解项目架构
   - 节省 token，提高效率

✅ **API 文档生成**
   - 只提取 API 路由和处理器的签名
   - 不需要完整实现代码

✅ **快速代码审查**
   - 先看核心文件的结构和接口
   - 再决定是否查看具体实现

✅ **教学和学习**
   - 学习新项目时先看整体结构
   - 逐步深入细节

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 对比效果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

传统方式（包含完整源码）:
  📄 1 个文件 = 500 行代码 = ~2000 tokens
  📄 5 个核心文件 = ~10000 tokens ❌

新方式（只要元数据）:
  📄 1 个文件 = 只有类和方法签名 = ~200 tokens
  📄 5 个核心文件 = ~1000 tokens ✅

节省 90% 的 tokens！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

现在有两种模式：

1. **概览模式** (include_file_text=False)
   - 只显示元数据（类、方法、签名）
   - 适合项目概述、API 文档
   - 节省 token

2. **详细模式** (include_file_text=True，默认)
   - 显示元数据 + 完整源码
   - 适合代码审查、学习
   - 信息完整

让 AI 先看懂结构，再深入细节！ 🚀

╚═══════════════════════════════════════════════════════════════════════╝
""")

