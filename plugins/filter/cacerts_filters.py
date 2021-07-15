"""ansible filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os


# Return groups ( and inventory_hostname keys )
def cacerts_certificate_group_keys(certificate, inventory_hostname, groups):
    keys = []
    for grp in groups:
        if grp in certificate:
            keys.append(grp)
    if inventory_hostname in certificate:
        keys.append(inventory_hostname)
    return keys


# Return all paths where certificates should be deployed
def cacerts_certificate_deploy_paths(certificate, inventory_hostname, groups):
    pths = []
    kys = cacerts_certificate_group_keys(
        certificate, inventory_hostname, groups)
    for ky in kys:
        pths += certificate[ky]
    return pths


# Return dirname of a certificate path for e.g stat.exists
def cacerts_dirname(paths):
    if 'crt' in paths[0]:
        return os.path.dirname(paths[0]['crt'])
    return os.path.dirname(paths[0]['pem'])


class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'cacerts_certificate_deploy_paths':
            cacerts_certificate_deploy_paths,
            'cacerts_certificate_group_keys':
            cacerts_certificate_group_keys,
            'cacerts_dirname':
            cacerts_dirname
        }
