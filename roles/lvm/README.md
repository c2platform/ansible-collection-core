# Ansible Role lvm

An Ansible Role that helps with managment of data disks / volumes using LVM.

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

The way this works is self explanatory. Configure a name of the volume group e.g. 

```yaml
lvm_vg: 'data'
```

A list of devices to use for this group

```yaml
lvm_vg_devices: ['sdb', 'sdc']
```

Add the Ansible role that uses the LVM role to `lvm_roles_supported`. And then configure how the volume should be created

```yaml
lvm_roles:
  bitbucket:
    size: '10g' 
    path: '{{ bitbucket_home if bitbucket_home is defined else "/opt/bitbucket" }}'
```

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }
```
