# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import os
import re

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

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.INFO,
)
log = logging.getLogger('sphinxcontrib-vcs')


def find_hosting_site(url):
    if url.find('github.com') > 0:
        return HOSTING_SERVICE['github']
    elif url.find('bitbucket.org') > 0:
        return HOSTING_SERVICE['bitbucket']
    return None


def find_repository_top(current_dir, conf_dir):
    repository_dir = os.path.abspath(os.path.join(current_dir, conf_dir))
    if repository_dir == os.path.abspath(os.sep):
        return None

    if os.path.exists(repository_dir) and os.path.isdir(repository_dir):
        return os.path.abspath(current_dir)
    else:
        parent_dir = os.path.join(current_dir, os.path.pardir)
        return find_repository_top(parent_dir, conf_dir)


def make_commit_url(pattern, path, site, revision):
    m = re.match(pattern, path)
    if m is None:
        return ''

    info = m.groupdict()
    account = info.get('account') or info.get('account_')
    repository = info.get('repository_name') or info.get('repository_name_')
    return site['commit_template'].format(
        site=site['site'],
        user=account,
        repository=repository,
        sha=revision,
    )
