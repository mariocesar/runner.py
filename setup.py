#!/usr/bin/env python3
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    sys.exit('Python 3.6 is the minimum required version')

description, long_description = (
    open('README.rst', 'rt').read().split('\n\n', 1))


setup(
    name='runner.py',
    version='0.5',
    url='https://github.com/mariocesar/runner.py',
    author='Mario César Señoranis Ayala',
    author_email='mariocesar.c50@gmail.com',
    description=description,
    long_description=f'\n{long_description}',
    long_description_content_type='text/x-rst',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    keywords='runner process asyncio',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
