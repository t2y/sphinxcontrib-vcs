# -*- coding: utf-8 -*-
import re
import sys

from setuptools import find_packages, setup


try:
    import pypandoc
    long_description = '\n'.join([
        pypandoc.convert('README.md', 'rst'),
        pypandoc.convert('CHANGELOG.md', 'rst'),
    ])
except (IOError, ImportError):
    long_description = ''

version_py = open('sphinxcontrib/vcs.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", version_py))
desc = 'Sphinx extension to show commit history in version control system'

requires = [
    'GitPython',
    'Sphinx',
    'six',
]

if sys.version_info < (3, 0):
    requires.append('Mercurial==3.8.2')


setup(
    name='sphinxcontrib-vcs',
    version=metadata['version'],
    description=desc,
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    url='https://github.com/t2y/sphinxcontrib-vcs',
    license='BSD',
    author='Tetsuya Morimoto',
    author_email='tetsuya dot morimoto at gmail dot com',
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    namespace_packages=['sphinxcontrib'],
    include_package_data=True,
    install_requires=requires,
    tests_require=[
        'flake8', 'mock', 'nose', 'reportlab', 'sphinx-testing',
    ],
)
