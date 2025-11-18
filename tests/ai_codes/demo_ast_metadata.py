"""
演示 AST 元数据功能

这个脚本会生成一个包含 AST 元数据的 Markdown 文件
"""
import sys
from pathlib import Path

# 添加项目路径（避免导入错误）
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 由于 nb_path_class.py 有 Python 3.10+ 的语法，我们直接使用独立脚本生成演示
import ast

def ast_to_source_simple(node):
    """简单的 AST 转源码"""
    if node is None:
        return ""
    if hasattr(ast, 'unparse'):
        return ast.unparse(node)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{ast_to_source_simple(node.value)}.{node.attr}"
    return node.__class__.__name__

# 解析 ai_md_generator.py
file_path = project_root / "nb_path" / "ai_md_generator.py"
with open(file_path, 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

output_file = project_root / "tests" / "ai_docs" / "ast_metadata_demo.md"
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as out:
    out.write("# AiMdGenerator AST 元数据演示\n\n")
    out.write("这是使用 AST 解析功能生成的 Python 文件元数据\n\n")
    out.write("---\n\n")
    
    # 获取类信息
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            out.write(f"## 类: `{node.name}`\n\n")
            out.write(f"**行号**: {node.lineno}\n\n")
            
            # 文档字符串
            docstring = ast.get_docstring(node)
            if docstring:
                first_lines = '\n'.join(docstring.split('\n')[:5])
                out.write(f"**文档字符串**:\n```\n{first_lines}\n```\n\n")
            
            # 继承
            if node.bases:
                bases = [ast_to_source_simple(base) for base in node.bases]
                out.write(f"**继承**: {', '.join(bases)}\n\n")
            
            # 方法统计
            methods = [item for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]
            public_methods = [m for m in methods if not m.name.startswith('_')]
            
            out.write(f"**方法统计**:\n")
            out.write(f"- 总方法数: {len(methods)}\n")
            out.write(f"- 公有方法: {len(public_methods)}\n")
            out.write(f"- 私有方法: {len(methods) - len(public_methods)}\n\n")
            
            # 公有方法详情
            out.write(f"### 公有方法 ({len(public_methods)})\n\n")
            for method in public_methods:
                # 参数
                params = []
                for arg in method.args.args:
                    param_str = arg.arg
                    if arg.annotation:
                        param_str += f": {ast_to_source_simple(arg.annotation)}"
                    params.append(param_str)
                
                # 返回类型
                return_type = ""
                if method.returns:
                    return_type = f" -> {ast_to_source_simple(method.returns)}"
                
                # 装饰器
                decorators = ""
                if method.decorator_list:
                    decs = [ast_to_source_simple(d) for d in method.decorator_list]
                    decorators = f" `@{', @'.join(decs)}`"
                
                out.write(f"#### `{method.name}({', '.join(params)}){return_type}`{decorators}\n\n")
                out.write(f"*行号: {method.lineno}*\n\n")
                
                # 文档字符串
                method_doc = ast.get_docstring(method)
                if method_doc:
                    first_line = method_doc.split('\n')[0]
                    out.write(f"**说明**: {first_line}\n\n")
                
                out.write("---\n\n")

print(f"\n✅ 演示文件已生成!")
print(f"📄 输出路径: {output_file}")
print(f"📊 文件大小: {output_file.stat().st_size} 字节")
print(f"\n💡 这展示了 AiMdGenerator 如何提取 Python 文件的结构化元数据")
print(f"   让 AI 能更高效地理解代码结构，减少幻觉，提高推理准确性。")

