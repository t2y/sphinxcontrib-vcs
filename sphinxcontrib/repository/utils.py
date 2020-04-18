import logging
import re

# type check
from typing import Dict
from typing import Optional
from typing import Pattern


HOSTING_SERVICE: Dict[str, Dict[str, Optional[str]]] = {
    'github': {
        'site': 'https://github.com',
        'commit_template': '{site}/{user}/{repository}/commit/{sha}',
    },
    'bitbucket': {
        'site': 'https://bitbucket.org',
        'commit_template': '{site}/{user}/{repository}/commits/{sha}',
    },
    'internal': {
        'site': None,
        'commit_template': '{site}/{user}/{repository}/commit/{sha}',
    },
}

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.INFO,
)
log = logging.getLogger('sphinxcontrib-vcs')


def find_hosting_site(url: str) -> Dict[str, Optional[str]]:
    if url.find('github.com') > 0:
        return HOSTING_SERVICE['github']
    elif url.find('bitbucket.org') > 0:
        return HOSTING_SERVICE['bitbucket']
    return HOSTING_SERVICE['internal']


def make_commit_url(pattern: Pattern[str], path: str,
                    site: Dict[str, Optional[str]], revision: str) -> str:
    m = re.match(pattern, path)
    if m is None:
        return ''

    info = m.groupdict()

    _site = site['site']
    if _site is None:
        # suppose GitHub Enterprise
        _site = 'https://%s' % info.get('domain')

    account = info.get('account') or info.get('account_')
    repository = info.get('repository_name') or info.get('repository_name_')
    commit_template = site['commit_template']
    assert commit_template is not None
    return commit_template.format(
        site=_site,
        user=account,
        repository=repository,
        sha=revision,
    )
