#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Platform Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: manage_service
short_description: Manages system services with advanced options
version_added: "1.0.0"
description:
    - This module manages system services with additional checks and options
    - Provides idempotent service management with verification
    - Supports systemd-based systems
options:
    name:
        description:
            - Name of the service to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the service
        choices: ['started', 'stopped', 'restarted', 'reloaded']
        default: started
        type: str
    enabled:
        description:
            - Whether the service should start on boot
        type: bool
        default: null
    verify:
        description:
            - Verify service is actually running after start
        type: bool
        default: true
    timeout:
        description:
            - Timeout in seconds for service operations
        type: int
        default: 60
author:
    - David Danielsson (@djdanielsson)
    - David Igou (@david-igou)
    - Jeff Pullen (@jeffcpullen)
    - Vinny Valdez (@vvaldez)
'''

EXAMPLES = r'''
# Start and enable a service
- name: Ensure nginx is running
  myorg.custom_collection.manage_service:
    name: nginx
    state: started
    enabled: true

# Stop a service
- name: Stop apache
  myorg.custom_collection.manage_service:
    name: httpd
    state: stopped

# Restart with verification disabled
- name: Restart database
  myorg.custom_collection.manage_service:
    name: postgresql
    state: restarted
    verify: false
...
'''

RETURN = r'''
name:
    description: Name of the service managed
    type: str
    returned: always
    sample: nginx
state:
    description: Current state of the service
    type: str
    returned: always
    sample: started
enabled:
    description: Whether service is enabled on boot
    type: bool
    returned: when enabled parameter is set
    sample: true
changed:
    description: Whether any change was made
    type: bool
    returned: always
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import time


def is_service_running(name):
    """Check if service is running"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', name],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip() == 'active'
    except Exception:
        return False


def is_service_enabled(name):
    """Check if service is enabled"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-enabled', name],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip() == 'enabled'
    except Exception:
        return False


def manage_service_state(module, name, state, verify, timeout):
    """Manage service state"""
    changed = False
    current_state = 'started' if is_service_running(name) else 'stopped'

    if state == 'started' and current_state == 'stopped':
        try:
            subprocess.run(
                ['systemctl', 'start', name],
                check=True,
                timeout=timeout
            )
            changed = True

            if verify:
                # Wait for service to be active
                start_time = time.time()
                while time.time() - start_time < timeout:
                    if is_service_running(name):
                        break
                    time.sleep(1)
                else:
                    module.fail_json(msg=f"Service {name} did not start within {timeout} seconds")

        except subprocess.TimeoutExpired:
            module.fail_json(msg=f"Timeout starting service {name}")
        except subprocess.CalledProcessError as e:
            module.fail_json(msg=f"Failed to start service {name}: {e}")

    elif state == 'stopped' and current_state == 'started':
        try:
            subprocess.run(['systemctl', 'stop', name], check=True, timeout=timeout)
            changed = True
        except Exception as e:
            module.fail_json(msg=f"Failed to stop service {name}: {e}")

    elif state in ['restarted', 'reloaded']:
        action = 'restart' if state == 'restarted' else 'reload'
        try:
            subprocess.run(['systemctl', action, name], check=True, timeout=timeout)
            changed = True
        except Exception as e:
            module.fail_json(msg=f"Failed to {action} service {name}: {e}")

    return changed, 'started' if is_service_running(name) else 'stopped'


def manage_service_enabled(module, name, enabled):
    """Manage service enabled state"""
    changed = False
    current_enabled = is_service_enabled(name)

    if enabled is not None and enabled != current_enabled:
        action = 'enable' if enabled else 'disable'
        try:
            subprocess.run(['systemctl', action, name], check=True)
            changed = True
        except Exception as e:
            module.fail_json(msg=f"Failed to {action} service {name}: {e}")

    return changed


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', default='started', choices=['started', 'stopped', 'restarted', 'reloaded']),
        enabled=dict(type='bool', default=None),
        verify=dict(type='bool', default=True),
        timeout=dict(type='int', default=60),
    )

    result = dict(
        changed=False,
        name='',
        state='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    name = module.params['name']
    state = module.params['state']
    enabled = module.params['enabled']
    verify = module.params['verify']
    timeout = module.params['timeout']

    if module.check_mode:
        module.exit_json(**result)

    # Manage state
    state_changed, final_state = manage_service_state(module, name, state, verify, timeout)

    # Manage enabled
    enabled_changed = manage_service_enabled(module, name, enabled)

    result['changed'] = state_changed or enabled_changed
    result['name'] = name
    result['state'] = final_state

    if enabled is not None:
        result['enabled'] = is_service_enabled(name)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
