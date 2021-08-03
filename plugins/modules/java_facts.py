#!/usr/bin/python

from ansible.module_utils.basic import *


# Return folder name for JDK
# e.g. jdk8_222b10_oj9
def java_folder(version):
    return version.lower()


# Return Java home
# e.g. /usr/lib/jvm/jdk8_222b10_oj9
def java_home(version, java_version):
    if 'java_home' in java_version:
        return java_version['java_home']
    if 'folder' in java_version:
        folder = java_version['folder']
    else:
        folder = java_folder(version)
    return os.path.join(os.path.sep, '/usr/lib/jvm', folder)


def java_keystore(version, java_version):
    rel_path = 'lib/security/cacerts'
    if 'keystore' in java_version:
        rel_path = java_version['keystore']
    return java_path(java_home(version, java_version), rel_path)


def java_keytool(version, java_version):
    rel_path = 'bin/keytool'
    if 'keytool' in java_version:
        rel_path = java_version['keytool']
    return java_path(java_home(version, java_version), rel_path)


def java_path(java_home, rel_path):
    return os.path.join(os.path.sep, java_home, rel_path)


def java_facts(data):
    fcts = {}
    fcts['java'] = {}
    fcts['java_versions'] = {}
    fcts['java_install_archives'] = []
    fcts['java_install_packages'] = []
    for v in data['versions']:
        fcts['java_versions'][v] = {}
        fcts['java_versions'][v]['java_home'] = \
            java_home(v, data['versions'][v])
        fcts['java_versions'][v]['keytool'] = \
            java_keytool(v, data['versions'][v])
        fcts['java_versions'][v]['keystore'] = \
            java_keystore(v, data['versions'][v])
    install_versions = data['alternatives']
    install_versions.append(data['version'])
    for v in install_versions:
        if 'package' in data['versions'][v]:
            if data['versions'][v]['package']:
                fcts['java_install_packages'].append(v)
            else:
                fcts['java_install_archives'].append(v)
        else:
            fcts['java_install_archives'].append(v)
    default_version = fcts['java_versions'][data['version']]
    fcts['java_home'] = default_version['java_home']
    fcts['java_keytool'] = default_version['keytool']
    fcts['java_keystore'] = default_version['keystore']
    return False, fcts, "Java facts set"


def main():
    fields = {
        "versions": {"required": True, "type": "dict"},
        "version": {"required": True, "type": "str"},
        "alternatives": {"required": True, "type": "list"}
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts, tr = java_facts(module.params)
    module.exit_json(changed=False, ansible_facts=fcts, msg=tr)


if __name__ == '__main__':
    main()
