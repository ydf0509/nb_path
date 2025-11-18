"""测试类变量提取功能"""
import ast
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def ast_to_source_simple(node):
    """简单的 AST 转源码，兼容 Python 3.7+"""
    if node is None:
        return ""
    try:
        if hasattr(ast, 'unparse'):
            return ast.unparse(node)
        # Python 3.7 简单处理
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            value = ast_to_source_simple(node.value)
            return f"{value}.{node.attr}"
        if hasattr(node, 's'):  # Python 3.7 Str
            return repr(node.s)
        if hasattr(node, 'n'):  # Python 3.7 Num
            return str(node.n)
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Call):
            func = ast_to_source_simple(node.func)
            args = [ast_to_source_simple(arg) for arg in node.args]
            return f"{func}({', '.join(args)})"
        return node.__class__.__name__
    except Exception:
        return "<parse_error>"


# 创建测试用的 Python 代码
test_code = '''
import datetime

class NbTime:
    """时间转换类"""
    
    # 类变量 - 字符串常量
    FORMATTER_DATETIME = "%Y-%m-%d %H:%M:%S %z"
    FORMATTER_DATE = "%Y-%m-%d"
    FORMATTER_TIME = "%H:%M:%S"
    
    # 类变量 - 字符串
    TIMEZONE_UTC = 'UTC'
    TIMEZONE_EASTERN_8 = 'UTC+8'
    
    # 类变量 - 复杂表达式
    TIMEZONE_TZ_EAST_8 = datetime.timezone(datetime.timedelta(hours=8), name='UTC+08:00')
    
    # 类变量 - 带类型注解
    default_formatter: str = None
    default_time_zone: str = None
    
    def __init__(self):
        pass
'''

# 解析代码
tree = ast.parse(test_code)

print("=" * 70)
print("测试类变量提取功能")
print("=" * 70)

for node in tree.body:
    if isinstance(node, ast.ClassDef):
        print(f"\n📌 类: {node.name}")
        print(f"文档: {ast.get_docstring(node)}")
        
        class_vars = []
        
        # 遍历类成员
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # 带类型注解的类变量
                var_name = item.target.id
                var_type = ast_to_source_simple(item.annotation) if item.annotation else ""
                var_value = ast_to_source_simple(item.value) if item.value else ""
                class_vars.append((var_name, var_type, var_value))
                
            elif isinstance(item, ast.Assign):
                # 无类型注解的类变量
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        var_type = ""
                        var_value = ast_to_source_simple(item.value) if item.value else ""
                        class_vars.append((var_name, var_type, var_value))
        
        print(f"\n类变量数量: {len(class_vars)}")
        print("\n类变量列表:")
        for name, type_anno, value in class_vars:
            type_str = f": {type_anno}" if type_anno else ""
            value_str = f" = {value}" if value else ""
            # 限制长度
            if len(value_str) > 52:
                value_str = value_str[:52] + "..."
            print(f"  • {name}{type_str}{value_str}")

print("\n" + "=" * 70)
print("✅ 测试完成！")
print("=" * 70)

