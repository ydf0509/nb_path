"""独立测试 AST 解析功能 - 兼容 Python 3.7+"""
import ast
import sys
from pathlib import Path


def ast_to_source(node):
    """将 AST 节点转换为源代码字符串，兼容 Python 3.7+"""
    if node is None:
        return ""
    try:
        # Python 3.9+ 支持 ast.unparse
        if hasattr(ast, 'unparse'):
            return ast.unparse(node)
        else:
            # Python 3.7/3.8 的回退方案
            # 简单的手工处理常见情况
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Constant):
                return repr(node.value)
            elif isinstance(node, ast.Attribute):
                value = ast_to_source(node.value)
                return f"{value}.{node.attr}"
            elif isinstance(node, ast.Subscript):
                value = ast_to_source(node.value)
                slice_val = ast_to_source(node.slice)
                return f"{value}[{slice_val}]"
            elif hasattr(node, 's'):  # Python 3.7 的 Str 节点
                return repr(node.s)
            elif hasattr(node, 'n'):  # Python 3.7 的 Num 节点
                return str(node.n)
            else:
                # 对于复杂类型，返回类型名称
                return node.__class__.__name__
    except Exception as e:
        return f"<parse_error: {e}>"


def parse_type_annotation(annotation) -> str:
    """解析类型注解，返回字符串表示"""
    return ast_to_source(annotation)


def extract_function_metadata(node):
    """提取函数/方法的元数据"""
    metadata = {
        "name": node.name,
        "type": "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
        "lineno": node.lineno,
        "docstring": ast.get_docstring(node) or "",
        "parameters": [],
        "return_type": parse_type_annotation(node.returns),
        "decorators": [ast_to_source(dec) for dec in node.decorator_list],
        "is_public": not node.name.startswith("_"),
    }

    # 提取参数信息
    for arg in node.args.args:
        param_info = {
            "name": arg.arg,
            "type": parse_type_annotation(arg.annotation),
            "default": None,
        }
        metadata["parameters"].append(param_info)

    return metadata


def extract_class_metadata(node):
    """提取类的元数据"""
    metadata = {
        "name": node.name,
        "type": "class",
        "lineno": node.lineno,
        "docstring": ast.get_docstring(node) or "",
        "bases": [ast_to_source(base) for base in node.bases],
        "methods": [],
        "is_public": not node.name.startswith("_"),
    }

    # 遍历类的成员
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method_info = extract_function_metadata(item)
            metadata["methods"].append(method_info)

    return metadata


def parse_python_file(file_path):
    """解析 Python 文件的 AST"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        tree = ast.parse(source_code, filename=str(file_path))
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return None

    metadata = {
        "file": str(file_path),
        "module_docstring": ast.get_docstring(tree) or "",
        "classes": [],
        "functions": [],
        "imports": [],
    }

    # 只获取顶层定义
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            metadata["classes"].append(extract_class_metadata(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            metadata["functions"].append(extract_function_metadata(node))

    return metadata


# 测试
if __name__ == "__main__":
    print(f"🐍 Python 版本: {sys.version}")
    print(f"📦 AST 支持 unparse: {hasattr(ast, 'unparse')}\n")
    
    # 测试文件路径
    test_file = Path(__file__).parent.parent.parent / "nb_path" / "ai_md_generator.py"
    
    print(f"🔍 正在解析文件: {test_file.name}")
    print(f"📁 文件路径: {test_file}")
    print(f"✅ 文件存在: {test_file.exists()}\n")
    
    if test_file.exists():
        metadata = parse_python_file(test_file)
        
        if metadata:
            print("=" * 60)
            print(f"📊 解析结果统计")
            print("=" * 60)
            print(f"🏛️  类数量: {len(metadata['classes'])}")
            print(f"🔧 顶级函数数量: {len(metadata['functions'])}")
            
            # 显示类详情
            for cls in metadata['classes']:
                print(f"\n{'=' * 60}")
                print(f"📌 类: {cls['name']}")
                print(f"{'=' * 60}")
                print(f"继承: {', '.join(cls['bases']) if cls['bases'] else 'object'}")
                print(f"行号: {cls['lineno']}")
                
                if cls['docstring']:
                    doc_preview = cls['docstring'].split('\n')[0][:80]
                    print(f"文档: {doc_preview}...")
                
                # 统计方法
                public_methods = [m for m in cls['methods'] if m['is_public']]
                private_methods = [m for m in cls['methods'] if not m['is_public']]
                
                print(f"\n方法统计:")
                print(f"  - 公有方法: {len(public_methods)}")
                print(f"  - 私有方法: {len(private_methods)}")
                
                # 显示前5个公有方法
                print(f"\n前5个公有方法:")
                for method in public_methods[:5]:
                    params = ", ".join([p['name'] for p in method['parameters']])
                    return_type = f" -> {method['return_type']}" if method['return_type'] else ""
                    print(f"  • {method['name']}({params}){return_type}")
                    if method['docstring']:
                        doc = method['docstring'].split('\n')[0][:60]
                        print(f"    → {doc}")
            
            # 显示顶级函数
            if metadata['functions']:
                print(f"\n{'=' * 60}")
                print(f"🔧 顶级函数")
                print(f"{'=' * 60}")
                for func in metadata['functions']:
                    if func['is_public']:
                        params = ", ".join([p['name'] for p in func['parameters']])
                        print(f"  • {func['name']}({params})")
            
            print(f"\n{'=' * 60}")
            print("✅ 测试完成!")
            print(f"{'=' * 60}")
    else:
        print("❌ 文件不存在!")
