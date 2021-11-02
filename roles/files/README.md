# Ansible Role Files

Manage files, directories and ACL. This role is included in the [common](./../common) role.

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

Three dictionaries ( not lists ) `common_files`, `common_directories` and `common_acl`. Dictionaries are used to group resources you are creating. In example below `external-stub` is just a group. This group defines a list of directories to create.

```yaml
common_directories:
  external-stub:
    - group: "{{ tomcat_group }}" # users-bkwi
      owner: "{{ tomcat_user }}"
      path: "{{ tomcat_home_version  }}/stub"
    - group: "{{ tomcat_group }}"
      owner: "{{ tomcat_user }}"
      path: "{{ tomcat_home_version  }}/stub/responses"
      acl_entity: "{{ tomcat_user }}"
      acl_etype: user
      acl_permission: rwx
      acl_default: yes
      acl_state: present

common_acl:
  external-stub:
    - path: "{{ tomcat_home_version  }}/stub/responses"
      entity: "{{ tomcat_user }}"
      etype: user
      permission: rwx
      default: yes
      state: present
```

These dictionaries can be used as-is but they can also be included in other roles for example a **Tomcat** role as follows:

```yaml
- name: Files
  include_role:
    name: c2platform.core.files
    tasks_from: main
  vars:
    role_name: tomcat # role_name
    common_files: "{{ tomcat_files }}"
    common_directories: "{{ tomcat_directories }}"
    common_acl: "{{ tomcat_acl }}"
```

This gives more control over when those files, directories, acl are created. Example below also demonstrates how we introduce our own local variables with prefixed with `tomcat` so that we can configure:

```yaml
tomcat_directories:
  external-stub:
    - group: "{{ tomcat_group }}" # users-bkwi
      owner: "{{ tomcat_user }}"
      path: "{{ tomcat_home_version  }}/stub"
    - group: "{{ tomcat_group }}"
      owner: "{{ tomcat_user }}"
      path: "{{ tomcat_home_version  }}/stub/responses"
      acl_entity: "{{ tomcat_user }}"
      acl_etype: user
      acl_permission: rwx
      acl_default: yes
      acl_state: present

tomcat_acl:
  external-stub:
    - path: "{{ tomcat_home_version  }}/stub/responses"
      entity: "{{ tomcat_user }}"
      etype: user
      permission: rwx
      default: yes
      state: present
```

Dict `common_files` can be used to manage files in various ways. This is for example done in [group_vars/keycloak/main.ym](https://github.com/c2platform/ansible-dev/blob/master/group_vars/keycloak/main.yml) in [ansible-dev](https://github.com/c2platform/ansible-dev/blob/master/group_vars/keycloak/main.yml) project. It has for example:

1. Configuration for download of JDBC jar.
2. Creation of a plain text property file `profile.properties` using inline `content`.
3. Manipulation of a XML file using regular expression.

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

This role is included included in the [common](./../common) role so we can use that.

```yaml
    - hosts: servers
      roles:
        - { role: c2platform.core.common,      tags: ["common"] }
```

Or we use it directly

```yaml
    - hosts: servers
      roles:
        - { role: c2platform.core.files,      tags: ["common"] }
```

Or we use it in any other role as described above

```yaml
- name: Files
  include_role:
    name: c2platform.core.files
    tasks_from: main
  vars:
    role_name: tomcat # role_name
    common_files: "{{ tomcat_files }}"
    common_directories: "{{ tomcat_directories }}"
    common_acl: "{{ tomcat_acl }}"
```
