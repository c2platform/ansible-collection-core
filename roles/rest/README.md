# Ansible Role rest

A simple Ansible Role for interacting with webservices using Ansible module [ansible.builtin.uri](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html). This role allows you to basically use [ansible.builtin.uri](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html) by providing a dict `rest_resources` which is used to configure groups of webservices requests.

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

The dict of groups of requests you need to provide is named `rest_resources`. An example is shown below.

```yaml
rest_resources:
  01_authenticate:
    headers: 
      X-OpenAM-Username: amadmin
      X-OpenAM-Password: "{{ am_amster_amadmin_pw }}"
      Content-Type: application/json
      Accept-API-Version: resource=2.0, protocol=1.0
    resources:
      - id: Authenticate
        url: json/realms/root/authenticate
  02_amUserAdmin:
    resources:
      - id: amUserAdmin
        url: json/realms/root/users/?_action=create
        body_format: json
        body:
          username: amUserAdmin
          userpassword: supersecret
        status_code: [201,409]
      - id: amDelegates # group
        url: json/realms/root/groups?_action=create
        body_format: json
        body:
          username: amDelegates
        status_code: [201,409]
```

The dict `01_authenticate` is for a group of REST interactions defined by the `resources`. Note that the other group of requests `02_amUserAdmin` does not have a `headers` key. This is because all other requests will use the same headers wich we can configure using var `rest_headers`.

```yaml
rest_headers:
  samb: "{{ rest_responses['01_authenticate'][0]['json']['tokenId']|default(omit) }}"
  Content-Type: application/json
  Accept-API-Version: resource=4.0, protocol=2.0
```

Note that the `samb` headers is defined by the `tokenId` that is part of the REST response of the first request `id: Authenticate` of the first group of requests `01_authenticate`. Some important points:

1. If you want to use information from a response in another request they need to be in separate groups.
2. The groups of requests are executed in *alphabetically* sorted order not *defined* order. So requests in `01_authenticate` will be executed before `02_amUserAdmin`.

The `url` attributes in `resources` lists are relative to `rest_base_url` for example defined as:

```yaml
rest_base_url: "https://{{ ansible_fqdn }}:{{ tomcat_ssl_connector_port }}/{{ am_context }}/"
```

Apart from `rest_headers` which was already discussed there are also vars for a default `rest_method`, `rest_timeout`, `rest_validate_certs`.

Of course Ansible allows you to easily integrate this role in your own role so you have more control on how, when, where REST requests are made. 

```yaml
- name: Configure using REST
  include_role:
    name: c2platform.core.rest
    tasks_from: main
```

The example below shows an `include_role` which uses the `rest_ansible_role` variable.

```yaml
  - name: Configure using REST
    include_role:
      name: c2platform.core.rest
      tasks_from: main
    vars:
      rest_ansible_role: am # role_name
```

Use of this variable allows you to redefine the vars to the namespace of your role. For example then you should use `am_rest_resources`. To explain a little further, configuring `rest_ansible_role: am` is just a more concise way of configuring the `include_role` as follows:

```yaml
- name: Configure using REST
  include_role:
    name: c2platform.core.rest
    tasks_from: main
  vars:
    rest_resources: "{{ am_rest_resources }}"
    rest_header: "{{ am_rest_header }}"
    rest_method: "{{ am_rest_method|default(omit) }}"
    rest_timout: "{{ am_rest_timout|default(omit) }}"
    rest_validate_certs: "{{ am_rest_validate_certs|default(False) }}"
    rest_base_url: "{{ am_rest_base_url }}"
    rest_enable: "{{ am_rest_enable|default(True) }}"
```

Note: an example of a role that integrates this role is [am](https://github.com/c2platform/ansible-collection-forgerock/tree/master/roles/am) role of the [Ansible ForgeRock Collection](https://github.com/c2platform/ansible-collection-forgerock).

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
    - hosts: servers
      roles:
         - { role: c2platform.core.rest }

      vars:
        rest_base_url: "https://{{ ansible_fqdn }}:{{ tomcat_ssl_connector_port }}/{{ am_context }}/"
        rest_headers:
          samb: "{{ rest_responses['01_authenticate'][0]['json']['tokenId']|default(omit) }}"
          Content-Type: application/json
          Accept-API-Version: resource=4.0, protocol=2.0
        rest_resources:
          01_authenticate:
            headers: 
              X-OpenAM-Username: amadmin
              X-OpenAM-Password: "{{ am_amster_amadmin_pw }}"
              Content-Type: application/json
              Accept-API-Version: resource=2.0, protocol=1.0
            resources:
              - id: Authenticate
                url: json/realms/root/authenticate
          02_amUserAdmin:
            resources:
              - id: amUserAdmin
                url: json/realms/root/users/?_action=create
                body_format: json
                body:
                  username: amUserAdmin
                  userpassword: supersecret
                status_code: [201,409]
              - id: amDelegates # group
                url: json/realms/root/groups?_action=create
                body_format: json
                body:
                  username: amDelegates
                status_code: [201,409]
```
