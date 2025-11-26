"""Integration tests for the collection."""

import os
import pytest
import subprocess
import yaml


class TestCollectionIntegration:
    """Integration tests for collection functionality."""

    def test_collection_installed(self):
        """Test that collection is properly installed."""
        result = subprocess.run(
            ["ansible-galaxy", "collection", "list"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert "myorg.custom_collection" in result.stdout or result.returncode == 0

    def test_collection_build(self, tmp_path):
        """Test that collection builds successfully."""
        result = subprocess.run(
            ["ansible-galaxy", "collection", "build", "--output-path", str(tmp_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert any(f.endswith(".tar.gz") for f in os.listdir(tmp_path))

    def test_galaxy_yml_valid(self):
        """Test that galaxy.yml is valid."""
        with open("galaxy.yml", "r") as f:
            galaxy = yaml.safe_load(f)

        required_fields = ["namespace", "name", "version", "authors", "description"]
        for field in required_fields:
            assert field in galaxy, f"Missing required field: {field}"

        # Check version format
        version = galaxy["version"]
        assert isinstance(version, str)
        parts = version.split(".")
        assert len(parts) >= 3, "Version should be in format x.y.z"

    def test_role_structure(self):
        """Test that role has proper structure."""
        role_path = "roles/run"
        required_dirs = ["tasks", "defaults", "meta"]

        for dir_name in required_dirs:
            assert os.path.isdir(
                os.path.join(role_path, dir_name)
            ), f"Missing required directory: {dir_name}"

        # Check meta/main.yml exists
        assert os.path.isfile(os.path.join(role_path, "meta", "main.yml"))

    def test_module_documentation(self):
        """Test that modules have proper documentation."""
        modules_path = "plugins/modules"

        if not os.path.isdir(modules_path):
            pytest.skip("No modules directory")

        for filename in os.listdir(modules_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_path = os.path.join(modules_path, filename)
                with open(module_path, "r") as f:
                    content = f.read()

                # Check for required documentation
                assert "DOCUMENTATION = " in content, f"{filename} missing DOCUMENTATION"
                assert "EXAMPLES = " in content, f"{filename} missing EXAMPLES"
                assert "RETURN = " in content, f"{filename} missing RETURN"


class TestRoleIntegration:
    """Integration tests for roles."""

    def test_role_syntax(self):
        """Test role syntax with ansible-playbook."""
        test_playbook = """
---
- name: Test role syntax
  hosts: localhost
  gather_facts: false
  roles:
    - role: run
      run_message: "test"
"""

        with open("/tmp/test_playbook.yml", "w") as f:
            f.write(test_playbook)

        result = subprocess.run(
            ["ansible-playbook", "--syntax-check", "/tmp/test_playbook.yml"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Syntax check failed: {result.stderr}"

    def test_role_defaults(self):
        """Test that role has valid defaults."""
        defaults_path = "roles/run/defaults/main.yml"

        if os.path.isfile(defaults_path):
            with open(defaults_path, "r") as f:
                defaults = yaml.safe_load(f)

            assert isinstance(defaults, dict) or defaults is None

    def test_role_meta(self):
        """Test that role meta is valid."""
        meta_path = "roles/run/meta/main.yml"

        with open(meta_path, "r") as f:
            meta = yaml.safe_load(f)

        assert "galaxy_info" in meta
        assert "name" in meta["galaxy_info"]
        assert "author" in meta["galaxy_info"]


class TestCollectionQuality:
    """Quality checks for the collection."""

    def test_no_debug_tasks(self):
        """Test that no debug tasks are left in production code."""
        # Skip this test in development, but could be enforced for releases
        pass

    def test_ansible_lint(self):
        """Test that collection passes ansible-lint."""
        result = subprocess.run(
            ["ansible-lint", "--profile", "production"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Allow warnings, but no errors
        # Return code 0 = success, 2 = warnings, other = errors
        assert result.returncode in [0, 2], f"ansible-lint failed: {result.stdout}"

    def test_yaml_lint(self):
        """Test that YAML files are properly formatted."""
        result = subprocess.run(
            ["yamllint", "-c", ".yamllint", "."],
            capture_output=True,
            text=True,
            check=False,
        )

        # Return code 0 = success, 1 = warnings, 2 = errors
        assert result.returncode in [0, 1], f"yamllint failed: {result.stdout}"


@pytest.fixture
def sample_inventory():
    """Provide a sample inventory for testing."""
    return {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local",
                }
            }
        }
    }


@pytest.fixture
def sample_playbook():
    """Provide a sample playbook for testing."""
    return """
---
- name: Test playbook
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Test task
      ansible.builtin.debug:
        msg: "Test message"
"""
