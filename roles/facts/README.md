# Ansible Role Facts

Role to gather facts from hosts using [ansible.builtin.setup](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html). The results are returned as a fact `common_facts_hosts`. This role can be used directly but is more intended to be integrated / called from other roles using `include_role`. An example of this use is in [haproxy role](../haproxy).

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Dependencies](#dependencies)
- [Example](#example)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

Specify hosts to gather facts using `common_facts_gather_hosts`. A filter can be provided using `common_facts_filter`.

```yaml
common_facts_gather_hosts: "{{ groups['myapps'] }}"
common_facts_filter: 'ansible_eth1'
```

This role is used / integrated in [haproxy role](../haproxy) as follows

```yaml
- name: Gather facts
  include_role:
    name: c2platform.core.facts
    tasks_from: main
  vars:
    common_facts_role_name: haproxy
```

Now - in this haproxy role - facts of servers can be made available using vars

```yaml
haproxy_facts_gather_hosts: "{{ groups['myapps'] }}"
haproxy_facts_filter: 'ansible_eth1'
```

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

