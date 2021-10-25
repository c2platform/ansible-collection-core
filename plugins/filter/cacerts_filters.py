"""ansible filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os
import hashlib


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
    if 'p12' in paths[0]:
        return os.path.dirname(paths[0]['p12'])
    return os.path.dirname(paths[0]['pem'])


# Return path to ownca directory
def cacerts2_ca_domain_dir(common_name, dir_domain):
    return "{}/{}".format(dir_domain, common_name)


# Return path to private key of the ownca
def cacerts2_ca_key_path(common_name, dir_domain):
    return "{}/{}/ca-{}.key".format(dir_domain, common_name, common_name)


# Return path to csr of the ownca
def cacerts2_ca_csr_path(common_name, dir_domain):
    return "{}/{}/ca-{}.csr".format(dir_domain, common_name, common_name)


# Return path to crt of the ownca
def cacerts2_ca_crt_path(common_name, dir_domain):
    return "{}/{}/ca-{}.crt".format(dir_domain, common_name, common_name)


# Return path to a key, crt file
def cacerts2_path(ca_common_name, ca_dir_domain, common_name,
                  ansible_hostname, ansible_group, ext):
    return "{}/{}/{}/{}/{}-{}.{}".format(ca_dir_domain, ca_common_name,
                                         ca_common_name, ansible_group,
                                         common_name, ansible_hostname, ext)


class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'cacerts_certificate_deploy_paths':
            cacerts_certificate_deploy_paths,
            'cacerts_certificate_group_keys':
            cacerts_certificate_group_keys,
            'cacerts_dirname': cacerts_dirname,
            'cacerts2_ca_domain_dir': cacerts2_ca_domain_dir,
            'cacerts2_ca_key_path': cacerts2_ca_key_path,
            'cacerts2_ca_csr_path': cacerts2_ca_csr_path,
            'cacerts2_ca_crt_path': cacerts2_ca_crt_path,
            'cacerts2_path': cacerts2_path
        }
