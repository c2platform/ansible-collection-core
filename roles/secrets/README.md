# Ansible Role c2platform.core.secrets

Currently AWX lacks adequate support for Ansible vault secrets. See for example [Support vault encrypted secrets in the inventory source · Issue #223 · ansible/awx](https://github.com/ansible/awx/issues/223). This role is workaround for this issue.

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

There are many workarounds available. This role support one solution with a optional var `common_secrets_dirs`. You can for example set this to `"{{ inventory_dir }}/project/secret_vars/acceptance"` and then create a folder `secret_vars` in your repo next to the inventory file. 

```yaml
common_secrets_dirs:
  - "{{ inventory_dir }}/secret_vars" # ansible cli
  - "{{ inventory_dir }}/project/secret_vars/acceptance" # awx
```

Any file you then put in this directory will then be included when this role runs.

Note: when using AWX the `inventory_dir` is not what you might expect. It is not for example the same as the location in source control.

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
```
