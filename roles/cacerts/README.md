# Ansible Role cacerts

An Ansible Role that manages Java keystores using [java_cert](https://docs.ansible.com/ansible/latest/modules/java_cert_module.html) module.

Note: `java_cert` check for existance using the certificate alias. If certificates are renewed the new certificates are not imported. As a workaround to trigger the import of a new certificate you can change the alias.

This role can also be used to manage OS keystore.
<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Ansible roles](#ansible-roles)
  - [Trusted sites](#trusted-sites)
  - [Add certificates](#add-certificates)
  - [Add OS certs](#add-os-certs)
- [Dependencies](#dependencies)
- [Example playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

### Ansible roles

Add keystore info using `cacerts_roles_supported` and `cacerts_roles`. For example for Jira. Add it as a supported role with

```yaml
cacerts_roles_supported: ['jira']
```

Add Jira keystore info

```yaml
cacerts_roles:
  jira:
    keystore_path: "{{ jira_home_version_app|default(omit) }}/jre/lib/security/cacerts"
    keystore_pass: "{{ cacerts_keystore_pass }}"
    notify: jira-systemctl-restart
    executable: "{{ jira_home_version_app|default(omit) }}/jre/bin/keytool"
```

### Trusted sites

Configure sites that should be trusted using `cacerts_trusted_sites` for example as shown below. `notify` can be used to notify handlers for example to trigger restart of a tomcat instance.

```yaml
cacerts_trusted_sites:
  - name: bkd-ds
    url: 1.1.1.51
    port: 4444
    notify: restart tomcat instance
  - name: bkd-ds2
    url: 1.1.1.58
    port: 4444
    notify: restart tomcat instance
  - name: google.com
    url: google.com
    port: 443
    notify: restart tomcat instance
```

Note: because you can specify `notify` typically you would add this configuration to a group for example for tomcat nodes.

### Add certificates

Configure certificates, CA bundles to import using `cacerts_import_certs_urls` for example:

```yaml
cacerts_import_certs_urls:
  - name: mycompanybundle
    url: https://example.com/SectigoRSADVBundle.crt
```
### Add OS certs

Configure array of URLS to download into OS keystore:

```yaml
cacerts_os_ca_pem_urls:
  - https://example.com/SectigoRSADVBundle.crt
```

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

This role is included in the common role.

```yaml
- name: bitbucket.yml
  hosts: bitbucket
  become: yes

  roles:
    - { role: c2platform.core.common,               tags: ["common"] }
```


