from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

version = {}
with open("thingsusers/version.py") as f:
    exec(f.read(), version)

with open("requirements.txt") as f:
    install_requires = f.readlines()

setup(
    name="thingsusers",
    version=version["__version__"],
    description="Service for managing users.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/e-k-m/thingsusers",
    author="Eric Matti",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="thingsusers",
    packages=find_packages(include=["thingsusers", "thingsusers.*"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["thingsusers-utils=thingsusers.cli:main"]
    },
)
