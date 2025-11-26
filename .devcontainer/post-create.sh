#!/bin/bash
# Post-create script for automation-collection-example development container
# This script runs after the container is created

set -e

echo "🚀 Setting up Ansible Collection development environment..."

# Install/upgrade development tools
echo "📦 Installing development tools..."

# Ensure pip is up to date
pip install --upgrade pip

# Install Ansible and development tools
pip install \
    ansible-core>=2.15 \
    ansible-lint \
    ansible-creator \
    ansible-navigator \
    ansible-builder \
    yamllint \
    jinja2-cli \
    pre-commit \
    detect-secrets \
    molecule \
    'molecule-plugins[docker]' \
    pytest \
    pytest-ansible \
    pytest-cov \
    pytest-mock \
    black \
    isort \
    flake8 \
    pylint \
    bandit \
    mypy \
    tox \
    sphinx \
    sphinx-rtd-theme \
    antsibull-docs

# Install collection dependencies if requirements.yml exists
if [ -f requirements.yml ]; then
    echo "📚 Installing collection dependencies..."
    ansible-galaxy collection install -r requirements.yml --force
fi

# Install Python dependencies if they exist
if [ -f requirements.txt ]; then
    echo "📦 Installing Python requirements..."
    pip install -r requirements.txt
fi

if [ -f test-requirements.txt ]; then
    echo "📦 Installing test requirements..."
    pip install -r test-requirements.txt
fi

# Install yq (YAML processor)
VERSION=v4.40.5
BINARY=yq_linux_amd64
wget -q https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY} -O /tmp/yq
mv /tmp/yq /usr/local/bin/yq
chmod +x /usr/local/bin/yq

# Setup pre-commit
if [ -f .pre-commit-config.yaml ]; then
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
    pre-commit install --hook-type commit-msg
fi

# Git configuration
echo "⚙️  Configuring Git..."
git config --global --add safe.directory /workspace

# Create helpful aliases
echo "📝 Setting up shell aliases..."
cat >> ~/.bashrc <<'EOF'

# Ansible Collection Aliases
alias ansible-creator='ansible-creator'
alias ac-init='ansible-creator init'
alias ac-add='ansible-creator add'

# Testing Aliases
alias test-sanity='ansible-test sanity --docker'
alias test-units='ansible-test units --docker'
alias test-integration='ansible-test integration --docker'
alias test-all='pytest tests/ -v --cov=plugins --cov-report=html --cov-report=term'
alias molecule-test='molecule test'
alias molecule-converge='molecule converge'

# Linting Aliases
alias lint-all='yamllint . && ansible-lint && flake8 plugins/ && pylint plugins/'
alias format-python='black plugins/ tests/ && isort plugins/ tests/'
alias security-scan='bandit -r plugins/'

# Build Aliases
alias build-collection='ansible-galaxy collection build --force'
alias build-docs='sphinx-build -b html docs/ docs/_build/html'

# Git Aliases
alias gs='git status'
alias gp='git pull'
alias gc='git commit'
alias gco='git checkout'

# Development Helpers
alias check-docs='antsibull-docs lint-collection-docs .'
alias validate-meta='ansible-galaxy collection verify . --ignore-certs'
EOF

source ~/.bashrc

# Create ansible.cfg if it doesn't exist
if [ ! -f ansible.cfg ]; then
    echo "📝 Creating ansible.cfg..."
    cat > ansible.cfg <<'EOF'
[defaults]
collections_path = ./
stdout_callback = yaml
bin_ansible_callbacks = True
host_key_checking = False

[inventory]
enable_plugins = yaml, ini
EOF
fi

# Build the collection for local testing
if [ -f galaxy.yml ]; then
    echo "🔨 Building collection..."
    ansible-galaxy collection build --force --output-path ./ > /dev/null 2>&1 || true

    # Extract namespace and name from galaxy.yml
    NAMESPACE=$(yq eval '.namespace' galaxy.yml)
    NAME=$(yq eval '.name' galaxy.yml)
    VERSION=$(yq eval '.version' galaxy.yml)

    if [ -f "${NAMESPACE}-${NAME}-${VERSION}.tar.gz" ]; then
        echo "📦 Installing collection locally..."
        ansible-galaxy collection install "${NAMESPACE}-${NAME}-${VERSION}.tar.gz" --force
    fi
fi

echo "✅ Ansible Collection development environment ready!"
echo ""
echo "Available commands:"
echo "  - ansible-creator: Create/manage collection content"
echo "  - ansible-test: Run sanity, units, integration tests"
echo "  - molecule: Test roles with Molecule"
echo "  - pytest: Run Python unit tests"
echo "  - black, isort, flake8, pylint: Python code quality"
echo "  - bandit: Security scanning"
echo ""
echo "Quick commands:"
echo "  - lint-all: Run all linters"
echo "  - format-python: Auto-format Python code"
echo "  - test-all: Run all pytest tests with coverage"
echo "  - build-collection: Build collection tarball"
echo ""
echo "Collection structure:"
if [ -f galaxy.yml ]; then
    echo "  Namespace: $(yq eval '.namespace' galaxy.yml)"
    echo "  Name: $(yq eval '.name' galaxy.yml)"
    echo "  Version: $(yq eval '.version' galaxy.yml)"
fi

