# Ansible Role service

Add custom services to your Linux system. Currently only [systemd](https://systemd.io/) is supported. This role is designed to be easily adapt generation of service files for your need. 

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Sections, keys and defaults](#sections-keys-and-defaults)
  - [Service defintion](#service-defintion)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

### Sections, keys and defaults

Variable `service_sections`  contains the sections for example `[Unit]` This role provides defaults for example

```yaml
service_sections: ['Unit', 'Service', 'Install']
```

Per section `service_keys` is used to configure the type of settings that can be made. The role provides defaults for example:

```yaml
service_keys:
  Unit: ['Description', 'After']
  Service: ['Type', 'WorkingDirectory', 'User', 'Group', 'ExecStart', 'ExecStop', 'Environment', 'EnvironmentFile', 'Restart', 'RestartSec', 'PIDFile', 'LimitNOFILE', 'LimitNPROC']
  Install: ['WantedBy']
```

Default values for settings can be provided using `service_defaults`. This role provides defaults for example: 

```yaml
service_defaults:
  Install:
    WantedBy: multi-user.target
```

The role aims to provide configuration in `service_sections`, `service_keys` and `service_defaults` that are suitable for most service definitions. 

### Service defintion

Using dictionary `service` we can now configure for example a simple Tomcat service:

```yaml
service:
  Name: "{{ tomcat_service_name }}"
  Unit:
    Description: "{{ tomcat_service_name }}"
  Service:
    User: "{{ tomcat_user }}"
    Group: "{{ tomcat_group }}"
    ExecStart: "/bin/bash {{ tomcat_home_version }}/bin/catalina.sh run" 
```

It is also possible to pass an array of `service` using `services`

```yaml
services:
  - Name: "{{ tomcat_service_name }}"
    Unit:
      Description: "{{ tomcat_service_name }}"
    Service:
      User: "{{ tomcat_user }}"
      Group: "{{ tomcat_group }}"
      ExecStart: "/bin/bash {{ tomcat_home_version }}/bin/catalina.sh run" 
  - Name: someotherservice
```


## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
    - hosts: servers
      roles:
         - { role: c2platform.core.service }

      vars:
        service:
          Name: "{{ tomcat_service_name }}"
          Unit:
            Description: "{{ tomcat_service_name }}"
          Service:
            User: "{{ tomcat_user }}"
            Group: "{{ tomcat_group }}"
            ExecStart: "/bin/bash {{ tomcat_home_version }}/bin/catalina.sh run" 

```

In many cases it might make more sense to include this role in other roles. This way you have more control over order in which resources including the service are created, restarted etc. In such cases you can use `include_role` to reuse the `service` role in another role. The example below shows how we introduce a new dictionary `tomcat_service`.


```yaml
- name: Service
  include_role:
    name: c2platform.core.service
    tasks_from: main
  vars:
    service: "{{ tomcat_service }}"
```          
