"""
测试 BOM (Byte Order Mark) 字符处理

BOM 是 UTF-8 文件开头的特殊标记 U+FEFF，有些编辑器会添加它。
Python 的 ast.parse() 不接受 BOM，所以需要先移除。
"""
import ast
from pathlib import Path

print("=" * 80)
print("测试 BOM (Byte Order Mark) 字符处理")
print("=" * 80)
print()

# 测试代码（带 BOM）
test_code_with_bom = '\ufeff# -*- coding: utf-8 -*-\nimport os\n\nclass MyClass:\n    pass'
test_code_without_bom = '# -*- coding: utf-8 -*-\nimport os\n\nclass MyClass:\n    pass'

print("📋 什么是 BOM?")
print("-" * 80)
print("BOM (Byte Order Mark) 是 Unicode 字符 U+FEFF")
print("在 UTF-8 文件中表示为: \\ufeff")
print("有些 Windows 编辑器会在 UTF-8 文件开头添加它")
print("Python 的 ast.parse() 不接受 BOM，会报错")
print()

print("📋 测试 1: 尝试解析带 BOM 的代码")
print("-" * 80)
try:
    tree = ast.parse(test_code_with_bom)
    print("✅ 成功解析（不应该发生）")
except SyntaxError as e:
    print(f"❌ 解析失败（预期）: {e}")
    print(f"   错误类型: invalid non-printable character U+FEFF")
print()

print("📋 测试 2: 移除 BOM 后再解析")
print("-" * 80)
if test_code_with_bom.startswith('\ufeff'):
    print("✅ 检测到 BOM 字符")
    cleaned_code = test_code_with_bom[1:]
    print("✅ 移除 BOM 字符")
    try:
        tree = ast.parse(cleaned_code)
        print("✅ 成功解析!")
        
        # 统计节点
        imports = sum(1 for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom)))
        classes = sum(1 for node in tree.body if isinstance(node, ast.ClassDef))
        
        print(f"   - 找到 {imports} 个 import")
        print(f"   - 找到 {classes} 个 class")
    except SyntaxError as e:
        print(f"❌ 解析失败: {e}")
print()

print("📋 测试 3: 解析没有 BOM 的代码")
print("-" * 80)
try:
    tree = ast.parse(test_code_without_bom)
    print("✅ 成功解析（正常情况）")
except SyntaxError as e:
    print(f"❌ 解析失败: {e}")
print()

print("=" * 80)
print("✅ 修复方案")
print("=" * 80)
print("""
在 _parse_python_file_ast() 方法中添加:

```python
source_code = file_path.read_text(encoding="utf-8")

# 移除 BOM 字符
if source_code.startswith('\\ufeff'):
    source_code = source_code[1:]
    
tree = ast.parse(source_code, filename=str(file_path))
```

这样就能正确处理带 BOM 的 Python 文件了！
""")
print()

print("💡 如何检查文件是否有 BOM?")
print("-" * 80)
print("方法 1: 用十六进制编辑器查看文件开头")
print("        UTF-8 BOM 是: EF BB BF")
print()
print("方法 2: 用 Python 检查")
print("        with open('file.py', 'rb') as f:")
print("            if f.read(3) == b'\\xef\\xbb\\xbf':")
print("                print('有 BOM')")
print()
print("方法 3: 用 chardet 检测")
print("        result = chardet.detect(file_bytes)")
print("        if 'BOM' in str(result):")
print("            print('有 BOM')")
print()

