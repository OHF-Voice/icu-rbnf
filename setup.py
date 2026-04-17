#!/usr/bin/env python3
"""Setup script for icu_rbnf - uses setuptools with C extension."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Try to find ICU using pkg-config
def get_icu_cflags():
    """Get ICU compiler flags from pkg-config."""
    try:
        result = subprocess.run(
            ["pkg-config", "--cflags", "icu-uc", "icu-i18n"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split()
    except subprocess.CalledProcessError:
        return []

def get_icu_ldflags():
    """Get ICU linker flags from pkg-config."""
    try:
        result = subprocess.run(
            ["pkg-config", "--libs", "icu-uc", "icu-i18n"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split()
    except subprocess.CalledProcessError:
        return []

class BuildExtWithICU(build_ext):
    """Custom build_ext that ensures ICU is found."""
    
    def build_extension(self, ext):
        # Add ICU flags if not already present
        if not ext.extra_compile_args:
            ext.extra_compile_args = get_icu_cflags()
        if not ext.extra_link_args:
            ext.extra_link_args = get_icu_ldflags()
        
        super().build_extension(ext)


# Define the extension module - use C++ for ICU
ext_modules = [
    Extension(
        "icu_rbnf._icu",
        sources=["src/icu_rbnf.cpp"],
        define_macros=[("PY_SSIZE_T_CLEAN", "1")],
        include_dirs=[],
        py_limited_api=True,
        extra_compile_args=get_icu_cflags(),
        extra_link_args=get_icu_ldflags(),
    )
]

# Get long description from README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="icu_rbnf",
    version="0.1.0",
    description="Spell out numbers into words using ICU RBNF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Home Assistant Authors",
    author_email="hello@home-assistant.io",
    url="https://github.com/OHF-voice/icu-rbnf",
    project_urls={
        "Homepage": "https://github.com/OHF-voice/icu-rbnf",
        "Issues": "https://github.com/OHF-voice/icu-rbnf/issues",
    },
    packages=["icu_rbnf"],
    package_dir={"icu_rbnf": "icu_rbnf"},
    package_data={"icu_rbnf": ["py.typed"]},
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtWithICU},
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: C",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "mypy",
            "pylint",
            "pytest",
            "build",
        ],
    },
)
