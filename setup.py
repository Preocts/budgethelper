#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Basic setup file """
from setuptools import find_packages
from setuptools import setup


setup(
    name="budget_helper_preocts",
    version="0.0.1",
    license="MIT License",
    description="Something to help me keep track of details",
    author="Preocts",
    author_email="preocts@preocts.com",
    url="https://github.com/Preocts/budgethelper",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={"console_scripts": ["phstart=modulename.poe:func"]},
    include_package_data=False,
)
