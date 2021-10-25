#!/usr/bin/python

from ansible.module_utils.basic import *


def deploy_path(data, crt, ext):
    return "{}/{}-{}.{}".format(crt['deploy'][ext]['dir'], crt['common_name'],
                                data['hostname'], ext)


def src_path(data, crt, ext):
    return "{}/{}-{}.{}".format(crt['dir'], crt['common_name'],
                                data['hostname'], ext)


def ca_path(data, ext):
    return "{}/{}.{}".format(ca_dir(data),
                             data['ca_domain']['common_name'], ext)


def ca_dir(data):
    return "{}/{}".format(data['ca_dir'], data['ca_domain']['common_name'])


def certificates_key(data):
    return "{}_{}".format(data['role_name'], 'cacerts2_certificates')


def facts_ca(data, facts):
    facts['cacerts2_ca_domain'] = data['ca_domain']
    facts['cacerts2_ca_domain']['dir'] = ca_dir(data)
    facts['cacerts2_ca_domain']['key'] = ca_path(data, 'key')
    facts['cacerts2_ca_domain']['crt'] = ca_path(data, 'crt')
    facts['cacerts2_ca_domain']['csr'] = ca_path(data, 'csr')
    facts['cacerts2_ca_domain']['crl'] = ca_path(data, 'crl')
    return facts


def facts_certificates(data, facts):
    if data['role_name']:
        ck = certificates_key(data)
        facts[ck] = []
        for crt in data['certificates']:
            facts[ck].append(cert(data, crt))
    return facts


def facts(data):
    facts = {}
    facts = facts_certificates(data, facts)
    facts = facts_ca(data, facts)
    #if data['role_name']:
    #    facts['cacerts2_certificates'] = facts[certificates_key(data)]
    return (False, facts)


def cert(data, crt):
    crt['dir'] = "{}/{}".format(ca_dir(data), data['role_name'])
    for ext in crt['deploy']:
        dest = deploy_path(data, crt, ext)
        crt['deploy'][ext]['dest'] = dest
        crt['create'] = {}
    for ext in data['ca_domain']['create']:
        crt['create'][ext] = \
            src_path(data, crt, ext)
    return crt


def main():
    fields = {"certificates": {"required": False, "type": "list"},
              "ca_server": {"required": True, "type": "str"},
              "ca_dir": {"required": True, "type": "str"},
              "hostname": {"required": True, "type": "str"},
              "ca_dir": {"required": True, "type": "str"},
              "role_name": {"required": False, "type": "str"},
              "ca_domain": {"required": True, "type": "dict"}}
    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=True)
    has_changed, fcts = facts(module.params)
    module.exit_json(changed=has_changed, ansible_facts=fcts)


if __name__ == '__main__':
    main()
