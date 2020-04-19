# sphinxcontrib-vcs

![](https://github.com/kazamori/github-api-tools/workflows/Python%20package/badge.svg)

*sphinxcontrib-vcs* provides showing commit history in version control system.

## Setup

    $ pip install sphinxcontrib-vcs

## Usage

Add *'sphinxcontrib.vcs'* as extensions into conf.py.

    $ vi conf.py
    extensions = ['sphinxcontrib.vcs']

Then, repository directives are available as follows.

### Git

    .. git::
        :number_of_revisions: 20
        :with_ref_url:
        :include_diff:

For more information have a look at [the documentation](https://sphinxcontrib-vcs.readthedocs.io/).

## Acknowledgments

*sphinxcontrib-vcs* is inspired from the [sphinx-git](https://github.com/OddBloke/sphinx-git).

## ChangeLog

### 0.3.0 (2020-04-19)

* drop Python 3.5 support
* add type annotation and modules reference

### 0.2.2 (2019-11-06)

* fix packaging issue: cannot import sphinxcontrib.repository

### 0.2.1 (2019-08-04)

* fix wrong Docutils DTD list_item node thanks to amedama41

### 0.2.0 (2018-11-17)

* drop Python 2.7 support and mercurial feature
* support internal git repository such as GitHub Enterprise

### 0.1.0 (2016-09-06)

* first release
