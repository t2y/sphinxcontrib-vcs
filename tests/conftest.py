import os.path
import pathlib
import shutil

import pytest
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


def copy_dot_git(dst_dir):
    path = pathlib.Path(os.path.dirname(__file__))
    docs_path = path.joinpath(dst_dir)
    if not docs_path.exists():
        dot_git_path = path.parent.joinpath('.git')
        print(f'copy {dot_git_path} to {docs_path}')
        shutil.copytree(dot_git_path, docs_path)


copy_dot_git('docs/test-basic/.git')
copy_dot_git('docs/test-errors/.git')


@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'docs'
