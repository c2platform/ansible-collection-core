# Ansible Role: Java

A simple Ansible Role that installs Java on Linux servers. 

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Install](#install)
  - [Bundles](#bundles)
  - [Trusted sites](#trusted-sites)
  - [Etc profile.d JAVA_HOME](#etc-profiled-java_home)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

## Role Variables

### Install

Available variables are listed below, along with default values. Version to install 

```yaml
java:
  version: "jdk11_0411_oj9"
```

Vars for available versions to install

```yaml
java:
  version: jdk11_0411_oj9
  version_alternatives: []
  versions:
    jdk8_8u292b10_hs:
      url: https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u292-b10/OpenJDK8U-jdk_x64_linux_hotspot_8u292b10.tar.gz
      checksum: 0949505fcf42a1765558048451bb2a22e84b3635b1a31dd6191780eeccaa4ada
    jdk11_0411_oj9:
      url: https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz
      checksum: b1099cccc80a3f434728c9bc3b8a90395793b625f4680ca05267cf635143d64d
      bundles:
        - alias: bkd-ca
          url: file:///vagrant/.ca/mydomain/mydomain.crt      
```

### Bundles

Using `bundles` as shown above it is possible to import certificates and CA bundles.

### Trusted sites

Sites can be trusted by importing certificates using `java_trusted_sites` for example

```yaml
java_trusted_sites_enabled: yes
java_trusted_sites:
  certs:
    acs:
      alias: example1
      uri: example.com:443
    acs1:
      alias: example2
      uri: example2.com:443
  notify: restart tomcat instance
```

### Etc profile.d JAVA_HOME

For the default java a etc profile `/etc/profile/jdk.sh` is created that contains the `JAVA_HOME` 

java_home_etc_profile

## Dependencies

## Example Playbook
