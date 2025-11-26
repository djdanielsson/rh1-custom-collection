# Ansible Role: webserver

Deploys and configures an Apache HTTP Server.

## Requirements

- RHEL/CentOS/Rocky Linux 8+ or Ubuntu 20.04+
- Python 3.6+
- Ansible 2.14+

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Package configuration
webserver_packages:
  - httpd

# Service configuration
webserver_service: httpd
webserver_port: 80

# User and group
webserver_user: apache
webserver_group: apache

# Document root
webserver_document_root: /var/www/html

# Configuration
webserver_config_template: httpd.conf.j2
webserver_config_path: /etc/httpd/conf/httpd.conf

# Firewall
webserver_configure_firewall: true
webserver_firewall_services:
  - http
  - https

# Verification
webserver_verify_response: true

# Server configuration
webserver_server_admin: admin@example.com
webserver_server_name: "{{ ansible_fqdn }}"

# Security
webserver_server_tokens: Prod
webserver_server_signature: "Off"
```

## Dependencies

- `ansible.posix` collection (for firewalld module)

## Example Playbook

```yaml
---
- name: Deploy web server
  hosts: webservers
  become: true

  roles:
    - role: myorg.custom_collection.webserver
      webserver_server_name: www.example.com
      webserver_server_admin: admin@example.com
      webserver_port: 80
```

## Testing

This role includes Molecule tests:

```bash
# Test default scenario
molecule test

# Test on Ubuntu
molecule test -s ubuntu

# Test on CentOS
molecule test -s centos
```

## License

MIT

## Author Information

Created by the Platform Team for the Cloud-Native Ansible Lifecycle platform.
