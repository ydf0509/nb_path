import setuptools

# 从 README.zh.md 文件中读取长描述
with open("README.zh.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nb-path",  # 包名，在 PyPI 上必须是唯一的
    version="1.9",  # 版本号，每次发布新版本时需要增加
    author="ydf0509",  # 您的名字或昵称
    author_email="your_email@example.com",  # 您的联系邮箱
    description="一个赋予文件系统操作超能力的 Python 路径库",  # 简短描述
    long_description=long_description,  # 详细描述，来自 README
    long_description_content_type="text/markdown",  # 描述文件类型
    url="https://github.com/ydf0509/nb_path",  # 项目的 GitHub URL
    packages=setuptools.find_packages(),  # 自动查找项目中的所有包
    
    # 定义可选依赖项
    # 用户可以通过 pip install nb-path[all] 来安装所有额外功能
    extras_require={
        'download': ['requests', 'tqdm'],  # `download_from_url` 方法需要这些依赖
        'all': ['requests', 'tqdm'],
    },
    
    # 对包进行分类，有助于在 PyPI 上被搜索到
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: 3.10",
        # "Programming Language :: Python :: 3.11",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    
    # 指定项目要求的 Python 版本
    python_requires='>=3.6',
)