"""java filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import os


# Return folder name for JDK
# e.g. jdk8_222b10_oj9
def java_folder(version):
    return version.lower()


# Return Java home
# e.g. /usr/lib/jvm/jdk8_222b10_oj9
def java_home(version):
    return os.path.join(os.path.sep, '/usr/lib/jvm', java_folder(version))


def java_keystore(version, jdk={}):
    rel_path = 'lib/security/cacerts'
    if 'keystore' in jdk:
        rel_path = jdk['keystore']
    return java_path(java_home(version), rel_path)


def java_keytool(version, jdk={}):
    rel_path = 'bin/keytool'
    if 'keytool' in jdk:
        rel_path = jdk['keytool']
    return java_path(java_home(version), rel_path)


def java_path(java_home, rel_path):
    return os.path.join(os.path.sep, java_home, rel_path)


def java_package_install(java_version):
    if 'package' in java_version:
        if java_version['package']:
            return True
    return False


class FilterModule(object):
    """java filters."""

    def filters(self):
        return {
            'java_folder': java_folder,
            'java_home': java_home,
            'java_keystore': java_keystore,
            'java_keytool': java_keytool,
            'java_package_install': java_package_install
        }
