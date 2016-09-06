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


### Mercurial

    .. mercurial::
        :number_of_revisions: 20
        :with_ref_url:
        :include_diff:

For more information have a look at the documentation.

## Note

[Mercurial](https://www.mercurial-scm.org/) supports Python 2.x only.
So *sphinxcontrib-vcs* supports the *mercurial* directive on Python 2.7.

## Acknowledgments

*sphinxcontrib-vcs* is inspired from the [sphinx-git](https://github.com/OddBloke/sphinx-git).

