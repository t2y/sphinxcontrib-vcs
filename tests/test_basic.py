import pytest


@pytest.mark.sphinx('html', testroot='basic/')
def test_build_html(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx('html', testroot='basic/')
def test_build_singlehtml(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='latex', srcdir='basic/')
def test_build_latex(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='epub', srcdir='basic/')
def test_build_epub(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx(buildername='json', srcdir='basic/')
def test_build_json(app, status, warning):
    app.builder.build_all()
