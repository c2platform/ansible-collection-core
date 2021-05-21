
# Ansible Role Common

<!-- MarkdownTOC levels="2,3,4" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
    - [Optional Ansible User](#optional-ansible-user)
    - [Optional AWX Ansible Vault](#optional-awx-ansible-vault)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

### Optional Ansible User

Create an Ansible user. Default is disabled because it is mostly only used in development environments.

```yaml
common_ansible_user: ansible
common_ansible_user_password: $1$tBPdczeQ$Kca8G0jWZ4fyGsgCtZD5F/ # supersecure
common_ansible_user_create: false
common_ansible_user_expires: -1
```

Note: `common_ansible_user_password` is the password shadow hash created with for example `openssl passwd -1 "mypassword"`. This done to prevent continuous changes being reported to the account if we use Ansible to do this for using for example `password_hash("sha512")` filter. 

### Optional AWX Ansible Vault

Currently AWX lacks adequate support for Ansible vault secrets. See for example [Support vault encrypted secrets in the inventory source · Issue #223 · ansible/awx](https://github.com/ansible/awx/issues/223).

There are many workarounds available. This role support one solution with a optional var `common_secrets_dir`. You can for example set this to `"{{ inventory_dir }}/secret_vars"` and then create a folder `secret_vars` in your repo next to the inventory file. 

```yaml
common_secrets_dir: "{{ inventory_dir }}/project/inventory/test/secret_vars"
```

Any file you then put in this directory will then be included when this role runs.

Note: when using AWX the `inventory_dir` is not what you might expect. It is not for example the same as the location in source control.

TODO common_secrets_no_log

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }
```