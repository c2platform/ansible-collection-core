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


def java_facts_trusted_sites_export(data, fcts, site):
    site['exported'] = {}
    site['exported']['status'] = False
    site['exported']['cert'] = None
    site['exported']['sha256'] = None
    for exp in data['trusted_sites']['exports']['results']:
        if site['alias'] == exp['site']['alias']:
            if 'source' in exp:
                f = open(exp['source'], "r")
                crt = f.read().rstrip()
                crt2 = crt.encode('utf-8')
                chksm = hashlib.sha256(crt2).hexdigest()
                site['exported']['cert'] = crt
                site['exported']['sha256'] = chksm
                site['exported']['status'] = True
    return site


def java_facts_trusted_sites_download(data, fcts, site):
    site['downloaded'] = {}
    site['downloaded']['status'] = False
    for dwnld in data['trusted_sites']['downloads']['results']:
        if site['alias'] == dwnld['site']['alias']:
            if 'BEGIN CERTIFICATE' in dwnld['stdout']:
                stdout2 = dwnld['stdout'].rstrip().encode('utf-8')
                chksm = hashlib.sha256(stdout2).hexdigest()
                site['downloaded']['status'] = True
                site['downloaded']['cert'] = dwnld['stdout']
                site['downloaded']['sha256'] = chksm
    return site


def site_status(site):
    ds = site['downloaded']['status']
    es = site['exported']['status']
    dsum = site['downloaded']['sha256']
    esum = site['exported']['sha256']
    new = False
    if ds and not es:
        new = True
        s = "import"
        m = "Certificate alias {} not in keystore".format(site['alias'])
    if ds and es and dsum != esum:
        s = "update"
        m = 'Certificate alias {} in keystore is old'.format(site['alias'])
    if ds and es and dsum == esum:
        s = "ok"
        m = 'Certificate alias {} is current'.format(site['alias'])
    return s, m, new


def java_facts_trusted_sites(data, fcts):
    trusted_sites = []
    for site in data['versions'][data['version']]['trusted-sites']:
        site = java_facts_trusted_sites_download(data, fcts, site)
        site = java_facts_trusted_sites_export(data, fcts, site)
        s, m, new = site_status(site)
        site['status'] = s
        site['message'] = m
        site['new'] = new
        trusted_sites.append(site)
    fcts['java_versions'][data['version']]['trusted-sites-status'] = \
        trusted_sites
    return fcts


def java_facts(data):
    fcts = {}
    fcts['java_versions'] = data['versions']
    if data['trusted_sites'] is not None:
        fcts = java_facts_trusted_sites(data, fcts)
    return False, fcts, "Java trusted sites facts set"


def main():
    fields = {
        "versions": {"required": True, "type": "dict"},
        "version": {"required": True, "type": "str"},
        "trusted_sites": {"required": False, "type": "dict"}
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts, tr = java_facts(module.params)
    module.exit_json(changed=False, ansible_facts=fcts, msg=tr)


if __name__ == '__main__':
    main()
