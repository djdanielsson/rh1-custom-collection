# Development Guide - myorg.custom_collection

This collection was created using `ansible-creator` and includes Molecule for testing.

## Repository Information

- **Git Repository**: https://github.com/djdanielsson/rh1-custom-collection.git
- **Namespace**: myorg
- **Collection Name**: custom_collection
- **Full Name**: myorg.custom_collection

## Development Setup

### 1. Activate Python Virtual Environment

```bash
source ~/workspace/ansible/bin/activate
```

### 2. Install Dependencies

```bash
# Install collection dependencies
ansible-galaxy collection install -r requirements.txt

# Install Python testing dependencies
pip install -r test-requirements.txt
```

### 3. Install Collection Locally

```bash
# Install in development mode
ansible-galaxy collection install . --force
```

## Testing with Molecule

### Running Molecule Tests

```bash
# Navigate to role directory
cd roles/run

# Run full test sequence
molecule test

# Or run step-by-step:
molecule create      # Create test environment
molecule converge    # Run the role
molecule verify      # Run verification tests
molecule destroy     # Clean up
```

### Adding New Molecule Scenarios

```bash
# Navigate to role directory
cd roles/run

# Create a new scenario
molecule init scenario centos
```

## Linting

```bash
# Ansible lint
ansible-lint

# YAML lint
yamllint .
```

## Building the Collection

```bash
# Build collection tarball
ansible-galaxy collection build

# Result: myorg-custom_collection-X.Y.Z.tar.gz
```

## CI/CD Integration

This collection is part of the Cloud-Native Ansible Lifecycle platform:
- **PR Validation**: ansible-lint + molecule tests
- **Atomic Promotion**: Version-locked in release manifest
- **EE Building**: Bundled into custom Execution Environment

## Links

### Related Repositories
- **Cluster Config** (Platform GitOps): https://github.com/djdanielsson/rh1-cluster-config
- **AAP Config as Code**: https://github.com/djdanielsson/rh1-aap-config-as-code
- **Execution Environment**: https://github.com/djdanielsson/rh1-custom-ee
- **Release Manifests**: https://github.com/djdanielsson/rh1-release-manifest

### Documentation
- **Project Workspace**: https://github.com/djdanielsson/rh1_ansible_code_lifecycle
- **Platform Specs**: https://github.com/djdanielsson/rh1_ansible_code_lifecycle/tree/main/specs/001-cloud-native-ansible-lifecycle
- **Molecule Docs**: https://molecule.readthedocs.io/
- **Ansible-Lint**: https://ansible-lint.readthedocs.io/

---

**Last Updated**: 2025-10-29
**Maintained By**: Platform Team

