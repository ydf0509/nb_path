import logging
import nb_log
from nb_path import NbPath
import sys

if __name__ == '__main__':
    nb_log.get_logger('NbPath').setLevel(logging.DEBUG)
    src_dir = NbPath('d:/codes/nb_path')
    for result in src_dir.grep("error", file_pattern='*.py', is_regex=False,):
            print(f"{result.path.name}:{result.line_number}: {result.line_content.strip()}")

    for result in src_dir.grep("error", context=5, file_pattern='*.py', is_regex=False):
            print("-" * 20)
            for num, line_text in result.context_lines:
                prefix = ">>" if num == result.line_number else "  "
                sys.stdout.write(f"{prefix} {num:4d}: {line_text.rstrip()}\n")