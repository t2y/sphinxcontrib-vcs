import os
from datetime import datetime

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.osutil import copyfile

from .repository import GitRepository

__version__ = '0.1.0'

logger = logging.getLogger(__name__)

CSS_CLASS = {
    'diff': ['contrib-vcs-diff', 'toggle-close'],
    'directive': ['contrib-vcs'],
    'message': ['contrib-vcs-message'],
}


def get_revision(argument):
    if argument is None:
        raise ValueError('revision string required as argument')
    return argument.strip()


OPTION_INCLUDE_DIFF = 'include_diff'
OPTION_NUMBER_OF_REVISIONS = 'number_of_revisions'
OPTION_REVISION = 'revision'
OPTION_WITH_REF_URL = 'with_ref_url'


class BaseDirective(Directive):

    option_spec = {
        OPTION_INCLUDE_DIFF: directives.flag,
        OPTION_NUMBER_OF_REVISIONS: directives.positive_int,
        OPTION_REVISION: get_revision,
        OPTION_WITH_REF_URL: directives.flag,
    }

    def _make_message_node(self, message, sha):
        message, classes = message, []
        if OPTION_INCLUDE_DIFF in self.options:
            classes = CSS_CLASS['message']
        return nodes.strong(ids=[sha], text=message, classes=classes)

    def _make_diff_node(self, diff, sha):
        classes = CSS_CLASS['diff']
        return nodes.literal_block(ids=[sha], text=diff, classes=classes)

    def run(self):
        list_node = nodes.bullet_list()

        number_of_revisions = self.options.get(OPTION_NUMBER_OF_REVISIONS, 10)
        repo = self.get_repo(number_of_revisions)
        if repo is None:
            return

        revision = self.options.get(OPTION_REVISION)
        for commit in repo.get_commits(revision=revision):
            item = self.get_changelog(repo, commit)
            list_node.append(item)
        return [list_node]


class GitDirective(BaseDirective):

    def get_repo(self, number_of_revisions):
        env = self.state.document.settings.env
        return GitRepository(
            number_of_revisions, env.srcdir, search_parent_directories=True,
        )

    def get_changelog(self, repo, commit):
        item = nodes.list_item()

        item.append(self._make_message_node(commit.message, commit.hexsha))
        item.append(nodes.inline(text=' by '))
        item.append(nodes.emphasis(text=commit.author.name))
        item.append(nodes.inline(text=' at '))

        commit_date = datetime.fromtimestamp(commit.authored_date)
        item.append(nodes.emphasis(text=commit_date))

        if OPTION_WITH_REF_URL in self.options:
            ref_url = repo.get_commit_url(commit.hexsha)
            ref = nodes.reference('', commit.hexsha, refuri=ref_url)
            item.append(nodes.paragraph('', '', ref))

        if OPTION_INCLUDE_DIFF in self.options:
            diff = repo.get_diff(commit.hexsha)
            item.append(self._make_diff_node(diff, commit.hexsha))

        return item


CSS_FILES = ['contrib-vcs.css']
JS_FILES = ['contrib-vcs.js']


def add_assets(app):
    for file_ in CSS_FILES:
        app.add_stylesheet(file_)
    for file_ in JS_FILES:
        app.add_javascript(file_)


def copy_assets(app, exception):
    if app.builder.name != 'html' or exception:
        return

    if len(app.builder.config.html_static_path) <= 0:
        return

    current_path = os.path.abspath(os.path.dirname(__file__))
    static_path = app.builder.config.html_static_path[0]

    logger.info('Copying vcs stylesheet/javascript... ', nonl=True)
    for file_ in CSS_FILES + JS_FILES:
        dest = os.path.join(app.builder.outdir, static_path, file_)
        source = os.path.join(current_path, static_path, file_)
        copyfile(source, dest)
    logger.info('done')


def setup(app):
    app.add_directive('git', GitDirective)

    # copying css/js to _static
    app.connect('builder-inited', add_assets)
    app.connect('build-finished', copy_assets)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
