#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检测文件编码的脚本
"""
import nb_log

import chardet
from nb_path import NbPath


def detect_file_encoding(file_path):
    """
    检测文件编码
    """
    # 读取文件的原始字节
    raw_data = NbPath(file_path).read_bytes()
    
    # 使用chardet检测编码
    result = chardet.detect(raw_data)
    
    return result['encoding'], result['confidence']


if __name__ == "__main__":
    # 要检测的文件路径
    file_to_check = r"D:\codes\nb_path\tests\markdown_gen_files_git_ignore\ai_txt_files\nb_aiohttp_all_docs_and_codes.txt"
    
    try:
        encoding, confidence = detect_file_encoding(file_to_check)
        print(f"文件编码: {encoding}")
        print(f"置信度: {confidence:.2f}")
    except Exception as e:
        print(f"检测文件编码时出错: {e}")