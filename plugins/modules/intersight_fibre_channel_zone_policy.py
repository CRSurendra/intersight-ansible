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
module: intersight_fibre_channel_zone_policy
short_description: Fibre Channel Zone policy configuration for Cisco Intersight
description:
  - Fibre Channel Zone policy configuration for Cisco Intersight.
  - Used to configure Fibre Channel Zone Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Fibre Channel Zone policy.
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
  fc_target_members:
    description:
      -  List of target WWPN members that are part of the zone.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          -  name given to the target member.
        type: str
        default: ""
      switch_id:
        description:
          -  Unique identifier for the Fabric object.
          -  A - Switch Identifier of Fabric Interconnect A.
          -  B - Switch Identifier of Fabric Interconnect B.
        choices: ['A' , 'B']
        default: A
        type: str
      vsan_id:
        description:
          -  VSAN with scope defined as Storage in the VSAN policy.
        type: int
      wwpn:
        description:
          -  WWPN that is a member of the FC zone.
        type: str
        default: ""
  fc_target_zoning_type:
    description:
      -  Type of FC zoning. Allowed values are SIST, SIMT and None.
      -  SIST - The system automatically creates one zone for each vHBA and storage port pair. Each zone has two members.
      -  SIMT - The system automatically creates one zone for each vHBA. Configure this type of zoning if the number of zones created is likely to
      -  exceed the maximum supported number of zones.
      -  None - FC zoning is not configured.
    choices: ['SIST' , 'SIMT' , 'None']
    default: SIST
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Fibre Channel Zone Policy
  cisco.intersight.intersight_fibre_channel_zone_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FCZP
    description: Fibre Channel Zone policy for COS
    tags:
      - Key: Site
        Value: RCDN
    fc_target_zoning_type: SIST
    fc_target_members:
      - name: TEST1
        switch_id: A
        vsan_id: 1
        wwpn: 20:00:00:25:B5:FF:00:00

- name: Delete Fibre Channel Zone Policy
  cisco.intersight.intersight_fibre_channel_zone_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FCZP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-FCZP",
        "ObjectType": "fabric.FcZonePolicy",
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


def check_and_add_prop(prop, propKey, params, api_body):
    if propKey in params.keys():
        api_body[prop] = params[propKey]


def check_and_add_prop_dict_array(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = []
        if params[prop_key] :
            for item in params[prop_key]:
                item_dict = {}
                for key in item.keys():
                    item_dict[to_camel_case(key)] = item[key]
                api_body[prop].append(item_dict)


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    fc_target_members_spec = {
        "name": {
            "type": "str",
            "default": ""
        },
        "switch_id": {
            "type": "str",
            "choices": [
                'A',
                'B'
            ],
            "default": "A"
        },
        "vsan_id": {
            "type": "int",
        },
        "wwpn": {
            "type": "str",
            "default": ""
        },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        fc_target_members={
            "type": "list",
            "options": fc_target_members_spec,
            "elements": "dict",
        },
        fc_target_zoning_type={
            "type": "str",
            "choices": [
                'SIST',
                'SIMT',
                'None'
            ],
            "default": "SIST"
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
    resource_path = '/fabric/FcZonePolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop_dict_array('FcTargetMembers', 'fc_target_members', intersight.module.params, intersight.api_body)
    check_and_add_prop('FcTargetZoningType', 'fc_target_zoning_type', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
