"""ansible filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import os
import hashlib


# Return a logical name based on inventory file
# e.g. development (from /somepath/development.ini)
def ansible_environment(inv_file):
    bn = os.path.basename(inv_file)
    return bn.split('.', 1)[0]


# Return path of cache file
def ansible_cache_file(url):
    bn = os.basename(url)
    ename = os.path.splitext(bn)[1]
    bn2 = os.path.splitext(bn)[0]
    url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()
    return os.path.join(os.path.sep, '/var/tmp',
                        bn2 + '-' + url_hash + '.' + ename)


class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'ansible_environment': ansible_environment,
            'ansible_cache_file': ansible_cache_file
        }
