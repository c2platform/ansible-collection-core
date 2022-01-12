#!/usr/bin/python

from ansible.module_utils.basic import *


def rest_facts(data):
    fcts = {}
    fcts['rest_responses'] = data['rest_responses']
    fcts['rest_responses'][data['rest_resource_group_name']] = data['results']
    return False, fcts, "REST facts set"


def main():
    fields = {
        "rest_responses": {"required": True, "type": "dict"},
        "rest_resource_group_name": {"required": True, "type": "str"},
        "results": {"required": True, "type": "list"}
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts, tr = rest_facts(module.params)
    module.exit_json(changed=False, ansible_facts=fcts, msg=tr)


if __name__ == '__main__':
    main()
