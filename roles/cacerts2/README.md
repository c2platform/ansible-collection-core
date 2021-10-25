# Ansible Role cacerts2

Ansible role that allows you to create / manage your [own small CA](https://docs.ansible.com/ansible/latest/collections/community/crypto/docsite/guide_ownca.html). Note: certificates are created, installed on nodes by other C2 Platform roles by include tasks from [certs.yml](./tasks/certs.yml) from this role. See for example [certs.yml](https://github.com/c2platform/ansible-collection-mw/tree/master/roles/apache/tasks/cert.yml) in [c2platform.mw.apache](https://github.com/c2platform/ansible-collection-mw/tree/master/roles/apache/).

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [CA](#ca)
  - [Certificates](#certificates)
- [Dependencies](#dependencies)
- [Example Play](#example-play)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

### CA

Certificates are created and stored on your "CA server" using `cacerts2_ca_server` in directory `cacerts2_ca_dir`. 

```yaml
cacerts2_ca_server: c2d-rproxy # inventory_hostname
cacerts2_ca_dir: /vagrant/.ca
```

To create the private key, cert etc of the CA the dict `cacerts2_ca_domain` is used. If you want the CA private key to have a passphrase you need to provide `passphrase` and `cipher: auto`. With `create` you can configure the type of files to create.

```yaml
cacerts2_ca_domain:
  common_name: example_com
  create: ['key','csr', 'crt', 'p12', 'pem']
  cipher: auto
  passphrase: supersecure # vault
```

These settings will be used by all nodes that need certificates installed so these needs to be "global vars" for example kept in `groupvars/all.yml` or `groupvars/all/certs.yml`.


This role uses a plugin module [set_certificate_facts](../plugins/modules/set_certificate_facts) to enhance `cacerts2_ca_domain` list with facts used for certificate creation and deployment. For example `cacerts2_ca_domain` as shown above will be enhanded to:

```yaml
cacerts2_ca_domain:
    cipher: auto
    common_name: c2d
    create:
    - key
    - csr
    - crt
    - p12
    - pem
    crl: /vagrant/.ca/c2d/c2d.crl
    crt: /vagrant/.ca/c2d/c2d.crt
    csr: /vagrant/.ca/c2d/c2d.csr
    dir: /vagrant/.ca/c2d
    key: /vagrant/.ca/c2d/c2d.key
    passphrase: supersecure
```

On the file system this will create for example

```
.ca/
└── c2d
    ├── c2d.crt
    ├── c2d.csr
    └── c2d.key
```

### Certificates

With the CA configured and the CA server provisioned other roles configure the certificates to create and deploy using the list `cacerts2_certificates`. For example for [c2platform.mw.apache](https://github.com/c2platform/ansible-collection-mw/tree/master/roles/apache/) configure

```yaml
apache_cacerts2_certificates:
  - common_name: "{{ hosts_domain|replace('.','_') }}"
    subject_alt_name:
    - "DNS:{{ hosts_domain }}"
    - "DNS:*.{{ hosts_domain }}"
    - "DNS:{{ ansible_hostname }}"
    - "DNS:{{ ansible_fqdn }}"
    - "IP:{{ ansible_eth1.ipv4.address }}"
    ansible_group: reverse_proxy
    deploy:
      key:
        dir: /etc/ssl/private
        owner: www-data
        group: www-data
        mode: '640'
      crt:
        dir: /etc/ssl/certs
        owner: www-data
        group: www-data
        mode: '644'
```

The plugin module [set_certificate_facts](../plugins/modules/set_certificate_facts) will enhance `apache_cacerts2_certificates` to for example something like


```yaml
apache_cacerts2_certificates:
-   common_name: seetoo_tech
    create:
        crt: /vagrant/.ca/c2d/apache/seetoo_tech-c2d-rproxy.crt
        csr: /vagrant/.ca/c2d/apache/seetoo_tech-c2d-rproxy.csr
        key: /vagrant/.ca/c2d/apache/seetoo_tech-c2d-rproxy.key
        p12: /vagrant/.ca/c2d/apache/seetoo_tech-c2d-rproxy.p12
        pem: /vagrant/.ca/c2d/apache/seetoo_tech-c2d-rproxy.pem
    deploy:
        crt:
            dest: /etc/ssl/certs/seetoo_tech-c2d-rproxy.crt
            dir: /etc/ssl/certs
            group: www-data
            mode: '644'
            owner: www-data
        key:
            dest: /etc/ssl/private/seetoo_tech-c2d-rproxy.key
            dir: /etc/ssl/private
            group: www-data
            mode: '640'
            owner: www-data
    dir: /vagrant/.ca/c2d/apache
    subject_alt_name:
    - DNS:seetoo.tech
    - DNS:*.seetoo.tech
    - DNS:c2d-rproxy
    - IP:1.1.1.3
```

On apache nodes the `deploy` config will create:

* Certificate `/etc/ssl/certs/seetoo_tech-c2d-rproxy.crt`
* Key `/etc/ssl/certs/seetoo_tech-c2d-rproxy.key`

On the CA server this will create for example

```
.ca/
└── c2d
    ├── apache
    │   ├── keycloak-c2d-rproxy.crt
    │   ├── keycloak-c2d-rproxy.csr
    │   ├── keycloak-c2d-rproxy.key
    │   ├── keycloak-c2d-rproxy.p12
    │   ├── keycloak-c2d-rproxy.pem
    │   ├── seetoo_tech-c2d-rproxy.crt
    │   ├── seetoo_tech-c2d-rproxy.csr
    │   ├── seetoo_tech-c2d-rproxy.key
    │   ├── seetoo_tech-c2d-rproxy.p12
    │   └── seetoo_tech-c2d-rproxy.pem
    ├── c2d.crt
    ├── c2d.csr
    └── c2d.key
```

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Play

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

**CA Certs Server play** to create the CA server.

```yaml
---
- name: CA Certs Server
  hosts: cacerts_server
  become: yes

  roles:
    - { role: c2platform.core.common,        tags: ["common"] }
    - { role: c2platform.core.cacerts2,      tags: ["certificates"] }

  vars:
    cacerts2_ca_server: "{{ groups['cacerts_server'][0] }}"
    cacerts2_ca_dir: /vagrant/.ca
    cacerts2_ca_domain:
      common_name: example_com
      create: ['key','csr', 'crt', 'p12', 'pem']
      cipher: auto
      passphrase: supersecure # vault
```

Other roles such as [c2platform.mw.apache](https://github.com/c2platform/ansible-collection-mw/tree/master/roles/apache/) that support / integrate with this role can then create and deploy certificates for example using

```yaml
apache_cacerts2_certificates:
  - common_name: "{{ hosts_domain|replace('.','_') }}"
    subject_alt_name:
    - "DNS: {{ hosts_domain }}"
    - "DNS: *.{{ hosts_domain }}"
    - "DNS:{{ ansible_hostname }}"
    - "DNS:{{ ansible_fqdn }}"
    - "IP:{{ ansible_eth1.ipv4.address }}"
    ansible_group: reverse_proxy
    deploy:
      key:
        path: /etc/ssl/private
        owner: www-data
        group: www-data
        mode: '640'
      crt:
        path: /etc/ssl/certs
        owner: www-data
        group: www-data
        mode: '644'
```

For a fully configured / working example see the [ansible-dev](https://github.com/c2platform/ansible-dev) project:

* Play [mw/reverse_proxy](https://github.com/c2platform/ansible-dev/tree/master/plays/mw/reverse_proxy.yml)