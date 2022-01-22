#!/usr/bin/python

from ansible.module_utils.basic import *
import hashlib


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


def java_facts_trusts_export(data, fcts, trust):
    trust['exported'] = {}
    trust['exported']['status'] = False
    trust['exported']['sha256'] = None
    for exp in data['trusts']['exports']['results']:
        if trust['alias'] == exp['trust']['alias']:
            if 'source' in exp:
                f = open(exp['source'], "r")
                crt = f.read().rstrip()
                crt2 = crt.encode('utf-8')
                chksm = hashlib.sha256(crt2).hexdigest()
                trust['exported']['cert'] = crt
                trust['exported']['sha256'] = chksm
                trust['exported']['status'] = True
    return trust


def java_facts_trusts_download(data, fcts, trust):
    trust['downloaded'] = {}
    trust['downloaded']['status'] = False
    trust['downloaded']['sha256'] = None
    for dwnld in data['trusts']['downloads_uri']['results']:
        if trust['alias'] == dwnld['trust']['alias']:
            if 'BEGIN CERTIFICATE' in dwnld['stdout']:
                stdout2 = dwnld['stdout'].rstrip().encode('utf-8')
                chksm = hashlib.sha256(stdout2).hexdigest()
                trust['downloaded']['status'] = True
                trust['downloaded']['cert'] = dwnld['stdout']
                trust['downloaded']['sha256'] = chksm
    for dwnld in data['trusts']['downloads']['results']:
        if trust['alias'] == dwnld['trust']['alias']:
            crt = open(dwnld['dest'], "r").read().rstrip()
            chksm = hashlib.sha256(crt.encode('utf-8')).hexdigest()
            trust['downloaded']['status'] = True
            # trust['downloaded']['cert'] = crt
            trust['downloaded']['path'] = dwnld['dest']
            trust['downloaded']['sha256'] = chksm
    return trust


def trust_status(trust):
    ds = trust['downloaded']['status']
    es = trust['exported']['status']
    dsum = trust['downloaded']['sha256']
    esum = trust['exported']['sha256']
    new = False
    if ds and not es:
        new = True
        s = "import"
        m = "Certificate alias {} not in keystore".format(trust['alias'])
    if ds and es and dsum != esum:
        s = "update"
        m = 'Certificate alias {} in keystore is old'.format(trust['alias'])
    if ds and es and dsum == esum:
        s = "ok"
        m = 'Certificate alias {} is current'.format(trust['alias'])
    if not ds and not es:
        s = "fail"
        m = 'Certificate alias {} failed to download'.format(trust['alias'])
    return s, m, new


def java_trust_remove(trust):
    remove = False
    if 'state' in trust:
        if trust['state'] == 'absent':
            remove = True
    return remove


def java_facts_trusts(data, fcts):
    trusts = []
    trusts_config = data['versions'][data['version']]['trusts']
    trusts_config += data['java_trusts']
    for trust in trusts_config:
        if java_trust_remove(trust):
            s, m, new = 'remove', 'Certificate state is absent', False
        else:
            trust = java_facts_trusts_download(data, fcts, trust)
            trust = java_facts_trusts_export(data, fcts, trust)
            s, m, new = trust_status(trust)
        trust['status'] = s
        trust['message'] = m
        trust['new'] = new
        trusts.append(trust)
    fcts['java_versions'][data['version']]['trusts-status'] = \
        trusts
    return fcts


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
    if data['trusts'] is not None:
        fcts = java_facts_trusts(data, fcts)
    return False, fcts, "Java facts set"


def main():
    fields = {
        "versions": {"required": True, "type": "dict"},
        "version": {"required": True, "type": "str"},
        "alternatives": {"required": True, "type": "list"},
        "trusts": {"required": False, "type": "dict"},
        "java_trusts": {"required": False, "type": "list"}
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts, tr = java_facts(module.params)
    module.exit_json(changed=False, ansible_facts=fcts, msg=tr)


if __name__ == '__main__':
    main()
