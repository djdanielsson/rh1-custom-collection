# Ansible Collection - myorg.custom_collection

**Purpose**: Example custom Ansible collection with roles, modules, plugins, and filters  
**Repository**: https://github.com/djdanielsson/rh1-custom-collection.git  
**Created with**: ansible-creator  
**Testing**: Molecule scenarios, ansible-test, pytest

## Overview

This repository contains a custom Ansible collection demonstrating best practices for collection development. It includes example roles, custom modules, filters, lookups, and comprehensive testing.

**Constitution Compliance**: Article IV (Production-Grade Quality) - Tested, documented, idempotent

## Collection Contents

### Roles (4)

| Role | Purpose | Molecule Tested |
|------|---------|-----------------|
| `webserver` | Deploy and configure web servers | ✅ Yes |
| `database` | Deploy and configure databases | ✅ Yes |
| `monitoring` | Deploy monitoring agents | ✅ Yes |

### Modules (2)

| Module | Purpose |
|--------|---------|
| `sample_module` | Example module demonstrating module structure |
| `sample_module_info` | Example info/facts module |

### Filters (4)

| Filter | Purpose |
|--------|---------|
| `sample_filter` | Example filter plugin |
| `normalize_text` | Text normalization utilities |
| `slugify` | Convert text to URL-safe slugs |
| `title_case` | Convert text to title case |

### Lookups (2)

| Lookup | Purpose |
|--------|---------|
| `sample_lookup` | Example lookup plugin |
| `vault_secrets` | HashiCorp Vault secret lookup |

### Action Plugins (1)

| Plugin | Purpose |
|--------|---------|
| `sample_action` | Example action plugin |

## Repository Structure

```
automation-collection-example/
├── galaxy.yml                    # Collection metadata and version
├── README.md                     # This file
├── CHANGELOG.rst                 # Release history
├── requirements.txt              # Python dependencies for development
├── test-requirements.txt         # Testing dependencies
├── pyproject.toml                # Python project config
├── tox-ansible.ini               # Tox configuration for testing
│
├── roles/                        # Ansible roles
│   ├── webserver/
│   │   ├── defaults/main.yml
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── templates/
│   ├── database/
│   ├── monitoring/
│
├── plugins/                      # Custom plugins
│   ├── modules/
│   │   ├── sample_module.py
│   │   └── sample_module_info.py
│   ├── filter/
│   │   ├── sample_filter.py
│   │   └── text_filters.py
│   ├── lookup/
│   │   ├── sample_lookup.py
│   │   └── vault_secrets.py
│   └── action/
│       └── sample_action.py
│
├── tests/                        # Test suites
│   ├── unit/                     # Python unit tests
│   ├── integration/              # Integration tests
│   └── sanity/                   # Ansible sanity tests
│
├── extensions/                   # Extended features
│   ├── molecule/                 # Shared Molecule resources
│   └── eda/                      # Event-Driven Ansible rulebooks
│       └── rulebooks/
│
├── docs/                         # Documentation
│   └── docsite/
│
└── meta/
    └── runtime.yml               # Ansible version requirements
```

## Installation

### From Galaxy (when published)

```bash
ansible-galaxy collection install myorg.custom_collection
```

### From Git

```bash
ansible-galaxy collection install git+https://github.com/djdanielsson/rh1-custom-collection.git
```

### In requirements.yml

```yaml
collections:
  - name: myorg.custom_collection
    source: https://github.com/djdanielsson/rh1-custom-collection.git
    type: git
    version: main  # or specific tag like 26.1.5-0
```

## Usage

### Using Roles

```yaml
- name: Deploy web server
  hosts: webservers
  roles:
    - role: myorg.custom_collection.webserver
      vars:
        webserver_port: 8080
        webserver_document_root: /var/www/html
```

### Using Modules

```yaml
- name: Use custom module
  myorg.custom_collection.sample_module:
    name: example
    state: present
  register: result

- name: Get info
  myorg.custom_collection.sample_module_info:
    name: example
  register: info
```

### Using Filters

```yaml
- name: Use text filters
  ansible.builtin.debug:
    msg: "{{ 'Hello World' | myorg.custom_collection.slugify }}"
    # Output: "hello-world"
```

### Using Lookups

```yaml
- name: Get secret from Vault
  ansible.builtin.debug:
    msg: "{{ lookup('myorg.custom_collection.vault_secrets', 'secret/data/myapp') }}"
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/djdanielsson/rh1-custom-collection.git
cd automation-collection-example

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r test-requirements.txt

# Install collection in development mode
ansible-galaxy collection install . --force
```

### Running Tests

#### Molecule (Role Testing)

```bash
# Test a specific role
cd roles/webserver
molecule test

# Test with a specific scenario
molecule test -s default

# Run converge only (faster iteration)
molecule converge
molecule verify
molecule destroy
```

#### Unit Tests

```bash
# Run Python unit tests
pytest tests/unit/ -v
```

#### Sanity Tests

```bash
# Run ansible-test sanity
ansible-test sanity --docker
```

#### All Tests

```bash
# Run all tests via tox
tox
```

### Linting

```bash
# Ansible lint
ansible-lint

# Python lint
flake8 plugins/
pylint plugins/

# YAML lint
yamllint .
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run all hooks
pre-commit run --all-files
```

## Building the Collection

```bash
# Build collection artifact
ansible-galaxy collection build

# Output: myorg-custom_collection-X.Y.Z.tar.gz
```

