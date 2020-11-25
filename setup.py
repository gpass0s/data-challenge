#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 07:44 BRT 2020
author: guilherme passos | twitter: @gpass0s
"""
from setuptools import find_packages
from setuptools import setup


setup(
    name="desafios",
    version="0.0.0",
    description="A hiring process challenge",
    author="@gpass0s",
    url="https://github.com/gPass0s/data-challenge",
    packages=find_packages(exclude=["tests*"]),
)
