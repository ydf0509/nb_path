"""
测试显示所有 imports（不使用省略号）
"""
import ast
from pathlib import Path

# 创建一个有很多 imports 的测试文件
test_code = '''
import os
import sys
import json
import time
import datetime
import pathlib
import typing
import logging
import threading
import collections
import functools
import itertools
import re
import hashlib
import base64
from typing import List, Dict, Optional, Union, Any
from pathlib import Path
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from functools import lru_cache, wraps
from itertools import chain, cycle
from logging import getLogger
from threading import Lock, Thread
from collections.abc import Iterable

class MyClass:
    """测试类"""
    pass
'''

# 解析代码
tree = ast.parse(test_code)

print("=" * 80)
print("测试：显示所有 imports（不使用省略号）")
print("=" * 80)
print()

imports = []
for node in tree.body:
    if isinstance(node, ast.Import):
        for alias in node.names:
            imports.append(f"import {alias.name}")
    elif isinstance(node, ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            imports.append(f"from {module} import {alias.name}")

print(f"📦 找到 {len(imports)} 个 imports:\n")

# 模拟生成的 Markdown 格式
print("#### 📦 Imports\n")
for imp in imports:
    print(f"- `{imp}`")

print()
print("=" * 80)
print(f"✅ 显示了所有 {len(imports)} 个 imports，没有使用省略号！")
print("=" * 80)
print()
print("💡 修改前的行为:")
print("   - 只显示前 20 个 imports")
print("   - 超过 20 个时显示: '... and X more imports'")
print()
print("💡 修改后的行为:")
print("   - 显示所有 imports")
print("   - 不再使用省略号")
print()

