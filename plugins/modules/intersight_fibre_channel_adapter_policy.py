#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: intersight_fibre_channel_adapter_policy
short_description: Fibre Channel Adapter policy configuration for Cisco Intersight
description:
  - Fibre Channel Adapter policy configuration for Cisco Intersight.
  - Used to configure Fibre Channel Adapter Policy on Cisco Intersight managed devices.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
    type: str
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    default: default
    type: str
  name:
    description:
      - The name assigned to the Fibre Channel Adapter policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements : dict
  description:
    description:
      - The user-defined description of the Boot Order policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  error_detection_timeout:
    description:
      -  Error Detection Timeout, also referred to as EDTOV, is the number of milliseconds to wait before the system assumes that an error has occurred.
    default: 2000
    type: int
  error_recovery_settings:
    description:
      -  Fibre Channel Error Recovery Settings.
    type: list
    elements: dict
    suboptions:
      enabled:
        description:
          -  Enables Fibre Channel Error recovery.
        type: bool
      io_retry_count:
        description:
          -  The number of times an I/O request to a port is retried because the port is busy before the system decides the port is unavailable.
        default: 8
        type: int
      io_retry_timeout:
        description:
          -  The number of seconds the adapter waits before aborting the pending command and resending the same IO request.
        default: 5
        type: int
      link_down_timeout:
        description:
          -  The number of milliseconds the port should actually be down before it is marked down and fabric connectivity is lost.
        default: 30000
        type: int
      port_down_timeout:
        description:
          -  The number of milliseconds a remote Fibre Channel port should be offline before informing the SCSI upper layer that the port is unavailable.
          -  For a server with a VIC adapter running ESXi, the recommended value is 10000. For a server with a port used to boot a Windows OS from the SAN,
          -  the recommended value is 5000 milliseconds.
        default: 10000
        type: int
  flogi_settings:
    description:
      -  Fibre Channel Flogi Settings.
    type: list
    elements: dict
    suboptions:
      retries:
        description:
          -  The number of times that the system tries to log in to the fabric after the first failure. Allowed range is 0-4294967295.
        default: 8
        type: int
      timeout:
        description:
          -  The number of milliseconds that the system waits before it tries to log in again.
        default: 4000
        type: int
  interrupt_settings:
    description:
      -  Interrupt Settings for the virtual fibre channel interface.
    type: list
    elements: dict
    suboptions:
      mode:
        description:
          - 'The preferred driver interrupt mode. This can be one of the following:- MSIx - Message Signaled Interrupts (MSI) with the optional extension.
          -  MSI  - MSI only. INTx - PCI INTx interrupts. MSIx is the recommended option.'
          -  MSIx - Message Signaled Interrupt (MSI) mechanism with the optional extension (MSIx). MSIx is the recommended and default option.
          -  MSI - Message Signaled Interrupt (MSI) mechanism that treats messages as interrupts.
          -  INTx - Line-based interrupt (INTx) mechanism similar to the one used in Legacy systems.
        choices: ['MSIx' , 'MSI' , 'INTx']
        default: MSIx
        type: str
  io_throttle_count:
    description:
      -  The maximum number of data or control I/O operations that can be pending for the virtual interface at one time. If this value is exceeded,
      -  the additional I/O operations wait in the queue until the number of pending I/O operations decreases and the additional operations can be processed.
    default: 512
    type: int
  lun_count:
    description:
      -  The maximum number of LUNs that the Fibre Channel driver will export or show. The maximum number of LUNs is usually controlled by the operating system
      -  running on the server. Lun Count value can exceed 1024 only for vHBA of type 'FC Initiator' and on servers having supported firmware version.
    default: 1024
    type: int
  lun_queue_depth:
    description:
      -  The number of commands that the HBA can send and receive in a single transmission per LUN.
    default: 20
    type: int
  plogi_settings:
    description:
      -  Fibre Channel Plogi Settings.
    type: list
    elements: dict
    suboptions:
      retries:
        description:
          -  The number of times that the system tries to log in to a port after the first failure.
        default: 8
        type: int
      timeout:
        description:
          -  The number of milliseconds that the system waits before it tries to log in again.
        default: 20000
        type: int
  resource_allocation_timeout:
    description:
      -  Resource Allocation Timeout, also referred to as RATOV, is the number of milliseconds to wait before the system assumes that a resource cannot be
      -  properly allocated.
    default: 10000
    type: int
  rx_queue_settings:
    description:
      -  Fibre Channel Receive Queue Settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          -  The number of queue resources to allocate.
        default: 1
        type: int
      ring_size:
        description:
          -  The number of descriptors in each queue. The maximum value for Transmit queue is 128 and for Receive queue is 2048.
        default: 64
        type: int
  scsi_queue_settings:
    description:
      -  SCSI Input/Output Queue Settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          -  The number of SCSI I/O queue resources the system should allocate.
        default: 1
        type: int
      ring_size:
        description:
          -  The number of descriptors in each SCSI I/O queue.
        default: 512
        type: int
  tx_queue_settings:
    description:
      -  Fibre Channel Transmit Queue Settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          -  The number of queue resources to allocate.
        default: 1
        type: int
      ring_size:
        description:
          -  The number of descriptors in each queue. The maximum value for Transmit queue is 128 and for Receive queue is 2048.
        default: 64
        type: int
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Fibre Channel Adapter Policy
  cisco.intersight.intersight_fibre_channel_adapter_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FCAP
    description: fabric channel adapter policy for COS
    tags:
      - Key: Site
        Value: RCDN
    error_detection_timeout: 1000
    error_recovery_settings:
      enabled: True

