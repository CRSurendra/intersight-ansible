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
module: intersight_storage_policy
short_description: Storage Policy configuration for Cisco Intersight
description:
  - Storage Policy configuration for Cisco Intersight.
  - Used to configure Storage Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Storage policy.
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
      - The user-defined description of the Storage policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  default_drive_mode:
    description:
      -  All unconfigured drives (non-user configured drives) will move to the selected state on deployment. Newly inserted drives will move to the selected state. Select Unconfigured Good option to retain the existing configuration. Select JBOD to move the unconfigured drives to JBOD state. Select RAID0 to create a RAID0 virtual drive on each of the unconfigured drives. If JBOD is selected, unconfigured drives will move to JBOD state on host reboot. This setting is applicable only to selected set of controllers on FI attached servers.
      -  UnconfiguredGood - Newly inserted drives or on reboot, drives will remain the same state.
      -  Jbod - Newly inserted drives or on reboot, drives will automatically move to JBOD state if drive state was UnconfiguredGood.
      -  RAID0 - Newly inserted drives or on reboot, virtual drives will be created, respective drives will move to Online state.
    choices: ['UnconfiguredGood' , 'Jbod' , 'RAID0']
    default: UnconfiguredGood
    type: str
  global_hot_spares:
    description:
      -  A collection of disks that is to be used as hot spares, globally, for all the RAID groups. Allowed value is a number range separated by a comma or a hyphen.
    type: str
  m2_virtual_drive:
    description:
      -  Virtual Drive configuration for M.2 RAID controller.
    type: list
    elements: dict
    suboptions:
      controller_slot:
        description:
          -  Select the M.2 RAID controller slot on which the virtual drive is to be created. Select 'MSTOR-RAID-1' to create virtual drive on the M.2 RAID controller in the first slot or in the MSTOR-RAID slot, 'MSTOR-RAID-2' for second slot, 'MSTOR-RAID-1, MSTOR-RAID-2' for both slots or either slot.
          -  MSTOR-RAID-1 - Virtual drive  will be created on the M.2 RAID controller in the first slot.
          -  MSTOR-RAID-2 - Virtual drive  will be created on the M.2 RAID controller in the second slot, if available.
          -  MSTOR-RAID-1,MSTOR-RAID-2 - Virtual drive  will be created on the M.2 RAID controller in both the slots, if available.
        choices: ['MSTOR-RAID-1' , 'MSTOR-RAID-2' , 'MSTOR-RAID-1,MSTOR-RAID-2']
        default: MSTOR-RAID-1
        type: str
      enable:
        description:
          -  If enabled, this will create a virtual drive on the M.2 RAID controller.
        default: False
        type: bool
  raid0_drive:
    description:
      -  The list of disks where RAID0 virtual drives must be created on each individual drive.
    type: list
    elements: dict
    suboptions:
      drive_slots:
        description:
          -  The set of drive slots where RAID0 virtual drives must be created.
        type: str
      enable:
        description:
          -  If enabled, this will create a RAID0 virtual drive per disk and encompassing the whole disk.
        default: False
        type: bool
      virtual_drive_policy:
        description:
          -  This defines the characteristics of a specific virtual drive.
        type: list
        elements: dict
        suboptions:
          access_policy:
            description:
              -  Access policy that host has on this virtual drive.
              -  Default - Use platform default access mode.
              -  ReadWrite - Enables host to perform read-write on the VD.
              -  ReadOnly - Host can only read from the VD.
              -  Blocked - Host can neither read nor write to the VD.
            choices: ['Default' , 'ReadWrite' , 'ReadOnly' , 'Blocked']
            default: Default
            type: str
          drive_cache:
            description:
              -  Disk cache policy for the virtual drive.
              -  Default - Use platform default drive cache mode.
              -  NoChange - Drive cache policy is unchanged.
              -  Enable - Enables IO caching on the drive.
              -  Disable - Disables IO caching on the drive.
            choices: ['Default' , 'NoChange' , 'Enable' , 'Disable']
            default: Default
            type: str
          read_policy:
            description:
              -  Read ahead mode to be used to read data from this virtual drive.
              -  Default - Use platform default read ahead mode.
              -  ReadAhead - Use read ahead mode for the policy.
              -  NoReadAhead - Do not use read ahead mode for the policy.
            choices: ['Default' , 'ReadAhead' , 'NoReadAhead']
            default: Default
            type: str
          strip_size:
            description:
              -  Desired strip size - Allowed values are 64KiB, 128KiB, 256KiB, 512KiB, 1024KiB.
              -  64 - Number of bytes in a strip is 64 Kibibytes.
              -  128 - Number of bytes in a strip is 128 Kibibytes.
              -  256 - Number of bytes in a strip is 256 Kibibytes.
              -  512 - Number of bytes in a strip is 512 Kibibytes.
              -  1024 - Number of bytes in a strip is 1024 Kibibytes or 1 Mebibyte.
            choices: [64 , 128 , 256 , 512 , 1024]
            default: 64
            type: int
          write_policy:
            description:
              -  Write mode to be used to write data to this virtual drive.
              -  Default - Use platform default write mode.
              -  WriteThrough - Data is written through the cache and to the physical drives. Performance is improved, because subsequent reads of that data can be satisfied from the cache.
              -  WriteBackGoodBbu - Data is stored in the cache, and is only written to the physical drives when space in the cache is needed. Virtual drives requesting this policy fall back to Write Through caching when the battery backup unit (BBU) cannot guarantee the safety of the cache in the event of a power failure.
              -  AlwaysWriteBack - With this policy, write caching remains Write Back even if the battery backup unit is defective or discharged.
            choices: ['Default' , 'WriteThrough' , 'WriteBackGoodBbu' , 'AlwaysWriteBack']
            default: Default
            type: str
  secure_jbods:
    description:
      -  JBOD drives specified in this slot range will be encrypted. Allowed value is a comma or hyphen separated number range. Sample format is 1, 3 or 4-6, 8.
    type: str
  unused_disks_state:
    description:
      -  State to which drives, not used in this policy, are to be moved. NoChange will not change the drive state. No Change must be selected if Default Drive State is set to JBOD or RAID0.
      -  NoChange - Drive state will not be modified by Storage Policy.
      -  UnconfiguredGood - Unconfigured good state -ready to be added in a RAID group.
      -  Jbod - JBOD state where the disks start showing up to Host OS.
    choices: ['NoChange' , 'UnconfiguredGood' , 'Jbod']
    default: NoChange
    type: str
  use_jbod_for_vd_creation:
    description:
      -  Disks in JBOD State are used to create virtual drives. This setting must be disabled if Default Drive State is set to JBOD.
    type: bool
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Storage Policy
  cisco.intersight.intersight_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-SP
    description: Storage Policy for COS
    tags:
      - Key: Site
        Value: RCDN
    use_jbod_for_vd_creation: True
    m2_virtual_drive:
      - controller_slot: MSTOR-RAID-1
        enable: True      


