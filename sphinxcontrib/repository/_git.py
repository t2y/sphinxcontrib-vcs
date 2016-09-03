# -*- coding: utf-8 -*-
import re

from git import Repo


HOSTING_SERVICE = {
    'github': {
        'site': 'https://github.com',
        'commit_template': '{site}/{user}/{repository}/commit/{sha}',
    },
    'bitbucket': {
        'site': 'https://bitbucket.org',
        'commit_template': '{site}/{user}/{repository}/commits/{sha}',
    },
}

HOSTING_INFO_PATTERN = re.compile(
    r'git@.*?:(?P<account>.*?)/(?P<repository_name>.*?)\.git',
)


class GitRepository(Repo):

    EMPTY_TREE_SHA = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

    def __init__(self, max_count, *args, **kwargs):
        super(GitRepository, self).__init__(*args, **kwargs)
        self.max_count = max_count
        self._hexsha = {}
        self._commits = []

    @property
    def branch_name(self):
        return self.head.ref.name

    def get_commits(self, max_count=None, **kwargs):
        if len(self._commits) == 0 or max_count is not None:
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
            prev_hexsha = self._commits[index + 1].hexsha
        else:
            prev_hexsha = self.EMPTY_TREE_SHA
        return self.git.diff(prev_hexsha, target_commit.hexsha)

    def make_commit_url(self, site, revision):
        m = re.match(HOSTING_INFO_PATTERN, self.remotes.origin.url)
        if m is None:
            return ''

        info = m.groupdict()
        return site['commit_template'].format(
            site=site['site'],
            user=info['account'],
            repository=info['repository_name'],
            sha=revision,
        )

    def get_commit_url(self, revision):
        if len(self._commits) == 0:
            self.get_commits()

        site = find_hosting_site(self.remotes.origin.url)
        if site is None:
            return ''

        return self.make_commit_url(site, revision)


def get_repo(path):
    return GitRepository(path, search_parent_directories=True)


def find_hosting_site(url):
    if url.find('github.com') > 0:
        return HOSTING_SERVICE['github']
    elif url.find('bitbucket.org') > 0:
        return HOSTING_SERVICE['bitbucket']
    return None


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