- name: Delete Fibre Channel Adapter Policy
  cisco.intersight.intersight_fibre_channel_adapter_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FCAP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-FCAP",
        "ObjectType": "vnic.FcAdapterPolicy",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        if params[prop_key]:
            api_body[prop] = params[prop_key]


def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for item in params[prop_key]:
                for key in item.keys():
                    if item[key]:
                        api_body[prop][to_camel_case(key)] = item[key]


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    error_recovery_settings_spec = {
        "enabled": {
            "type": "bool",
        },
        "io_retry_count": {
            "type": "int",
            "default": 8
        },
        "io_retry_timeout": {
            "type": "int",
            "default": 5
        },
        "link_down_timeout": {
            "type": "int",
            "default": 30000
        },
        "port_down_timeout": {
            "type": "int",
            "default": 10000
        },
    }
    flogi_settings_spec = {
        "retries": {
            "type": "int",
            "default": 8
        },
        "timeout": {
            "type": "int",
            "default": 4000
        },
    }
    interrupt_settings_spec = {
        "mode": {
            "type": "str",
            "choices": [
                'MSIx',
                'MSI',
                'INTx'
            ],
            "default": "MSIx"
        },
    }
    plogi_settings_spec = {
        "retries": {
            "type": "int",
            "default": 8
        },
        "timeout": {
            "type": "int",
            "default": 20000
        },
    }
    rx_queue_settings_spec = {
        "count": {
            "type": "int",
            "default": 1
        },
        "ring_size": {
            "type": "int",
            "default": 64
        },
    }
    scsi_queue_settings_spec = {
        "count": {
            "type": "int",
            "default": 1
        },
        "ring_size": {
            "type": "int",
            "default": 512
        },
    }
    tx_queue_settings_spec = {
        "count": {
            "type": "int",
            "default": 1
        },
        "ring_size": {
            "type": "int",
            "default": 64
        },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        error_detection_timeout={
            "type": "int",
            "default": 2000
        },
        error_recovery_settings={
            "type": "list",
            "options": error_recovery_settings_spec,
            "elements": "dict",
        },
        flogi_settings={
            "type": "list",
            "options": flogi_settings_spec,
            "elements": "dict",
        },
        interrupt_settings={
            "type": "list",
            "options": interrupt_settings_spec,
            "elements": "dict",
        },
        io_throttle_count={
            "type": "int",
            "default": 512
        },
        lun_count={
            "type": "int",
            "default": 1024
        },
        lun_queue_depth={
            "type": "int",
            "default": 20
        },
        plogi_settings={
            "type": "list",
            "options": plogi_settings_spec,
            "elements": "dict",
        },
        resource_allocation_timeout={
            "type": "int",
            "default": 10000
        },
        rx_queue_settings={
            "type": "list",
            "options": rx_queue_settings_spec,
            "elements": "dict",
        },
        scsi_queue_settings={
            "type": "list",
            "options": scsi_queue_settings_spec,
            "elements": "dict",
        },
        tx_queue_settings={
            "type": "list",
            "options": tx_queue_settings_spec,
            "elements": "dict",
        },
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/vnic/FcAdapterPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('ErrorDetectionTimeout', 'error_detection_timeout', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('ErrorRecoverySettings', 'error_recovery_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('FlogiSettings', 'flogi_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('InterruptSettings', 'interrupt_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('IoThrottleCount', 'io_throttle_count', intersight.module.params, intersight.api_body)
    check_and_add_prop('LunCount', 'lun_count', intersight.module.params, intersight.api_body)
    check_and_add_prop('LunQueueDepth', 'lun_queue_depth', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('PlogiSettings', 'plogi_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('ResourceAllocationTimeout', 'resource_allocation_timeout', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('RxQueueSettings', 'rx_queue_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('ScsiQueueSettings', 'scsi_queue_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('TxQueueSettings', 'tx_queue_settings', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
