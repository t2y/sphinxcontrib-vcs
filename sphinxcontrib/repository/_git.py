import re

import gitdb
from git import Repo

from .utils import find_hosting_site, make_commit_url
from .utils import log


class GitRepository(Repo):

    EMPTY_TREE_SHA = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    URL_PATTERN = re.compile(
        r"""
        git@(?P<domain>.*?):(?P<account>.*?)/(?P<repository_name>.*?)\.git
        |https://github.com/(?P<account_>.*?)/(?P<repository_name_>.*?)\.git
        """, re.VERBOSE
    )

    def __init__(self, max_count, *args, **kwargs):
        super(GitRepository, self).__init__(*args, **kwargs)
        self.max_count = max_count
        self._hexsha = {}
        self._commits = []

    @property
    def branch_name(self):
        return self.head.ref.name

    def get_commit(self, revision):
        try:
            commit = self.commit(revision)
        except gitdb.exc.BadName as err:
            log.error(err)
            log.warn("Not found '%s' in git repository" % revision)
        else:
            self._commits.append(commit)
            self._hexsha[commit.hexsha] = 0
            if commit.parents:
                prev_commit = commit.parents[0]
                self._commits.append(prev_commit)
                self._hexsha[prev_commit.hexsha] = 1
            return commit

    def get_commits(self, revision=None, max_count=None, **kwargs):
        if revision is not None:
            self.get_commit(revision)
            self.max_count = 1
            return self._commits[:self.max_count]

        if len(self._commits) == 0 or max_count is not None:
            self._hexsha.clear()
            self._commits[:] = []
            if max_count is not None:
                self.max_count = max_count

            count = self.max_count + 1
            g = enumerate(self.iter_commits(max_count=count, **kwargs))
            for index, commit in g:
                self._hexsha[commit.hexsha] = index
                self._commits.append(commit)

        return self._commits[:self.max_count]

    def get_diff(self, revision):
        if len(self._commits) == 0:
            self.get_commits()

        index = self._hexsha[revision]
        target_commit = self._commits[index]
        if target_commit.parents:
            if len(self._commits) < index + 1:
                return ''
            prev_hexsha = self._commits[index + 1].hexsha
        else:
            prev_hexsha = self.EMPTY_TREE_SHA
        return self.git.diff(prev_hexsha, target_commit.hexsha)

    def get_commit_url(self, revision):
        if len(self._commits) == 0:
            self.get_commits()

        url = self.remotes.origin.url
        site = find_hosting_site(self.remotes.origin.url)
        return make_commit_url(self.URL_PATTERN, url, site, revision)


def get_repo(path):
    return GitRepository(path, search_parent_directories=True)


def test():
    r = get_repo('.')

    commits = r.get_commits(max_count=3)
    print(commits)

    for commit in commits:
        print(r.get_diff(commit.hexsha))

    commit_url = r.get_commit_url(commits[0].hexsha)
    print(commit_url)


if __name__ == '__main__':
    test()
