
# Ansible Role Common

<!-- MarkdownTOC levels="2,3,4" autolink="true" -->

- [Requirements](#requirements)
- [Git repositories](#git-repositories)
- [Role Variables](#role-variables)
  - [Optional Ansible User](#optional-ansible-user)
  - [common_regex_files](#common_regex_files)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Git repositories

Use `common_git_repos` to define Git repositories to checkout and where using [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html).

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

### common_regex_files

Use dict `common_regex_files` to change arbitrary files and trigger handlers using optional `notify` attribute. 

```yaml
common_regex_files:
  sshd_config:
    path: /etc/ssh/sshd_config
    regex:
      - search: ^.*ClientAliveInterval.*$
        replace: "#ClientAliveInterval 0"
      - search: ^.*ClientAliveCountMax.*$
        replace: "#ClientAliveCountMax 3"
    notify: restart haproxy
  ca_certificates:
    path: /etc/ca-certificates.conf
    regex:
      - search: ^.*mozilla/DST_Root_CA_X3.crt$
        replace: "!mozilla/DST_Root_CA_X3.crt"
    notify: Update CA certificates
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