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

- **Platform Docs**: ../specs/001-cloud-native-ansible-lifecycle/
- **AAP Config**: ../aap-config-as-code/
- **Cluster Config**: ../cluster-config/

---

**Last Updated**: 2025-10-29
**Maintained By**: Platform Team

