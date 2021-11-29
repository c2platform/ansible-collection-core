# Ansible Collection - c2platform.core

C2 Platform generic roles that are used by all or some other roles. These roles don't create services / processes on target node but are depedencies e.g. packages required by those roles. Or these roles help with Ansible provisioning for example offers generic Ansible modules, filters etc. 

## Roles

* [secrets](./roles/secrets) workaround for lack of support for vault when using AWX.
* [cacerts2](./roles/cacerts2) create your [own small CA](https://docs.ansible.com/ansible/latest/collections/community/crypto/docsite/guide_ownca.html).
* [apt_repo](./roles/apt_repo) add APT keys, repositories.
* [files](./roles/files) manage files, directories, ACL.
* [service](./roles/service) create systemd services.

## Plugins

Module plugins:

* 

Filter plugins:

*

## TODO

1. Remove / move dependency on c2platform.platform.monit and c2platform.test.swid.
2. 
