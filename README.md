# sphinxcontrib-vcs

[![Build Status](https://travis-ci.org/t2y/sphinxcontrib-vcs.svg?branch=master)](https://travis-ci.org/t2y/sphinxcontrib-vcs/)

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

### 0.2.0 (2018-11-17)

* drop Python 2.7 support and mercurial feature
* support internal git repository such as GitHub Enterprise

### 0.1.0 (2016-09-06)

* first release
