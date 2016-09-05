# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re

try:
    from mercurial import ui, hg, commands
    from mercurial.error import RepoLookupError
except ImportError:
    pass

from .utils import find_hosting_site, find_repository_top
from .utils import log
from .utils import make_commit_url


class MercurialRepository(object):

    LOG_PATTERN = re.compile(r'(?P<type>\w+):[\t\s]+(?P<value>.*)')
    URL_PATTERN = re.compile(
        r'ssh://hg@bitbucket.org/(?P<account>.*?)/(?P<repository_name>.*?)$'
    )

    def __init__(self, limit, path):
        self.limit = limit
        self.ui = ui.ui()
        self.raw = hg.repository(self.ui, path=path)
        self._changeset = {}
        self._commits = []
        self.set_default_path()

    def set_default_path(self):
        self.ui.pushbuffer()
        commands.paths(self.ui, self.raw, search='default')
        lines = self.ui.popbuffer().decode('utf-8').split('\n')
        if len(lines) > 0:
            _path = lines[0]
            if _path.split('/')[-1] == '...':
                # FIXME: how to get repository name
                repository_name = self.raw.root.split('/')[-1]
                _path = _path.replace('...', repository_name)
            self.default_path = _path
        else:
            self.default_path = ''

    def read_changeset_lines(self, lines):
        is_found, commit = False, {}
        for index, line in enumerate(lines, 1):
            m = re.match(self.LOG_PATTERN, line)
            if m is not None:
                log_info = m.groupdict()
                type_ = log_info.get('type', None)
                value = log_info.get('value', None)
                if type_ is not None:
                    if type_ == 'changeset':
                        if is_found:
                            index -= 1
                            break
                        is_found = True
                        revision, sha = value.split(':')
                        commit['revision'] = int(revision)
                        commit['sha'] = sha
                    commit[type_] = value
        return index, commit

    def get_commit(self, revision):
        self.ui.pushbuffer()
        try:
            commands.log(self.ui, self.raw, rev=[str(revision)])
        except RepoLookupError as err:
            log.error(err)
            log.warn("Not found '%s' in mercurial repository" % revision)
        else:
            lines = self.ui.popbuffer().decode('utf-8').split('\n')
            index, commit = self.read_changeset_lines(lines)
            changeset = commit.get('changeset')
            if changeset is not None:
                self._commits.append(commit)
                self._changeset[changeset] = commit
            return commit

    def get_commits(self, revision=None, limit=None):
        if revision is not None:
            self.get_commit(revision)
            self.limit = 1
            return self._commits[:self.limit]

        if len(self._commits) == 0 or limit is not None:
            self._commits[:] = []
            if limit is not None:
                self.limit = limit

            self.ui.pushbuffer()
            commands.log(self.ui, self.raw, limit=self.limit + 1)
            lines = self.ui.popbuffer().decode('utf-8').split('\n')

            while len(lines) != 0:
                index, commit = self.read_changeset_lines(lines)
                changeset = commit.get('changeset')
                if changeset is not None:
                    self._commits.append(commit)
                    self._changeset[changeset] = commit
                lines = lines[index:]

        return self._commits[:self.limit]

    def get_commit_url(self, revision):
        site = find_hosting_site(self.default_path)
        if site is None:
            return ''

        return make_commit_url(
            self.URL_PATTERN, self.default_path, site, revision)

    def get_diff(self, revision):
        self.ui.pushbuffer()
        revisions = [revision - 1, revision]
        commands.diff(self.ui, self.raw, rev=revisions)
        diff_text = self.ui.popbuffer()
        try:
            diff = diff_text.decode('utf-8')
        except UnicodeDecodeError as err:
            log.error(err)
            msg = 'Supports utf-8 encoding only, '\
                  'so ignore diff text from revisions: %s' % (revisions)
            log.warn(msg)
            diff = ''
        return diff


def get_repo(number_of_revisions, path):
    repository_path = find_repository_top(path, '.hg')
    if repository_path is None:
        return None
    return MercurialRepository(number_of_revisions, repository_path)


def test():
    r = get_repo(10, '.')

    commits = r.get_commits(max_count=3)
    print(commits)

    for commit in commits:
        print(r.get_diff(commit['revision']))

    commit_url = r.get_commit_url(commits[0]['sha'])
    print(commit_url)


if __name__ == '__main__':
    test()
