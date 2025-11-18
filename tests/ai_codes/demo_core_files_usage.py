"""
演示核心文件元数据提取功能的实际使用
"""
from pathlib import Path

print("=" * 80)
print("核心文件元数据提取功能 - 使用示例")
print("=" * 80)
print()

# 示例 1: 使用 add_project_summary
print("📋 示例 1: 在项目概述中添加核心文件元数据")
print("-" * 80)
print("""
from nb_path import AiMdGenerator

(
    AiMdGenerator("my_project_docs.md")
    .set_project_name("my_project")
    .clear_text()
    .add_project_summary(
        project_summary=\"""
        这是一个 FastAPI Web 项目。
        核心功能包括用户管理、数据分析、报表生成。
        \"",
        project_root="/path/to/project",
        most_core_source_code_file_list=[
            "src/main.py",        # 主入口
            "src/api/routes.py",  # API 路由
            "src/models/user.py", # 数据模型
        ],
    )
    .merge_from_dir(...)  # 然后再添加详细代码
)
""")
print()

# 示例 2: 使用 merge_from_files_with_metadata
print("📋 示例 2: 只提取元数据，不包含源码")
print("-" * 80)
print("""
from nb_path import AiMdGenerator

(
    AiMdGenerator("api_overview.md")
    .set_project_name("my_api")
    .clear_text()
    .merge_from_files_with_metadata(
        project_root="/path/to/project",
        relative_file_name_list=["src/api/routes.py", "src/models/user.py"],
        as_title="API 核心文件概览",
        include_ast_metadata=True,
        include_file_text=False,  # 🔑 只要元数据，不要源码
    )
)
""")
print()

# 对比效果
print("📊 效果对比")
print("-" * 80)
print("""
传统方式（包含完整源码）:
  ❌ 1 个文件 ~500 行 = ~2000 tokens
  ❌ 5 个核心文件 = ~10000 tokens

新方式（只要元数据）:
  ✅ 1 个文件元数据 = ~200 tokens
  ✅ 5 个核心文件 = ~1000 tokens
  
💡 节省 90% 的 tokens！
""")
print()

# 生成的文档结构
print("📝 生成的文档结构")
print("-" * 80)
print("""
# markdown content namespace: my_project project summary

项目概述文字...

---

## 📋 Core Source Files Metadata (Entry Points)

以下是项目最核心的入口文件的结构化元数据...

### 📄 Python File Metadata: `src/main.py`

#### 🔧 Public Functions (2)
- `def main() -> None`
- `def init_app() -> FastAPI`

---

### 📄 Python File Metadata: `src/api/routes.py`

#### 🏛️ Classes (1)
##### 📌 `class APIRouter`

**Public Methods (3):**
- `def get_users(self, page: int = 1) -> List[User]`
- `def create_user(self, user_data: UserCreate) -> User`
- `def delete_user(self, user_id: int) -> bool`

---

（注意：这里只有函数签名和类结构，没有完整源码！）

# markdown content namespace: 详细源代码

（后面才是完整的源码...）
""")
print()

print("=" * 80)
print("✅ 功能说明完成！")
print("=" * 80)
print()
print("💡 核心优势:")
print("  • 让 AI 先看懂项目结构，再深入细节")
print("  • 节省 token，提高效率")
print("  • 适合大型项目的概览和 API 文档")
print()

