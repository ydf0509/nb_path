from re import T
from nb_path import NbPath, NbPathPyImporter, AiMdGenerator
import logging
from pathlib import Path

if __name__ == "__main__":
    # --- Testing the new NbPath class ---
    from nb_log import get_logger

    get_logger("NbPath").setLevel(logging.DEBUG)

    print(type(NbPath("/")))
    print(type(NbPath(__file__)))
    print(type(NbPath(__file__).parent))
    print(type(NbPath(__file__).parent / "a.txt"))

    cur_dir = NbPath(__file__).parent
    print(type(cur_dir))
    cur_file = NbPath(__file__)
    print(NbPath(cur_file))

    print(NbPath(cur_dir, "adir", "bdir", "c.txt"))

    print(repr(NbPath().resolve()))
    print(NbPath().resolve())

    print(repr(Path().resolve()))
    print(Path().resolve())

    print(NbPath.self_py_file())
    print(NbPath.self_py_dir())
    print(NbPath.self_py_file().hash())

    print(
        list(
            cur_dir.rglob_files(
                "*.py",
            )
        )
    )

    NbPath(r"D:\codes\nb_path\tests\temps").zip_to(
        NbPath(r"D:\codes\nb_path\tests", "temps_zip.zip"), overwrite=True
    )
    print(
        NbPath(r"D:\codes\nb_path\tests", "temps_zip.zip").unzip_to(
            NbPath("d:/codes/nb_path/tests", "temps_unzip")
        )
    )

    print(NbPath("~/.config").expand())

    print(f"find_git_root: {NbPath().find_git_root()}")
    print(f"find_project_root: {repr(NbPath().find_project_root())}")

    print(
        NbPath("d:/codes/nb_path/tests", "baidu.html").download_from_url(
            "https://www.baidu.com", overwrite=True
        )
    )

    print(NbPath("d:/codes/nb_path/tests", "baidu.html").size_human())

    print(NbPathPyImporter(r"D:\codes\nb_path\tests\m1.py").import_as_module())

    print(NbPathPyImporter(r"D:\codes\nb_path\tests\m1.py").get_module_name())

    NbPathPyImporter(r"D:\codes\nb_path\tests\pacb").auto_import_pyfiles_in_dir()

    NbPath("d:/codes/nb_path/tests/temps").sync_to(
        "d:/codes/nb_path/tests/temps_sync", dry_run=True
    )
    NbPath("d:/codes/nb_path/tests/temps").sync_to(
        "d:/codes/nb_path/tests/temps_sync", dry_run=False
    )

    AiMdGenerator(r"D:\codes\nb_path\tests\markdown_gen_files\ai_md.md").delete().merge_from_files(
        relative_file_name_list=[
            "tests/pacb/m3.py",
            "tests/pacb/m4.py",
            "tests/pacb/m5.md",
        ],
        project_root=r"D:\codes\nb_path",
        as_title="my title111",
    )
    
    nb_path_ai_md = NbPath(r"D:\codes\nb_path\tests\markdown_gen_files\nb_path_all_docs_and_codes.md")
    
    (
        AiMdGenerator(nb_path_ai_md)
        .clear_text()
        .merge_from_files(
            relative_file_name_list=["README.md"],
            project_root=r"D:\codes\nb_path",
            as_title="nb_path docs",
        )
        .merge_from_dir(
            project_root=r"D:\codes\nb_path",
            relative_dir_name="nb_path",
            use_gitignore=True,
            as_title="nb_path codes",
            # 只包含 .py 和 .md 文件
            should_include_suffixes=[".py", ".md"],
            # 排除 __pycache__ 目录和特定的测试文件
            excluded_dir_name_list=["tests/markdown_gen_files"],
        )
        .merge_from_dir(
            project_root=r"D:\codes\nb_path",
            relative_dir_name="tests/test_nb_path",
            use_gitignore=True,
            as_title="nb_path tests",
            # 只包含 .py 和 .md 文件
            should_include_suffixes=[".py", ".md"],
            # 排除 __pycache__ 目录和特定的测试文件
            excluded_dir_name_list=["tests/markdown_gen_files"],
        )
        .get_textfile_info(is_show_info=True)
    )

   