## Versioning

This collection follows **CalVer: YY.M.D-PATCH**

```
26.1.5-0 - January 5, 2025, initial release
26.1.5-1 - January 5, 2025, hotfix
26.1.6-0 - January 6, 2025, new release
```

Update version in `galaxy.yml`:

```yaml
namespace: myorg
name: custom_collection
version: "26.1.5-0"
```

## CI/CD

### GitHub Actions

On every push/PR:
- Lint (ansible-lint, yamllint, flake8)
- Unit tests (pytest)
- Sanity tests (ansible-test)
- Molecule tests (all roles)

On tag push:
- Build collection
- Publish to Galaxy (if configured)

### Integration with AAP

This collection is included in the custom Execution Environment and can be used in AAP job templates:

```yaml
# In aap-config-as-code/group_vars/aap_dev/projects.yml
controller_projects_dev:
  - name: Custom Collection
    organization: Default
    scm_type: git
    scm_url: https://github.com/djdanielsson/rh1-custom-collection.git
    scm_branch: main
```

## Troubleshooting

### Molecule Test Failures

**Symptoms**: `molecule test` fails with various errors

**Diagnosis**:
```bash
# Check molecule configuration
molecule list

# Run with verbose output
molecule --debug test

# Check molecule logs
tail -f ~/.cache/molecule/<scenario>/ansible.log
```

**Common Solutions**:
- **Missing dependencies**: Install required collections with `ansible-galaxy collection install -r requirements.yml`
- **Platform issues**: Ensure Docker/Podman is running and accessible
- **Syntax errors**: Validate YAML with `ansible-lint` or `yamllint`
- **Resource conflicts**: Clean up previous test instances with `molecule destroy`

### Ansible-lint Errors

**Symptoms**: Linting fails with rule violations

**Diagnosis**:
```bash
# Run specific linter rules
ansible-lint --rules fqcn roles/

# Check ansible-lint version
ansible-lint --version

# Run with verbose output
ansible-lint -v roles/
```

**Common Fixes**:
- **FQCN violations**: Use fully qualified collection names (e.g., `ansible.builtin.copy`)
- **Naming issues**: Ensure all tasks have descriptive names
- **Syntax problems**: Fix YAML indentation and formatting
- **Import issues**: Add missing `ansible.builtin` imports

### Collection Build Failures

**Symptoms**: `ansible-galaxy collection build` fails

**Diagnosis**:
```bash
# Validate galaxy.yml
ansible-galaxy collection init --dry-run .

# Check for missing files
ansible-galaxy collection build --dry-run

# Validate manifest
python -c "import yaml; yaml.safe_load(open('galaxy.yml'))"
```

**Solutions**:
- **Invalid galaxy.yml**: Fix syntax errors in collection metadata
- **Missing files**: Ensure all required directories exist (plugins/, roles/, etc.)
- **Version conflicts**: Check for duplicate or conflicting versions
- **Dependency issues**: Verify requirements.yml is valid

### Galaxy Publishing Issues

**Symptoms**: `ansible-galaxy collection publish` fails

**Diagnosis**:
```bash
# Check API key
ansible-galaxy login --help

# Validate collection
ansible-galaxy collection publish --help

# Test with dry run (if available)
# ansible-galaxy collection publish --dry-run *.tar.gz
```

**Solutions**:
- **Authentication**: Verify Galaxy API key is valid and has publish permissions
- **Namespace issues**: Ensure collection namespace matches Galaxy account
- **Version conflicts**: Check if version already exists on Galaxy
- **Network issues**: Verify connectivity to galaxy.ansible.com

### Execution Environment Issues

**Symptoms**: Collection not available in custom EE

**Diagnosis**:
```bash
# Check EE build logs
podman/docker logs <ee-build-container>

# Validate requirements.yml
ansible-galaxy collection install -r requirements.yml --dry-run

# Test collection loading
ansible-galaxy collection list | grep myorg
```

**Solutions**:
- **Build failures**: Fix dependencies in execution-environment.yml
- **Path issues**: Ensure collection is properly included in EE build
- **Version mismatches**: Align collection and EE versions
- **Registry issues**: Verify EE image is pushed and accessible

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-role`
3. Make changes and add tests
4. Run linting: `pre-commit run --all-files`
5. Run tests: `molecule test` (for roles) or `pytest` (for plugins)
6. Commit with descriptive message
7. Create Pull Request

### Code Standards

- Follow [Ansible Best Practices](https://github.com/djdanielsson/rh1_ansible_code_lifecycle/blob/main/docs/ANSIBLE-BEST-PRACTICES.md)
- All roles must have Molecule tests
- All plugins must have unit tests
- All code must pass ansible-lint

## Links

### Related Repositories
- **Platform Workspace**: https://github.com/djdanielsson/rh1_ansible_code_lifecycle
- **Cluster Config**: https://github.com/djdanielsson/rh1-cluster-config
- **AAP Config as Code**: https://github.com/djdanielsson/rh1-aap-config-as-code
- **Execution Environment**: https://github.com/djdanielsson/rh1-custom-ee
- **Release Manifests**: https://github.com/djdanielsson/rh1-release-manifest

### External Resources
- [Ansible Collection Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)
- [Molecule Documentation](https://molecule.readthedocs.io/)
- [ansible-creator](https://ansible.readthedocs.io/projects/creator/)
- [Red Hat CoP Best Practices](https://redhat-cop.github.io/automation-good-practices/)
