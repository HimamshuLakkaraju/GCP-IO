from setuptools import setup, find_packages

with open("README.md") as readme_file:
    long_description = readme_file.read()
setup(
    name="gcp-io",
    version="0.0.0.1",
    url="https://github.com/HimamshuLakkaraju/GCPIO",
    author="Himamshu Lakkaraju",
    author_email="hlakkaraju@hawk.iit.edu",
    description="A package to return files stored in Google drive and Google Cloud Storage as a torch.utils.Dataset that can be used with the torch dataloaders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["gcpio", "gcpio/gdrive", "gcpio/gcs", "gcpio/utils", "gcpio/settings"],
    package_dir={"": "src"},
    # packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.28.1",
        "torch>=1.13.0",
        "torchdata>=0.5.0",
        "torchvision",
        "google-auth-oauthlib",
        "google-api-python-client",
        "google-cloud-storage>=2.6.0",
        "pillow>=9.0.1",
    ],
    extras_require={
        "dev": ["pytest>=3.7", "twine", "pytest-cov>=4.0.0"],
    },
)
