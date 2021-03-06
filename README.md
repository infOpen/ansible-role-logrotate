# logrotate

[![CI](https://github.com/infOpen/ansible-role-logrotate/workflows/CI/badge.svg)](https://github.com/infOpen/ansible-role-logrotate/actions)
[![Mergify Status][mergify-status]][mergify]
[![Updates](https://pyup.io/repos/github/infOpen/ansible-role-logrotate/shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-logrotate/)
[![Python 3](https://pyup.io/repos/github/infOpen/ansible-role-logrotate/python-3-shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-logrotate/)
[![Ansible Role](https://img.shields.io/ansible/role/25591.svg)](https://galaxy.ansible.com/infOpen/logrotate/)

Install logrotate package.

## Requirements

This role requires Ansible 2.8 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/ansible-community/molecule) to run tests.

Local and Github Actions tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- CentOS 7
- CentOS 8
- Debian Buster
- Debian Stretch
- Ubuntu Bionic
- Ubuntu Focal

and use:
- Ansible 2.8.x
- Ansible 2.9.x

### Running tests

#### Using Docker driver

```
$ tox
```

You can also configure molecule options and molecule command using environment variables:
* `MOLECULE_OPTIONS` Default: "--debug"
* `MOLECULE_COMMAND` Default: "test"

```
$ MOLECULE_OPTIONS='' MOLECULE_COMMAND=converge tox
```

## Role Variables

### Default role variables

``` yaml
# Defaults vars file for logrotate role
logrotate_packages: "{{ _logrotate_packages }}"
logrotate_repository_cache_valid_time: 3600
logrotate_repository_install_recommends: False

# Configuration paths
logrotate_conf_d_dir:
  path: '/etc/logrotate.d'
  owner: 'root'
  group: 'root'
  mode: '0755'
logrotate_conf_main_file:
  path: '/etc/logrotate.conf'
  owner: 'root'
  group: 'root'
  mode: '0644'

# Configuration content
logrotate_main_config: |
  weekly
  su root syslog
  rotate 4
  create
  include {{ logrotate_conf_d_dir.path }}
  /var/log/wtmp {
      missingok
      monthly
      create 0664 root utmp
      rotate 1
  }
  /var/log/btmp {
      missingok
      monthly
      create 0660 root utmp
      rotate 1
  }
logrotate_items: []
```

## Define logrotate items

You can define easily new logrotate items, the will be stored in *logrotate_conf_d_dir.path*.

``` yaml
logrotate_items:
  - name: 'my_app'
    content: |
      "/var/log/my_app.log" {
          daily
          missingok
          rotate 54
          compress
          delaycompress
          notifempty
          create 640 root root
          sharedscripts
          postrotate
              if [ -f /var/run/nginx.pid ]; then
                  kill -USR1 `cat /var/run/nginx.pid`
              fi
          endscript
      }
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.logrotate }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- https://www.infopen.pro
- a.chaussier [at] infopen.pro

[mergify]: https://mergify.io
[mergify-status]: https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/infOpen/ansible-role-logrotate&style=flat
