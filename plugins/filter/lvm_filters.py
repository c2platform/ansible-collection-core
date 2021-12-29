"""lvm filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


# Return physical volumes list based on device key
def lvm_pvs(devices):  # e.g. sdb, sdc
    pvs = []
    for d in devices:
        pvs.append("/dev/{}".format(d))
    return pvs


class FilterModule(object):
    """java filters."""

    def filters(self):
        return {
            'lvm_pvs': lvm_pvs
        }
