# -*- coding: utf-8 -*-
from datetime import datetime

import six
from docutils import nodes
from docutils.parsers.rst import Directive

from .repository import GitRepository

__version__ = '0.1.0'


class BaseDirective(Directive):

    TARGET_ID = 'vcs'

    option_spec = {
        'include_diff': bool,
        'number_of_revisions': int,
        'with_ref_url': bool,
    }

    def run(self):
        list_node = nodes.bullet_list()
        env = self.state.document.settings.env

        max_count = self.options.get('number_of_revisions', 10)
        repo = GitRepository(
            max_count, env.srcdir, search_parent_directories=True)

        targetnode = nodes.target('', '', ids=[self.TARGET_ID])
        for commit in repo.get_commits():
            item = self.get_changelog(repo, commit)
            list_node.append(item)
        return targetnode + [list_node]


class GitDirective(BaseDirective):

    def get_changelog(self, repo, commit):
        item = nodes.list_item()

        commit_date = datetime.fromtimestamp(commit.authored_date)

        item.append(nodes.strong(text=six.text_type(commit.message)))
        item.append(nodes.inline(text=six.text_type(' by ')))
        item.append(nodes.emphasis(text=six.text_type(commit.author.name)))
        item.append(nodes.inline(text=six.text_type(' at ')))
        item.append(nodes.emphasis(text=six.text_type(commit_date)))

        if self.options.get('with_ref_url') is not None:
            ref_url = repo.get_commit_url(commit.hexsha)
            ref = nodes.reference('', commit.hexsha, refuri=ref_url)
            item.append(nodes.paragraph('', '', ref))

        if self.options.get('include_diff') is not None:
            diff = repo.get_diff(commit.hexsha)
            item.append(nodes.literal_block(text=six.text_type(diff)))

        return item


def setup(app):
    app.add_directive('git', GitDirective)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
