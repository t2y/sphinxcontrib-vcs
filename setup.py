import re
from os import path
from setuptools import find_packages, setup

version_py = open('sphinxcontrib/vcs.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", version_py))
desc = 'Sphinx extension to show commit history in version control system'

cur_dir = path.abspath(path.dirname(__file__))
with open(path.join(cur_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name='sphinxcontrib-vcs',
    version=metadata['version'],
    description=desc,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
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
    author_email='tetsuya.morimoto@gmail.com',
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    namespace_packages=['sphinxcontrib'],
    include_package_data=True,
    install_requires=[
        'GitPython',
        'Sphinx',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-flake8',
        ],
        'lint': [
            'mypy',
            'docutils-stubs',
        ],
    },
)
