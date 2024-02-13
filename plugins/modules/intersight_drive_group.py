#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from pytest import console_main
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: intersight_drive_group
short_description: Drive Group Policy configuration for Cisco Intersight
description:
  - Drive Group configuration for Cisco Intersight.
  - Used to configure Drive Group on Cisco Intersight managed devices.
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
  name:
    description:
      - 'The name of the drive group. The name can be between 1 and 64 alphanumeric characters.'
      - 'Spaces or any special characters other than - (hyphen), _ (underscore), : (colon), and . (period) are not allowed.'
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements : dict
  # automatic_drive_group:
  #   description:
  #     -  This drive group is created using automatic drive selection.
  #   type: list
  #   elements: dict
  #   suboptions:
  #     drive_type:
  #       description:
  #         -  Type of drive that should be used for this RAID group.
  #         -  Any - Any type of drive can be used for virtual drive creation.
  #         -  HDD - Hard disk drives should be used for virtual drive creation.
  #         -  SSD - Solid state drives should be used for virtual drive creation.
  #       choices: ['Any' , 'HDD' , 'SSD']
  #       default: Any
  #       type: str
  #     drives_per_span:
  #       description:
  #         -  Number of drives within this span group. The minimum number of disks needed in a span group varies based on RAID level. RAID0 requires at least one disk. RAID1 and RAID10 requires at least 2 and in multiples of . RAID5 and RAID50 require at least 3 disks in a span group. RAID6 and RAID60 require atleast 4 disks in a span.
  #       default: 1
  #       type: int
  #     minimum_drive_size:
  #       description:
  #         -  Minimum size of the drive to be used for creating this RAID group.
  #       type: int
  #     num_dedicated_hot_spares:
  #       description:
  #         -  Number of dedicated hot spare disks for this RAID group. Allowed value is a comma or hyphen separated number range.
  #       type: str
  #     number_of_spans:
  #       description:
  #         -  Number of span groups to be created for this RAID group. Non-nested RAID levels have a single span.
  #       default: 0
  #       type: int
  #     use_remaining_drives:
  #       description:
  #         -  This flag enables the drive group to use all the remaining drives on the server.
  #       type: bool
  manual_drive_group:
    description:
      -  This drive group is created by specifying the drive slots to be used.
    type: list
    elements: dict
    suboptions:
      dedicated_hot_spares:
        description:
          -  A collection of drives to be used as hot spares for this Drive Group.
        type: str
      span_groups:
        description:
          -  Enter list of Disk IDs separated by comma or hypen. Sample format is 1, 3 or 4-6, 8. Non spanned RAID levels like RAID0, RAID1, RAID5 and RAID6 expect a single group of disks whereas spanned RAID levels need multiple groups of disks with each group representing a span group. Non spanned RAID levels expect one span group and spanned RAID levels accept minimum 2 span groups and up to 8.
        type: list
        elements: dict
        suboptions:
          slots:
            description:
              -  Collection of local disks that are part of this span group. Allowed value is a comma or hyphen separated number range. The minimum number of disks needed in a span group varies based on RAID level. RAID0 requires at least one disk, RAID1 and RAID10 requires at least 2 and in multiples of 2, RAID5 RAID50 RAID6 and RAID60 require at least 3 disks in a span group.
            type: str
            type: list
  raid_level:
    description:
      -  The supported RAID level for the disk group.
      -  Raid0 - RAID 0 Stripe Raid Level.
      -  Raid1 - RAID 1 Mirror Raid Level.
      -  Raid5 - RAID 5 Mirror Raid Level.
      -  Raid6 - RAID 6 Mirror Raid Level.
      -  Raid10 - RAID 10 Mirror Raid Level.
      -  Raid50 - RAID 50 Mirror Raid Level.
      -  Raid60 - RAID 60 Mirror Raid Level.
    choices: ['Raid0' , 'Raid1' , 'Raid5' , 'Raid6' , 'Raid10' , 'Raid50' , 'Raid60']
    default: Raid0
    type: str
  secure_drive_group:
    description:
      -  Enables/disables the drive encryption on all the drives used in this policy. This flag just enables the drive security and only after remote key setting configured, the actual encryption will be done.
    type: bool
  # type:
  #   description:
  #     -  type of drive selection to be used for this drive group.
  #     -  0 - Drives are selected manually by the user.
  #     -  1 - Drives are selected automatically based on the RAID and virtual drive configuration.
  #   choices: [0 , 1]
  #   default: 0
  #   type: int
  virtual_drives:
    description:
      -  The list of virtual drives and the disk groups that need to be created through this policy.
    type: list
    elements: dict
    suboptions:
      boot_drive:
        description:
          -  This flag enables this virtual drive to be used as a boot drive.
        type: bool
      expand_to_available:
        description:
          -  This flag enables the virtual drive to use all the space available in the disk group. When this flag is enabled, the size property is ignored.
        type: bool
      name:
        description:
          - 'The name of the virtual drive. The name can be between 1 and 15 alphanumeric characters. Spaces or any special characters other than - (hyphen), _ (underscore), : (colon), and . (period) are not allowed.'
        type: str
      size:
        description:
          -  Virtual drive size in MebiBytes. size is mandatory field except when the Expand to Available option is enabled.
        type: int
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
        type: list
  storage_policy:
    description:
      -  A reference to a storagestorage_policy resource.
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Storage Policy
  cisco.intersight.intersight_drive_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: COS-DG1
    tags:
      - Key: Site
        Value: RCDN
    manual_drive_group:
      span_groups:
        - slots: "1,3,4-6"
    raid_level: Raid0
    secure_drive_group: true
    storage_policy: COS-SP
    virtual_drives:
      - boot_drive: true
        name: VG1
        size: 256
        virtual_drive_policy:
          access_policy: Default
          drive_cache: Enable
          read_policy: ReadAhead
          strip_size: 64
          write_policy: Default

