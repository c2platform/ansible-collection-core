# Ansible Role: AdoptOpenJDK

A simple Ansible Role that installs [AdoptOpenJDK](https://adoptopenjdk.net/) on Linux servers. Java home will be made available as fact `adoptopenjdk_java_home`. 

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
    - [Install](#install)
    - [Bundles](#bundles)
    - [Etc environment / JAVA_HOME](#etc-environment--java_home)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
- [License](#license)
- [Author Information](#author-information)

<!-- /MarkdownTOC -->

## Requirements

## Role Variables

### Install

Available variables are listed below, along with default values. Version to install 

```yaml
adoptopenjdk:
  version: "jdk8u222b10_oj9"
```

Vars for available versions to install

```yaml
adoptopenjdk:
  versions:
    jdk8u222b10_oj9:
      url: https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u222-b10_openj9-0.15.1/OpenJDK8U-jdk_x64_linux_openj9_8u222b10_openj9-0.15.1.tar.gz
      checksum: 20cff719c6de43f8bb58c7f59e251da7c1fa2207897c9a4768c8c669716dc819
      bundles:
        - alias: bkd-ca
          url: file:///vagrant/.ca/suwinet.nl/ca-suwinet.nl.crt      
```

### Bundles

Using `bundles` as shown above it is possible to import certificates and CA bundles.

### Etc environment / JAVA_HOME

To add `JAVA_HOME` to `/etc/environment` use `adoptopenjdk_java_home_etc_environment: true`. Default is false.

## Dependencies

## Example Playbook

## License

MIT / BSD

## Author Information

This role was created in 2019 by [Onno van der Straaten](https://www.onknows.com/).
