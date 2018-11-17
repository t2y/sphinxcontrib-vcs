import logging
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
