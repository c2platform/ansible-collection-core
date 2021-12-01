# Ansible Role Files

Manage files, directories and ACL. This role is included in the [common](./../common) role.

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Files \( common_files \)](#files--common_files-)
  - [Linux ACL \( common_acl \)](#linux-acl--common_acl-)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

### Files ( common_files )

The dict `common_files` can be used to create files in various ways using for example [ansible.builtin.copy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html), [ansible.builtin.get_url](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/get_url_module.html). It can also be used to modify files using [ansible.builtin.replace](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/replace_module.html), [xml](https://docs.ansible.com/ansible/2.9/modules/xml_module.html).

For example let's say we want to provide [CRL](https://en.wikipedia.org/wiki/Certificate_revocation_list) to our Tomcat application that uses [Apache Rampart](http://axis.apache.org/axis2/java/rampart/) for secure messaging. In our Tomcat role we include `common_files` as follows

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

Note: the reason we do not use this role outright in our Ansible play is because we want more control over when and how files are created. As `group_vars` or `host_vars` we can now create a `crl` directory in the Tomcat `conf` directory.


```yaml
tomcat_directories:
  crl:
    - path: "{{ tomcat_apps_properties_folder }}/crl"
      owner: "{{ tomcat_user }}"
      group: "{{ tomcat_group }}"
```

We now define for our convience our list of CRL using a help var `my_crl` with items with only `dest`, `src` keys.

```yaml
my_crl:
  - src: http://crl.pkioverheid.nl/PrivateRootLatestCRL-G1.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/PrivateRootLatestCRL-G1.crl"
  - src: http://crl.pkioverheid.nl/DomPrivateServicesLatestCRL-G1.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/DomPrivateServicesLatestCRL-G1.crl"
  - src: http://crl.managedpki.com/KPNBVPKIoverheidPrivateServicesCAG1/LatestCRL.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/KPNBVPKIoverheidPrivateServicesCAG1-LatestCRL.crl"
  - src: http://crl.quovadisglobal.com/pkioprivservg1.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/pkioprivservg1.crl"
  - src: http://crl.pkioverheid.nl/EVRootLatestCRL.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/EVRootLatestCRL.crl"
  - src: http://crl.pkioverheid.nl/DomeinServerCA2020LatestCRL.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/DomeinServerCA2020LatestCRL.crl"
  - src: http://crl.pkioverheid.nl/DomeinServerCA2020LatestCRL.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/DomeinServerCA2020LatestCRL.crl"
```

All the files need to be created using `tomcat_files` with the same properties so here too we create a help variable `my_clr_attrs`

```yaml
my_clr_attrs:
  mode: '0700'
  owner: "{{ tomcat_user }}"
  group: "{{ tomcat_group }}"
  delegate: yes
  environment:
    http_proxy: http://127.0.0.1:8888
```

Using the Jinja filter `c2platform.core.add_attributes` we now define `tomcat_files` by adding the default attributes to `my_crl`.

```yaml
tomcat_files:
  crl: "{{ my_crl|c2platform.core.add_attributes(my_clr_attrs) }}"
```
Of course you can also writeout `tomcat_files` without any `my_crl`, `my_clr_attrs` and the filter `c2platform.core.add_attributes` as follows:

```yaml
tomcat_files:
  crl:
  - src: http://crl.pkioverheid.nl/PrivateRootLatestCRL-G1.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/PrivateRootLatestCRL-G1.crl"
    mode: '0700'
    owner: "{{ tomcat_user }}"
    group: "{{ tomcat_group }}"
    delegate: yes
    environment:
      http_proxy: http://127.0.0.1:8888
  - src: http://crl.pkioverheid.nl/DomPrivateServicesLatestCRL-G1.crl
    dest: "{{ tomcat_apps_properties_folder|default('whatever') }}/crl/DomPrivateServicesLatestCRL-G1.crl"
    mode: '0700'
    owner: "{{ tomcat_user }}"
    group: "{{ tomcat_group }}"
    delegate: yes
    environment:
      http_proxy: http://127.0.0.1:8888
  - src: ....etc
```

To configure our application we might have to provide a comma separated list of the CRLs for example for a Java property files were we use var `siwu_broker_crl`. 

```yaml
siwu_broker_crl: "{{ suwinet_broker_crl|map(attribute='dest')|join(',') }}"
```

### Linux ACL ( common_acl )

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
