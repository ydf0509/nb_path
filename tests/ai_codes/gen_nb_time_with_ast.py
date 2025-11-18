"""
生成 nb_time 项目的 Markdown 文档，包含 AST 元数据
这个版本会在每个 Python 文件前添加结构化的元数据信息
"""
from nb_path import AiMdGenerator, NbPath
from nb_log import get_logger

get_logger("nb_path")

ai_md = AiMdGenerator(
    r"tests/ai_docs/nb_time_with_ast_metadata.md"
)

(
    ai_md
    .set_project_name("nb_time")
    .clear_text()
    .auto_merge_from_python_project_some_files(
        project_root=r"D:\codes\nb_time",
    )
    .show_textfile_info()
    .merge_from_dir(
        project_root=r"D:\codes\nb_time",
        relative_dir_name="nb_time",
        use_gitignore=True,
        as_title="nb_time codes with AST metadata",
        should_include_suffixes=[".py", ".md"],
        excluded_dir_name_list=[],
        include_ast_metadata=True,  # 启用 AST 元数据
    )
    .show_textfile_info()
)

print("\n✅ 生成完成!")
print(f"📄 输出文件: {ai_md}")

