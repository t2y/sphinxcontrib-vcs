# -*- coding: utf-8 -*-
import unittest

from sphinx_testing import with_app


class TestSphinxcontribVcsErrors(unittest.TestCase):
    @with_app(srcdir='tests/docs/basic', write_docstring=True)
    def test_no_revision_error(self, app, status, warning):
        """
        .. git::
            :revision:
        """
        app.builder.build_all()
        message = 'revision string required as argument.'
        self.assertIn(message, warning.getvalue())
