#!/usr/bin/env python3
"""Setuptools configuration file"""

import ast
import io
import re
from setuptools import find_packages, setup

# get metadata from __init__
_DESCRIPTION_RE = re.compile(r'__version__\s+=\s+(.*)')
_VERSION_RE = re.compile(r'__version__\s+=\s+(.*)')
with open('dockerhub_stats/__init__.py', 'rb') as f:
    _INIT = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_VERSION_RE.search(_INIT).group(1)))
    DESCRIPTION = str(ast.literal_eval(_DESCRIPTION_RE.search(_INIT).group(1)))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open('README.md', encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name='dockerhub_stats',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version=VERSION,
    license='GPL v2',
    author='LM Networks Srl',
    author_email='info@lm-net.it',
    url='https://github.com/LMNetworks/dockerhub_stats',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        'influxdb',
        'prettytable',
    ],
    python_requires='>=3.6.0',
    entry_points={
        'console_scripts': ['dockerhub_stats = dockerhub_stats.cli:cli'],
    },
)
