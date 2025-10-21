import setuptools

# Read the long description from the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nb-path",  # Package name, must be unique on PyPI
    version="2.3",  # Version number, needs to be incremented for each new release
    author="ydf0509",  # Your name or nickname
    author_email="your_email@example.com",  # Your contact email
    description="A Python path library that gives filesystem operations superpowers",  # Short description
    long_description=long_description,  # Detailed description, from README
    long_description_content_type="text/markdown",  # Description file type
    url="https://github.com/ydf0509/nb_path",  # Project's GitHub URL
    packages=setuptools.find_packages(),  # Automatically find all packages in the project
    
    # Define optional dependencies
    # Users can install all extra features with: pip install nb-path[all]
    extras_require={
        'download': ['requests', 'tqdm'],  # For the download_from_url() method
        'lock': ['filelock'],              # For the lock() method
        'all': ['requests', 'tqdm', 'filelock'],
    },
    
    # Classify the package to help it be found on PyPI
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
    
    # Specify the required Python version for the project
    python_requires='>=3.6',
)