- name: Delete Storage Policy
  cisco.intersight.intersight_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-SP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-EP",
        "ObjectType": "storage.StoragePolicy",
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
                    if item[key] and isinstance(item[key], list):
                        api_body[prop][to_camel_case(key)] = {}
                        for element in item[key]:
                            for sub_key in element.keys():
                                api_body[prop][to_camel_case(key)][to_camel_case(sub_key)] = element[sub_key]
                    elif item[key]:
                        api_body[prop][to_camel_case(key)] = item[key]
    


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    m2_virtual_drive_spec = {
      "controller_slot":{
            "type": "str",
            "choices": [
                'MSTOR-RAID-1',
                'MSTOR-RAID-2',
                'MSTOR-RAID-1,MSTOR-RAID-2'
            ],
            "default": "MSTOR-RAID-1"
        },
      "enable": {
            "type": "bool",
            "default": False
        },
    }
    virtual_drive_policy_spec = {
      "access_policy":{
            "type": "str",
            "choices": [
                'Default',
                'ReadWrite',
                'ReadOnly',
                'Blocked'
            ],
            "default": "Default"
        },
      "drive_cache":{
            "type": "str",
            "choices": [
                'Default',
                'NoChange',
                'Enable',
                'Disable'
            ],
            "default": "Default"
        },
      "read_policy":{
            "type": "str",
            "choices": [
                'Default',
                'ReadAhead',
                'NoReadAhead'
            ],
            "default": "Default"
        },
      "strip_size":{
            "type": "int",
            "choices": [
                64,
                128,
                256,
                512,
                1024
            ],
            "default": 64
        },
      "write_policy":{
            "type": "str",
            "choices": [
                'Default',
                'WriteThrough',
                'WriteBackGoodBbu',
                'AlwaysWriteBack'
            ],
            "default": "Default"
        },
    }
    raid0_drive_spec = {
      "drive_slots": {
            "type": "str",
      },
      "enable": {
            "type": "bool",
            "default": False
        },
      "virtual_drive_policy": {
          "type": "list",
          "options": virtual_drive_policy_spec,
          "elements": "dict",
      },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        default_drive_mode={
            "type": "str",
            "choices": [
                'UnconfiguredGood',
                'Jbod',
                'RAID0'
            ],
            "default": "UnconfiguredGood"
        },
        global_hot_spares={
            "type": "str",
        },
        m2_virtual_drive={
            "type": "list",
            "options": m2_virtual_drive_spec,
            "elements": "dict",
        },
        raid0_drive={
            "type": "list",
            "options": raid0_drive_spec,
            "elements": "dict",
        },
        secure_jbods={
            "type": "str",
        },
        unused_disks_state={
            "type": "str",
            "choices": [
                'NoChange',
                'UnconfiguredGood',
                'Jbod'
            ],
            "default": "NoChange"
        },
        use_jbod_for_vd_creation={
            "type": "bool",
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
    resource_path = '/storage/StoragePolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('DefaultDriveMode', 'default_drive_mode', intersight.module.params, intersight.api_body)
    check_and_add_prop('GlobalHotSpares', 'global_hot_spares', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('M2VirtualDrive', 'm2_virtual_drive', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('Raid0Drive', 'raid0_drive', intersight.module.params, intersight.api_body)
    check_and_add_prop('SecureJbods', 'secure_jbods', intersight.module.params, intersight.api_body)
    check_and_add_prop('UnusedDisksState', 'unused_disks_state', intersight.module.params, intersight.api_body)
    check_and_add_prop('UseJbodForVdCreation', 'use_jbod_for_vd_creation', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
