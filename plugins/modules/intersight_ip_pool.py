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
module: intersight_ip_pool
short_description: IP Pool configuration for Cisco Intersight
description:
  - IP Pool configuration for Cisco Intersight.
  - Used to configure IP Pools on Cisco Intersight
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
      - The name assigned to the IP Pool policy.
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
  ip_v4_blocks:
    description:
      -  Collection of IPv4 blocks.
    type: list
    elements: dict
    suboptions:
      from:
        description:
          -  First IPv4 address of the block.
        type: str
      to:
        description:
          -  Last IPv4 address of the block.
        type: str
  ip_v4_config:
    description:
      -  Netmask, Gateway and DNS settings for IPv4 addresses.
    type: list
    elements: dict
    suboptions:      
      gateway:
        description:
          -  IP address of the default IPv4 gateway.
        type: str
      netmask:
        description:
          -  A subnet mask is a 32-bit number that masks an IP address and divides the IP address into network address and host address.
        type: str
      primary_dns:
        description:
          -  IP Address of the primary Domain Name System (DNS) server.
        type: str
      secondary_dns:
        description:
          -  IP Address of the secondary Domain Name System (DNS) server.
        type: str
  ip_v6_blocks:
    description:
      -  Collection of IPv6 blocks.
    type: list
    elements: dict
    suboptions:      
      from:
        description:
          -  First IPv6 address of the block.
        type: str
      to:
        description:
          -  Last IPv6 address of the block.
        type: str
  ip_v6_config:
    description:
      -  Netmask, Gateway and DNS settings for IPv6 addresses.
    type: list
    elements: dict
    suboptions:
      gateway:
        description:
          -  IP address of the default IPv6 gateway.
        type: str
      prefix:
        description:
          -  A prefix length which masks the  IP address and divides the IP address into network address and host address.
        type: int
      primary_dns:
        description:
          -  IP Address of the primary Domain Name System (DNS) server.
        type: str
      secondary_dns:
        description:
          -  IP Address of the secondary Domain Name System (DNS) server.
        type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure IP Pool
  cisco.intersight.intersight_ip_pool:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-IPP
    description: IP Pool for COS
    tags:
      - Key: Site
        Value: RCDN
    ip_v4_blocks:
      - from: 10.1.1.2
        to: 10.1.1.25
    ip_v4_config:
      - gateway: 10.1.1.1
        netmask: 255.255.255.0
        primary_dns: 172.121.234.231
        secondary_dns: 10.45.67.89

- name: Delete IP Pool
  cisco.intersight.intersight_ip_pool:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-IPP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-IPP",
        "ObjectType": "ippool.Pool",
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

def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for item in params[prop_key]:
                for key in item.keys():
                    api_body[prop][to_camel_case(key)] = item[key]


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    ip_v4_blocks_spec = {
        "from": {
            "type": "str",
            "default": ""
        },
        "to": {
            "type": "str",
            "default": ""
          },
    }
    ip_v4_config_spec = {
        "gateway": {
            "type": "str",
            "default": ""
          },
        "netmask": {
            "type": "str",
            "default": ""
          },
        "primary_dns": {
            "type": "str",
            "default": ""
          },
        "secondary_dns": {
            "type": "str",
            "default": ""
          },
    }
    ip_v6_blocks_spec = {
        "from": {
            "type": "str",
            "default": ""
          },
        "to": {
            "type": "str",
            "default": ""
          },
    }
    ip_v6_config_spec = {
        "gateway": {
            "type": "str",
            "default": ""
          },
        "prefix": {
            "type": "int",
          },
        "primary_dns": {
            "type": "str",
            "default": ""
          },
        "secondary_dns": {
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
        ip_v4_blocks={
            "type": "list",
            "options": ip_v4_blocks_spec,
            "elements": "dict",
        },
        ip_v4_config={
            "type": "list",
            "options": ip_v4_config_spec,
            "elements": "dict",
        },
        ip_v6_blocks={
            "type": "list",
            "options": ip_v6_blocks_spec,
            "elements": "dict",
        },
        ip_v6_config={
            "type": "list",
            "options": ip_v6_config_spec,
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
    resource_path = '/ippool/Pools'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop_dict_array('IpV4Blocks', 'ip_v4_blocks', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('IpV4Config', 'ip_v4_config', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict_array('IpV6Blocks', 'ip_v6_blocks', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('IpV6Config', 'ip_v6_config', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
