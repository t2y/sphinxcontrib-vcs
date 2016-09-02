# -*- coding: utf-8 -*-
import re
import sys

from setuptools import find_packages, setup


try:
    import pypandoc
    LONG_DESCRIPTION = '\n'.join([
        pypandoc.convert('README.md', 'rst'),
        pypandoc.convert('CHANGELOG.md', 'rst'),
    ])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

version_py = open('sphinxcontrib/vcs.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", version_py))


setup(
    name='sphinxcontrib-vcs',
    version=metadata['version'],
    description='Sphinx extension to show Changelog in version control system',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    url='https://github.com/t2y/...',
    license='BSD',
    author='Tetsuya Morimoto',
    author_email='tetsuya dot morimoto at gmail dot com',
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    namespace_packages=['sphinxcontrib'],
    include_package_data=True,
    install_requires=[
        'Sphinx',
        'GitPython',
    ],
    tests_require=['tox', 'pytest', 'pytest-pep8', 'pytest-flakes'],
)
