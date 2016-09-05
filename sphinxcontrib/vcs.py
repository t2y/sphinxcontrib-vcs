# -*- coding: utf-8 -*-
from datetime import datetime

import six
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

from .repository import GitRepository
from .repository import MercurialRepository
from .repository import find_repository_top

__version__ = '0.1.0'


OPTION_INCLUDE_DIFF = 'include_diff'
OPTION_NUMBER_OF_REVISIONS = 'number_of_revisions'
OPTION_WITH_REF_URL = 'with_ref_url'


class BaseDirective(Directive):

    TARGET_ID = 'vcs'

    option_spec = {
        OPTION_INCLUDE_DIFF: directives.flag,
        OPTION_NUMBER_OF_REVISIONS: directives.positive_int,
        OPTION_WITH_REF_URL: directives.flag,
    }

    def run(self):
        list_node = nodes.bullet_list()

        number_of_revisions = self.options.get(OPTION_NUMBER_OF_REVISIONS, 10)
        repo = self.get_repo(number_of_revisions)
        if repo is None:
            return

        targetnode = nodes.target('', '', ids=[self.TARGET_ID])
        for commit in repo.get_commits():
            item = self.get_changelog(repo, commit)
            list_node.append(item)
        return targetnode + [list_node]


class GitDirective(BaseDirective):

    def get_repo(self, number_of_revisions):
        env = self.state.document.settings.env
        return GitRepository(
            number_of_revisions, env.srcdir, search_parent_directories=True,
        )

    def get_changelog(self, repo, commit):
        item = nodes.list_item()
        item.append(nodes.strong(text=six.text_type(commit.message)))
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
            item.append(nodes.literal_block(text=six.text_type(diff)))

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
        item.append(nodes.strong(text=six.text_type(commit['summary'])))
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
            item.append(nodes.literal_block(text=six.text_type(diff)))

        return item


def setup(app):
    app.add_directive('git', GitDirective)
    app.add_directive('mercurial', MercurialDirective)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
