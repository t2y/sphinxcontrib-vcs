# -*- coding: utf-8 -*-
import os
from datetime import datetime

import six
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx.util.osutil import copyfile

from .repository import GitRepository
from .repository import MercurialRepository
from .repository import find_repository_top

__version__ = '0.1.0'

CSS_CLASS = {
    'diff': ['contrib-vcs-diff', 'toggle-close'],
    'directive': ['contrib-vcs'],
    'message': ['contrib-vcs-message'],
}


def get_revision(argument):
    if argument is None:
        raise ValueError('revision string required as argument')
    return argument.strip()


def is_merge(commit):
    return commit.message[0:6] == 'Merged'


OPTION_INCLUDE_DIFF = 'include_diff'
OPTION_NUMBER_OF_REVISIONS = 'number_of_revisions'
OPTION_REVISION = 'revision'
OPTION_WITH_REF_URL = 'with_ref_url'
OPTION_ONLY_MERGE = 'only_merge'


class BaseDirective(Directive):

    option_spec = {
        OPTION_INCLUDE_DIFF: directives.flag,
        OPTION_NUMBER_OF_REVISIONS: directives.positive_int,
        OPTION_REVISION: get_revision,
        OPTION_WITH_REF_URL: directives.flag,
        OPTION_ONLY_MERGE: directives.flag,
    }

    def _make_message_node(self, message, sha):
        message, classes = six.text_type(message), []
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
            if OPTION_ONLY_MERGE in self.options and not(is_merge(commit)):
                continue
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
        item.append(nodes.inline(text=six.text_type(' by ')))
        item.append(nodes.emphasis(text=six.text_type(commit.author.name)))
        item.append(nodes.inline(text=six.text_type(' at ')))

        commit_date = datetime.fromtimestamp(commit.authored_date)
        item.append(nodes.emphasis(text=six.text_type(commit_date)))

        if OPTION_WITH_REF_URL in self.options:
            ref_url = repo.get_commit_url(commit.hexsha)
            ref = nodes.reference('', commit.hexsha, refuri=ref_url)
            item.append(nodes.paragraph('', '', ref))

        if OPTION_INCLUDE_DIFF in self.options:
            diff = repo.get_diff(commit.hexsha)
            item.append(self._make_diff_node(diff, commit.hexsha))

        return item


class MercurialDirective(BaseDirective):

    def get_repo(self, number_of_revisions):
        env = self.state.document.settings.env
        src_dir = find_repository_top(env.srcdir, '.hg')
        if src_dir is None:
            return None
        return MercurialRepository(number_of_revisions, src_dir)

    def get_changelog(self, repo, commit):
        item = nodes.list_item()

        item.append(self._make_message_node(commit['summary'], commit['sha']))
        item.append(nodes.inline(text=six.text_type(' by ')))
        item.append(nodes.emphasis(text=six.text_type(commit['user'])))
        item.append(nodes.inline(text=six.text_type(' at ')))
        item.append(nodes.emphasis(text=six.text_type(commit['date'])))

        if OPTION_WITH_REF_URL in self.options:
            ref_url = repo.get_commit_url(commit['sha'])
            ref = nodes.reference('', commit['sha'], refuri=ref_url)
            item.append(nodes.paragraph('', '', ref))

        if OPTION_INCLUDE_DIFF in self.options:
            diff = repo.get_diff(commit['revision'])
            item.append(self._make_diff_node(diff, commit['sha']))

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

    app.info('Copying vcs stylesheet/javascript... ', nonl=True)
    for file_ in CSS_FILES + JS_FILES:
        dest = os.path.join(app.builder.outdir, static_path, file_)
        source = os.path.join(current_path, static_path, file_)
        copyfile(source, dest)
    app.info('done')


def setup(app):
    app.add_directive('git', GitDirective)
    app.add_directive('mercurial', MercurialDirective)

    # copying css/js to _static
    app.connect('builder-inited', add_assets)
    app.connect('build-finished', copy_assets)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
