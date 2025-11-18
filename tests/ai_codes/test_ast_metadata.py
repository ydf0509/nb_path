"""测试 AiMdGenerator 的 AST 元数据功能"""
from nb_path import AiMdGenerator, NbPath
from nb_log import get_logger

get_logger("nb_path")

# 测试文件路径
test_output = NbPath("tests/ai_docs/test_ast_output.md")

# 生成带有 AST 元数据的 Markdown
(
    AiMdGenerator(test_output)
    .set_project_name("nb_path")
    .clear_text()
    .merge_from_files_with_metadata(
        project_root=NbPath.self_py_dir().parent,
        relative_file_name_list=["nb_path/nb_path_class.py"],
        as_title="NbPath Core Class with AST Metadata",
        include_ast_metadata=True,
    )
    .show_textfile_info()
)

print(f"\n✅ 测试完成! 输出文件: {test_output}")
print(f"📊 文件大小: {test_output.size_human()}")
print(f"📝 文件行数: {test_output.get_textfile_info()['line_count']}")

