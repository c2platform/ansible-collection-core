#!/usr/bin/python

from ansible.module_utils.basic import *


def site_result(site, trusted_sites_download):
    rs = trusted_sites_download['results']
    for r in rs:
        if r['site'] == site:
            return r
    msg = "Result for site {} not found in {}".format(site, rs)
    raise Exception(msg)


def set_java_trusted_sites_facts(data):
    facts = {}
    facts['java_trusted_sites'] = {}
    facts['java_trusted_sites']['certs'] = {}
    for site in data['trusted_sites']['certs']:
        facts['java_trusted_sites']['certs'][site] = {}
        r = site_result(site, data['trusted_sites_download'])
        facts['java_trusted_sites']['certs'][site]['cert'] = r['stdout']
    return (False, facts)


def main():
    fields = {"trusted_sites": {"required": True, "type": "dict"},
              "trusted_sites_download": {"required": True, "type": "dict"}}
    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts = set_java_trusted_sites_facts(module.params)
    module.exit_json(changed=has_changed, ansible_facts=fcts)


if __name__ == '__main__':
    main()
