# ludobox setup.py

"""Setup script for Ludobox."""

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# Leave the following line to match the regexp [0-9]*\.[0-9]*\.[0-9]*
version = "0.0.1" # [major].[minor].[release]

# parse README
with open('README.md') as readme_file:
    long_description = readme_file.read()

# parse requirements
with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if 'git+https' not in x] # TODO - how to fix this?

setup(
      name = "ludobox",
      packages = find_packages(exclude=['tests']) ,
      version = version,
      description = "Ludobox",
      long_description = long_description,
      author = "DCALK",
      author_email = "info@ludobox.net",
      url = "http://ludobox.net",
      download_url = "http://github.com/ludobox/ludobox-ui",
      include_package_data=True,
      keywords = ["game", "public domain"],
      entry_points={
        'console_scripts': [
            'ludobox = ludocore:main'
        ],
    },
    license='GPL',
    classifiers = [
      "Programming Language :: Python",
      "Environment :: Other Environment",
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Developers",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=required
    )
