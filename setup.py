# ludobox setup.py

"""Setup script for Ludobox."""

# Copyright (C) 2016  Pierre-Yves Martin for DCALK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# Leave the following line to match the regexp [0-9]*\.[0-9]*\.[0-9]*
version = "0.0.1"  # [major].[minor].[release]

# parse README
with open('README.md') as readme_file:
    long_description = readme_file.read()

# parse requirements
with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines()]

setup(
      name="ludobox",
      packages=find_packages(exclude=['tests']),
      version=version,
      description="Ludobox",
      long_description=long_description,
      author="DCALK",
      author_email="info@ludobox.net",
      url="http://ludobox.net",
      download_url="http://github.com/ludobox/ludobox-ui",
      include_package_data=True,
      keywords=["game", "public domain"],
      entry_points={
        'console_scripts': [
            'ludobox = ludobox.main:main'
        ],
      },
      license='GPL',
      classifiers=[
        "Programming Language :: Python",
        "Environment :: Other Environment",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      install_requires=required
      )
