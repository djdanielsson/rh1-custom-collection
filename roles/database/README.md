# Ansible Role: database

Deploys and configures PostgreSQL database server.

## Requirements

- RHEL/CentOS/Rocky Linux 8+
- Python 3.6+
- Ansible 2.14+
- `community.postgresql` collection

## Role Variables

```yaml
# Service
database_service: postgresql

# PostgreSQL settings
database_listen_addresses: localhost
database_port: 5432
database_max_connections: 100

# Database and user (set in your playbook with vault)
database_name: myapp
database_user: myapp_user
database_password: "{{ lookup('env', 'DB_PASSWORD') }}"
```

## Example Playbook

```yaml
---
- name: Deploy database server
  hosts: databases
  become: true

  roles:
    - role: myorg.custom_collection.database
      database_name: webapp
      database_user: webapp_user
      database_password: "{{ vault_db_password }}"
```

## License

MIT
