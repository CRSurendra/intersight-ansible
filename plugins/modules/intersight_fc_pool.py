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
module: intersight_fc_pool
short_description: FC (WWNN or WWPN) Pool configuration for Cisco Intersight
description:
  - FC (WWPN or WWNN) Pool configuration for Cisco Intersight.
  - Used to configure FC Pools on Cisco Intersight
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
      - The name assigned to the FC Pool policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements : dict
    default: []
  description:
    description:
      - The user-defined description of the Boot Order policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
    default: ''
  id_blocks:
    description:
      -  Collection of WWN blocks.
    type: list
    elements: dict
    suboptions:
      from:
        description:
          - 'Starting WWN identifier of the block must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx. Allowed ranges are 20:00:00:00:00:00:00:00'
          - 'to 20:FF:FF:FF:FF:FF:FF:FF or from 50:00:00:00:00:00:00:00 to 5F:FF:FF:FF:FF:FF:FF:FF. To ensure uniqueness of WWNs in the SAN fabric,'
          - 'you are strongly encouraged to use the following WWN prefix; 20:00:00:25:B5:xx:xx:xx.'
        type: str
        default: ""
      to:
        description:
          - 'Ending WWN identifier of the block must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx.'
        type: str
        default: ""
  pool_purpose:
    description:
      -  Purpose of this WWN pool.
    type: str
    default: ""
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure FC Pool
  cisco.intersight.intersight_fc_pool:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-WWPN
    description: FC Pool for COS
    tags:
      - Key: Site
        Value: RCDN
    id_blocks:
      - from: '20:00:00:25:B5:FF:00:00'
        to: '20:00:00:25:B5:FF:00:10'
    pool_purpose: WWPN

- name: Delete FC Pool
  cisco.intersight.intersight_fc_pool:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-WWPN
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-WWPN",
        "ObjectType": "fcpool.Pool",
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


def check_and_add_prop_dict_array(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = []
        if params[prop_key] :
            for item in params[prop_key]:
                item_dict = {}
                for key in item.keys():
                    item_dict[to_camel_case(key)] = item[key]
                api_body[prop].append(item_dict)


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = params[prop_key]


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    id_blocks_spec = {
        "from": {
            "type": "str",
            "default": ""
        },
        "to": {
            "type": "str",
            "default": ""
        },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr'], "default": ""},
        tags={"type": "list", "default": [], "elements": "dict"},
        id_blocks={
            "type": "list",
            "options": id_blocks_spec,
            "elements": "dict",
        },
        pool_purpose={
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
    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/fcpool/Pools'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop_dict_array('IdBlocks', 'id_blocks', intersight.module.params, intersight.api_body)
    check_and_add_prop('PoolPurpose', 'pool_purpose', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
