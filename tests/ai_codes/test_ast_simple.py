"""简单测试 AST 元数据解析功能"""
import sys
import ast
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 直接测试 AST 解析
from nb_path.ai_md_generator import AiMdGenerator
from nb_path.nb_path_class import NbPath

# 创建测试实例
gen = AiMdGenerator("test.md")

# 测试解析 ai_md_generator.py 自身
test_file = NbPath(__file__).parent.parent.parent / "nb_path" / "ai_md_generator.py"

print(f"正在解析文件: {test_file}")
print(f"文件是否存在: {test_file.exists()}")

if test_file.exists():
    metadata = gen._parse_python_file_ast(test_file)
    
    print(f"\n✅ 解析成功!")
    print(f"📦 导入数量: {len(metadata.get('imports', []))}")
    print(f"🏛️  类数量: {len(metadata.get('classes', []))}")
    print(f"🔧 函数数量: {len(metadata.get('functions', []))}")
    
    # 显示类信息
    for cls in metadata.get('classes', []):
        print(f"\n类: {cls['name']}")
        print(f"  - 基类: {cls['bases']}")
        print(f"  - 公有方法数: {len([m for m in cls['methods'] if m['is_public']])}")
        print(f"  - 属性数: {len(cls['properties'])}")
        
        # 显示前3个公有方法
        public_methods = [m for m in cls['methods'] if m['is_public']][:3]
        for method in public_methods:
            params = gen._format_parameters(method['parameters'])
            print(f"  - {method['name']}({params})")
else:
    print("文件不存在!")

