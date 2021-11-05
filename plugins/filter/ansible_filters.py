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


# Return index of host in group
def inventory_hostname_group_index(inventory_hostname, group_name, groups):
    if group_name in groups:
        if inventory_hostname in groups[group_name]:
            return groups[group_name].index(inventory_hostname) + 1
        else:
            return None
    else:
        return None


# Return number of hostnames in group
def group_length(group_name, groups):
    if group_name in groups:
        return len(groups[group_name])
    else:
        return None


# Return number of hostnames in group
def inventory_hostname_vars(inventory_hostname, vars, default_vars=[]):
    if inventory_hostname in vars:
        return vars[inventory_hostname]
    else:
        return default_vars


def update_list_attibute(lst, key, value):
    for lst_itm in lst:
        if key in lst_itm:
            lst_itm[key] = value
    return lst


class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'ansible_environment': ansible_environment,
            'ansible_cache_file': ansible_cache_file,
            'inventory_hostname_group_index': inventory_hostname_group_index,
            'group_length': group_length,
            'inventory_hostname_vars': inventory_hostname_vars,
            'update_list_attibute': update_list_attibute
        }
