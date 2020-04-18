import pytest


@pytest.mark.sphinx('html', testroot='errors/')
def test_errors_build_html(app, status, warning):
    app.builder.build_all()
    message = 'revision string required as argument.'
    assert message in warning.getvalue()
