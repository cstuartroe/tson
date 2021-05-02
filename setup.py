import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tson",
    version="0.0.0",
    description="TS : JS :: TSON : JSON",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cstuartroe/tson",
    author="Conor Stuart Roe",
    author_email="conorstuartroe@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["tson"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)