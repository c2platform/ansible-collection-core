"""files filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError


def file_exists(item, no_update_files):
    for itm in no_update_files['results']:
        if itm['item']['dest'] == item['dest']:
            return itm['stat']['exists']
    return False


def file_exists_and_update_false(item, no_update_files):
    exists_and_false = False
    if 'update' in item:
        if not item['update']:
            if file_exists(item, no_update_files):
                exists_and_false = True
    return exists_and_false


class FilterModule(object):
    """java filters."""

    def filters(self):
        return {
            'file_exists_and_update_false': file_exists_and_update_false,
        }