- name: Delete Drive Group
  cisco.intersight.intersight_drive_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-DG1
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-DG1",
        "ObjectType": "storage.DriveGroup",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, intersight_argument_spec, compare_values


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        if params[prop_key]:
            api_body[prop] = params[prop_key]


def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for key in params[prop_key].keys():
                if params[prop_key][key] and isinstance(params[prop_key][key], list):                    
                    item_array = []
                    for element in params[prop_key][key]:
                        insert_array_elements(item_array, element)
                    api_body[prop][to_camel_case(key)] = item_array            
                elif params[prop_key][key]:
                    api_body[prop][to_camel_case(key)] = params[prop_key][key]

def insert_array_elements(item_array, element):
    if element and isinstance(element, dict):
        item_dict = {}
        for element_key in element.keys():
            if element[element_key]:
                item_dict[to_camel_case(element_key)] = element[element_key]
        item_array.append(item_dict)
    elif element:
        item_array.append(element)

def check_and_add_prop_dict_array(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = []
        if params[prop_key] :
            for item in params[prop_key]:
                item_dict = {}
                for key in item.keys():
                    if item[key] and isinstance(item[key], dict):
                        item_dict[to_camel_case(key)] = {}
                        for element in item[key].keys():
                          item_dict[to_camel_case(key)][to_camel_case(element)] = item[key][element]
                    elif item[key]:
                          item_dict[to_camel_case(key)] = item[key]
                api_body[prop].append(item_dict)
    
def check_and_add_prop_policy(prop, prop_key, params, api_body):
    api_body[prop] = {}
    for key in params.keys():
        if params[key]:
            api_body[prop][key] = params[key]

def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def get_policy_ref(intersight, policy_name, resource_path):
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    moid = None
    query = str.format("Name eq '{policy}'", policy=policy_name)
    intersight.get_resource(resource_path=resource_path, query_params={"$filter": query})
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        moid = intersight.result['api_response']['Moid']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    return {"Moid": moid}



def main():
    span_groups_spec = {
      "slots": {
            "type": "str",
        },
    }

    manual_drive_group_spec = {
      "dedicated_hot_spares": {
            "type": "str",
            "default": ""
        },
        "span_groups": {
            "type": "list",
            "options": span_groups_spec,
            "elements": "dict",
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
  
    virtual_drives_spec = {
      "boot_drive": {
            "type": "bool",
        },
      "expand_to_available": {
            "type": "bool",
        },
      "name": {
            "type": "str",
        },
      "size": {
            "type": "int",
        },
        "virtual_drive_policy": {
            "type": "dict",
            "options": virtual_drive_policy_spec,
        },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        name={"type": "str", "required": True},
        tags={"type": "list", "elements": "dict"},
        manual_drive_group={
            "type": "dict",
            "options": manual_drive_group_spec,            
        },
        raid_level={
            "type": "str",
            "choices": [
                'Raid0',
                'Raid1',
                'Raid5',
                'Raid6',
                'Raid10',
                'Raid50',
                'Raid60'
            ],
            "default": "Raid0"
        },
        secure_drive_group={
            "type": "bool",
        },
        virtual_drives={
            "type": "list",
            "options": virtual_drives_spec,
            "elements": "dict",
        },
        storage_policy={
            "type": "str",
            "default": ""
        },
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # get the storage policy reference
    storage_policy = get_policy_ref(intersight, intersight.module.params['storage_policy'], '/storage/StoragePolicies')
    if not storage_policy['Moid']:
        module.fail_json(msg="Storage Policy not found")
    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/storage/DriveGroups'
    # Define API body used in compares or create
    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
    }
    check_and_add_prop_dict('ManualDriveGroup', 'manual_drive_group', intersight.module.params, intersight.api_body)
    check_and_add_prop('RaidLevel', 'raid_level', intersight.module.params, intersight.api_body)
    check_and_add_prop('SecureDriveGroup', 'secure_drive_group', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict_array('VirtualDrives', 'virtual_drives', intersight.module.params, intersight.api_body)
    check_and_add_prop_policy('StoragePolicy', 'storage_policy', storage_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "Name eq '" + intersight.module.params['name'] + "'"
    filter_str += "and Parent.Moid eq '" + storage_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )

    check_and_add_resource(intersight, resource_path)

    module.exit_json(**intersight.result)

def check_and_add_resource(intersight, resource_path):
    dg_moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        dg_moid = intersight.result['api_response']['Moid']
        if intersight.module.params['state'] == 'present':
            resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present' and not resource_values_match:
        intersight.configure_resource(moid=dg_moid, resource_path=resource_path, body=intersight.api_body, query_params=None)
    elif intersight.module.params['state'] == 'absent':
        intersight.delete_resource(moid=dg_moid, resource_path=resource_path)
        dg_moid = None


if __name__ == '__main__':
    main()
