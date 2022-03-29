# Ansible Collection - c2platform.core

C2 Platform generic roles that are used by all or some other roles. These roles don't create services / processes on target node but are depedencies e.g. packages required by those roles. Or these roles help with Ansible provisioning for example offers generic Ansible modules, filters etc. 

## Roles

* [secrets](./roles/secrets) workaround for lack of support for vault when using AWX.
* [cacerts2](./roles/cacerts2) create your [own small CA](https://docs.ansible.com/ansible/latest/collections/community/crypto/docsite/guide_ownca.html).
* [apt_repo](./roles/apt_repo) add APT keys, repositories.
* [files](./roles/files) manage files, directories, ACL.
* [service](./roles/service) create systemd services.
* [java](./roles/java) install java, manage keystores.
* [facts](./roles/facts) gather facts.  
* [lcm](./roles/lcm) facts for LCM operations for other roles to build upon.
* [lvm](./roles/lvm) manage data disks for roles using [LVM](https://en.wikipedia.org/wiki/Logical_Volume_Manager_%28Linux%29).
* [rest](./roles/rest) interact with REST webservices.
* [postgresql_tasks](./roles/postgresql_tasks) include tasks for PostgreSQL database operations.
* [postgresql_client](./roles/postgresql_client).

## Plugins

Module plugins:

* 

Filter plugins:

*

## TODO

1. 
