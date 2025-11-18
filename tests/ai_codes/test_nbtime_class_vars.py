"""测试 NbTime 类的类变量提取"""
import ast
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def ast_to_source_simple(node):
    """简单的 AST 转源码"""
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
        if hasattr(node, 's'):
            return repr(node.s)
        if hasattr(node, 'n'):
            return str(node.n)
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Call):
            func = ast_to_source_simple(node.func)
            return f"{func}(...)"
        return node.__class__.__name__
    except Exception:
        return "<parse_error>"


# 模拟 NbTime 类的部分定义
test_code = '''
import datetime

class NbTime:
    """时间转换，支持链式操作"""
    
    FORMATTER_DATETIME = "%Y-%m-%d %H:%M:%S %z"
    FORMATTER_DATETIME_WITH_ZONE = "%Y-%m-%d %H:%M:%S %z"
    FORMATTER_DATETIME_NO_ZONE = "%Y-%m-%d %H:%M:%S"
    FORMATTER_MILLISECOND = "%Y-%m-%d %H:%M:%S.%f %z"
    FORMATTER_DATE = "%Y-%m-%d"
    FORMATTER_TIME = "%H:%M:%S"
    FORMATTER_ISO = "%Y-%m-%dT%H:%M:%S%z"
    
    TIMEZONE_UTC = 'UTC'
    TIMEZONE_EASTERN_7 = 'UTC+7'
    TIMEZONE_EASTERN_8 = 'UTC+8'
    TIMEZONE_E8 = 'Etc/GMT-8'
    TIMEZONE_ASIA_SHANGHAI = 'Asia/Shanghai'
    
    TIMEZONE_TZ_EAST_8 = datetime.timezone(datetime.timedelta(hours=8), name='UTC+08:00')
    TIMEZONE_TZ_UTC = datetime.timezone(datetime.timedelta(hours=0), name='UTC+07:00')
    
    default_formatter: str = None
    default_time_zone: str = None
    
    @classmethod
    def set_default_formatter(cls, datetime_formatter: str):
        cls.default_formatter = datetime_formatter
'''

# 解析代码
tree = ast.parse(test_code)

print("=" * 80)
print("🔍 测试 NbTime 类的类变量提取")
print("=" * 80)

for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == "NbTime":
        print(f"\n📌 类名: {node.name}")
        print(f"📝 文档: {ast.get_docstring(node)}")
        print(f"📍 行号: {node.lineno}\n")
        
        class_vars = []
        
        # 遍历类成员
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # 带类型注解的类变量
                var_name = item.target.id
                var_type = ast_to_source_simple(item.annotation) if item.annotation else ""
                var_value = ast_to_source_simple(item.value) if item.value else ""
                
                # 限制长度
                if len(var_value) > 50:
                    var_value = var_value[:50] + "..."
                
                class_vars.append((var_name, var_type, var_value, item.lineno))
                
            elif isinstance(item, ast.Assign):
                # 无类型注解的类变量
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        var_type = ""
                        var_value = ast_to_source_simple(item.value) if item.value else ""
                        
                        # 限制长度
                        if len(var_value) > 50:
                            var_value = var_value[:50] + "..."
                        
                        class_vars.append((var_name, var_type, var_value, item.lineno))
        
        print(f"🎯 找到 {len(class_vars)} 个类变量:\n")
        
        # 按类别分组显示
        string_constants = []
        timezone_constants = []
        config_vars = []
        
        for name, type_anno, value, lineno in class_vars:
            if name.startswith("FORMATTER_"):
                string_constants.append((name, type_anno, value, lineno))
            elif name.startswith("TIMEZONE_"):
                timezone_constants.append((name, type_anno, value, lineno))
            else:
                config_vars.append((name, type_anno, value, lineno))
        
        if string_constants:
            print("📋 格式化字符串常量:")
            for name, type_anno, value, lineno in string_constants:
                type_str = f": {type_anno}" if type_anno else ""
                value_str = f" = {value}" if value else ""
                print(f"  • {name}{type_str}{value_str}")
            print()
        
        if timezone_constants:
            print("🌍 时区常量:")
            for name, type_anno, value, lineno in timezone_constants:
                type_str = f": {type_anno}" if type_anno else ""
                value_str = f" = {value}" if value else ""
                print(f"  • {name}{type_str}{value_str}")
            print()
        
        if config_vars:
            print("⚙️  配置变量:")
            for name, type_anno, value, lineno in config_vars:
                type_str = f": {type_anno}" if type_anno else ""
                value_str = f" = {value}" if value else ""
                print(f"  • {name}{type_str}{value_str}")
            print()
        
        # 生成 Markdown 格式
        print("=" * 80)
        print("📄 生成的 Markdown 元数据格式:")
        print("=" * 80)
        print()
        print("**Class Variables ({}):".format(len(class_vars)))
        for name, type_anno, value, lineno in class_vars[:10]:  # 只显示前10个
            type_str = f": {type_anno}" if type_anno else ""
            value_str = f" = {value}" if value else ""
            print(f"- `{name}{type_str}{value_str}`")
        if len(class_vars) > 10:
            print(f"- ... and {len(class_vars) - 10} more variables")

print("\n" + "=" * 80)
print("✅ 测试完成！类变量已成功提取")
print("=" * 80)

