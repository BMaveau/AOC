#!/usr/bin/env python

from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages


setup(
    name="AdventTool",
    version="0.1.0",
    description="A toolbox for helping solving the AoC puzzles",
    author="Benjamin Maveau",
    author_email="benjamin.maveau@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26",
    ],
)
