# Ansible Role postgresql_tasks

This Ansible "role" includes reusable PosgreSQL tasks. This tasks are intended to run on the PostgreSQL server node itself.

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Terminate and block sessions](#terminate-and-block-sessions)
  - [Allow sessions](#allow-sessions)
  - [Create / upgrade database](#create--upgrade-database)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

These tasks are intended to be included by Ansible roles that use the [lcm](./../lcm) role to automate LCM operations. 

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

These tasks assumes specific role variables are used to configure a database connection. The vars are prefixed by the role name for example: 

```yaml
jira_database_username: jira
jira_database_password: supersecure
jira_database_host: localhost
jira_database_port: 5432
jira_database_name: jira
jira_database_admin_username: ansible
jira_database_admin_password: supersecure
jira_database_template: template0
jira_database_type_config: postgres72
jira_database_type: postgresql
jira_database_driver_class: org.postgresql.Driver
jira_database_validation_query: select 1
jira_database_schema: public
jira_database_lc_collate: C
jira_database_lc_ctype: C
```


### Terminate and block sessions

Tasks in [terminate-block-sessions.yml](./tasks/terminate-block-sessions.yml) can be terminate and block sessions to a specific database in order to do certain database operations that require no active sessions exist. For example dropping a database or using a database as a template.

This include will use only the port for example `jira_database_port` which typically is `5432`. When you include this task you have to specificy the database name with `terminate_database` and `lcm_role_upgrade` as shown below.

```yaml
- name: Terminate and block sessions on upgrade
  include_role:
    name: c2platform.core.postgresql_tasks
    tasks_from: psql-terminate-block-sessions
  vars:
    terminate_database: "{{ jira_database_name_version }}"
    lcm_role_upgrade: "jira"

```

### Allow sessions

Tasks in [allow-sessions.yml](./tasks/allow-sessions.yml) can be used to allow sessions to a specific database. 

This include will use only the port for example `jira_database_port` which typically is `5432`. When you include this task you have to specificy the database name with `allow_database` and `lcm_role_upgrade` as shown below.

```yaml
- name: Allow sessions after database copy
  include_role:
    name: c2platform.core.postgresql_tasks
    tasks_from: allow-sessions
  vars:
    allow_database: "{{ jira_database_name_version }}"
    lcm_role_upgrade: "jira"
```


### Create / upgrade database

Tasks in [database.yml](./tasks/database.yml) can be used to create and upgrade a database in your role. These database are version enabled so as to support easy rollback, rollforward operations.

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

An example of the use of these reusable tasks can be foud in [restore_db_postgresql.yml](https://github.com/c2platform/ansible-collection-mgmt/blob/master/roles/backup/tasks/restore_db_postgresql.yml) in the [c2platform.mgmt.backup](https://github.com/c2platform/ansible-collection-mgmt/tree/master/roles/backup) role.

```yaml
    - name: Terminate and block sessions on upgrade
      # a database cannot be dropped with active sessions
      include_role:
        name: c2platform.core.postgresql_tasks
        tasks_from: psql-terminate-block-sessions
      vars:
        terminate_database: "{{ vars[item + '_database_name_version']  }}"
        lcm_role_upgrade: "{{ item }}"
      when: backup_restore[item]['db_tar'] is defined
```
