# Ansible Role: Java

A simple Ansible Role that installs Java on Linux servers. 

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  - [Tarball install](#tarball-install)
  - [Package install](#package-install)
  - [Install multiple versions](#install-multiple-versions)
  - [Manage keystore / trusts](#manage-keystore--trusts)
  - [Etc profile.d JAVA_HOME](#etc-profiled-java_home)
  - [Java facts](#java-facts)
  - [Only keystore / trusts \( no installation \)](#only-keystore--trusts--no-installation-)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

## Role Variables

### Tarball install

To perform tarfile / tarball install of JDK for example [AdopOpenJDK 11](https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz).

```yaml
java_version: jdk11_0411_oj9
java_versions:
    jdk11_0411_oj9:
      url: https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz
      checksum: b1099cccc80a3f434728c9bc3b8a90395793b625f4680ca05267cf635143d64d
```

### Package install

To install OS package of Java add `package: yes`. The key `openjdk-11-jdk` should match the package name. You should also configure the `folder`. For example to install OpenJDK 11 on Ubuntu 18.04 you can use:

```yaml
java_version: openjdk-11-jdk
java_versions:
  openjdk-11-jdk:
    folder: java-11-openjdk-amd64 # in /usr/lib/jvm
    package: yes
```

If you don't want to have the key match the package name you can configure package name using `name` attribute.

```yaml
java_version: jdk11
java_versions:
  jdk11:
    name: openjdk-11-jdk:
    folder: java-11-openjdk-amd64 # in /usr/lib/jvm
    package: yes
```

### Install multiple versions

You can use `java_version_alternatives` to install other / more versions. The example below will perform three installations of Java. Two package installs, one tarball.

```yaml
java_version: jdk11_0411_oj9
java_version_alternatives: ['openjdk-11-jdk', 'openjdk-8-jdk']
java_versions:
    jdk11_0411_oj9:
      url: https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz
      checksum: b1099cccc80a3f434728c9bc3b8a90395793b625f4680ca05267cf635143d64d
    openjdk-11-jdk:
      folder: java-11-openjdk-amd64 # in /usr/lib/jvm
      package: yes
    openjdk-8-jdk:
      package: yes
      folder: java-8-openjdk-amd64
      keystore: jre/lib/security/cacerts
```

### Manage keystore / trusts

You can optionally manage the keystore to allow trusted / secure communications using `trusts` attribute. As illustrated in the example below this role allows you to:

1. Trust services by providing domain name and port using `uri` attribute for example `youtube.com:443`.
2. Import certificates / CA bundles using `url` attribute for example https://letsencrypt.org/certs/isrgrootx1.pem.
3. Remove certificates you don't need anymore with attribute `state` with value `absent`.
4. Notify Ansible handlers to for example restart services whenever the keystore entries change.

```yaml
java_version: jdk11_0411_oj9
java_versions:
    jdk11_0411_oj9:
      url: https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz
      checksum: b1099cccc80a3f434728c9bc3b8a90395793b625f4680ca05267cf635143d64d
      trusts:
        - alias: youtube
          uri: youtube.com:443
          state: absent
        - alias: duckduckgo
          uri: duckduckgo.com:443
        - alias: isrgrootx1
          url: https://letsencrypt.org/certs/isrgrootx1.pem
      notify: restart-tomcat
```

Note: this role will also update certificates whenever necessary. 

### Etc profile.d JAVA_HOME

You can set `JAVA_HOME` in `/etc/profile.d/java.sh` using var `java_home_etc_profile`.

```yaml
java_home_etc_profile: yes
```

### Java facts

This role uses a module [java_facts](../../plugins/modules/java_facts.py) to set Java facts that you can use. For example when I have another role to install Tomcat and this role requires me to configure a `JAVA_HOME` this module will set a `java-home` attribute that I can use.

```yaml
tomcat_environment_variables:
  - name: JAVA_HOME
    value: "{{ java_versions[java_version]['java-home'] }}"
```

Other attributes you can use are `keytool` and `keystore`. You can also provide override the values if the defaults are not correct. For example the default location of the keystore might change from one Java version to the next. So for example older Java 8 has keystore in different location.

```yaml
java_versions:
  openjdk-8-jdk:
    package: yes
    folder: java-8-openjdk-amd64
    keystore: jre/lib/security/cacerts
```

### Only keystore / trusts ( no installation )

You can use this role to only manage a Java keystore using `trusts` attribute. For example when we have an Ansible role for Confluence and this role uses the embedded Java that Confluence ships with.

```yaml
- name: Configure trusts
  include_role:
    name: c2platform.core.java
    tasks_from: main
  vars:
    java_version: confluence
    java_versions:
      confluence:
        install: no
        java_home: "{{ confluence_home_version_app }}/jre"
        keystore: "{{ confluence_home_version_app }}/jre/lib/security/cacerts"
        trusts: "{{ confluence_trusts }}"
        notify: confluence-systemctl-restart
  when: confluence_trusts is defined
```

## Dependencies

## Example Playbook

```yaml
---
- name: java.yml
  hosts: java
  become: yes

  roles:
    - { role: c2platform.core.common,        tags: ["common"] }
    - { role: c2platform.core.java,          tags: ["common"] }

  vars:
    java_version: jdk11_0411_oj9
    java_version_alternatives: []
    java_versions:
        jdk11_0411_oj9:
          url: https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11_openj9-0.15.1/OpenJDK11U-jdk_x64_linux_openj9_11.0.4_11_openj9-0.15.1.tar.gz
          checksum: b1099cccc80a3f434728c9bc3b8a90395793b625f4680ca05267cf635143d64d
          trusts:
            - alias: youtube
              uri: youtube.com:443
              state: absent
            - alias: duckduckgo
              uri: duckduckgo.com:443
            - alias: isrgrootx1
              url: https://letsencrypt.org/certs/isrgrootx1.pem
          notify: restart-apache
        openjdk-11-jdk:
          # name: openjdk-11-jdk
          folder: java-11-openjdk-amd64 # in /usr/lib/jvm
          package: yes
        openjdk-8-jdk:
          package: yes
          folder: java-8-openjdk-amd64
          keystore: jre/lib/security/cacerts
```
