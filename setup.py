#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

from setuptools import setup, find_packages
from smartoptim import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'flake8',
    'octopus-http',
    'pillow',
    'thumbor',
]

setup(
    name='smartoptim',
    version=__version__,
    description='Smart optimizer service for thumbor images.',
    long_description='''
Smart optimizer service for thumbor images.
''',
    keywords='dssim optimization performance images thumbor',
    author='Thumby',
    author_email='dev@thumby.io',
    url='https://github.com/thumby/smartoptim',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'deap',
        'numpy',
        'scikit-image',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'smartoptim=smartoptim.cli:main',
        ],
    },
)
