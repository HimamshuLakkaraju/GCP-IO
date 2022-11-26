from setuptools import setup

setup(
    name="gcp-io",
    version="0.0.6",
    url="https://github.com/HimamshuLakkaraju/GCPIO",
    author="Himamshu Lakkaraju",
    author_email="hlakkaraju@hawk.iit.edu",
    py_modules=["gcpio"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests>=2.28.1", "torch>=1.13.0", "torchdata>=0.5.0"],
    extras_require={
        "dev": ["pytest>=3.7", "twine"],
    },
)
