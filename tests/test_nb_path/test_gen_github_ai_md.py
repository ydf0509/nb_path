from nb_path import gen_github_proj_docs_and_codes_ai_md
from nb_path import NbPath


# 使用示例
if __name__ == "__main__":
    # 示例：生成 sqlmodel 项目的文档
    gen_github_proj_docs_and_codes_ai_md(
        github_zip_url="https://codeload.github.com/fastapi/sqlmodel/zip/refs/heads/main",
        output_md_path=NbPath(r'D:\codes\nb_path\tests\markdown_gen_files_git_ignore\ai_md_files\other_peoples',"sqlmodel_docs_and_codes.md"),
        readme_file="README.md",
        docs_dir_name="docs",
        codes_dir_name="sqlmodel",
        should_include_suffixes=[".py", ".md",]
    )