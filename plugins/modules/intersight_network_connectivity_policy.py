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
module: intersight_network_connectivity_policy
short_description: Network Connectivity policy configuration for Cisco Intersight
description:
  - Network Connectivity policy configuration for Cisco Intersight.
  - Used to configure Network Connectivity Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Network Connectivity policy.
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
      - The user-defined description of the Network Connectivity Policy
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  alternate_ipv4dns_server:
    description:
      -  IP address of the secondary DNS server.
    type: str
  alternate_ipv6dns_server:
    description:
      -  IP address of the secondary DNS server.
    type: str
  dynamic_dns_domain:
    description:
      -  The domain name appended to a hostname for a Dynamic DNS (DDNS) update. If left blank, only a hostname is sent to the DDNS update request.
    type: str
  enable_dynamic_dns:
    description:
      -  If enabled, updates the resource records to the DNS from Cisco IMC.
    type: bool
  enable_ipv4dns_from_dhcp:
    description:
      -  If enabled, Cisco IMC retrieves the DNS server addresses from DHCP. Use DHCP field must be enabled for IPv4 in Cisco IMC to enable it.
    type: bool
  enable_ipv6:
    description:
      -  If enabled, allows to configure IPv6 properties.
    type: bool
  enable_ipv6dns_from_dhcp:
    description:
      -  If enabled, Cisco IMC retrieves the DNS server addresses from DHCP. Use DHCP field must be enabled for IPv6 in Cisco IMC to enable it.
    type: bool
  preferred_ipv4dns_server:
    description:
      -  IP address of the primary DNS server.
    type: str
  preferred_ipv6dns_server:
    description:
      -  IP address of the primary DNS server.
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Network Connectivity Policy
  cisco.intersight.intersight_network_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-NCP
    description: Network Connectivity Policy for COS
    tags:
      - Key: Site
        Value: RCDN
    enable_dynamic_dns: False
    preferred_ipv4dns_server: 64.104.128.236
    alternate_ipv4dns_server: 72.163.128.140

- name: Delete Network Connectivity Policy
  cisco.intersight.intersight_network_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-NCP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-LCP",
        "ObjectType": "networkconfig.Policy",
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


def main():
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        alternate_ipv4dns_server={
            "type": "str",
        },
        alternate_ipv6dns_server={
            "type": "str",
        },
        dynamic_dns_domain={
            "type": "str",
        },
        enable_dynamic_dns={
            "type": "bool",
        },
        enable_ipv4dns_from_dhcp={
            "type": "bool",
        },
        enable_ipv6={
            "type": "bool",
        },
        enable_ipv6dns_from_dhcp={
            "type": "bool",
        },
        preferred_ipv4dns_server={
            "type": "str",
        },
        preferred_ipv6dns_server={
            "type": "str",
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
    resource_path = '/networkconfig/Policies'

    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('AlternateIpv4dnsServer', 'alternate_ipv4dns_server', intersight.module.params, intersight.api_body)
    check_and_add_prop('AlternateIpv6dnsServer', 'alternate_ipv6dns_server', intersight.module.params, intersight.api_body)
    check_and_add_prop('DynamicDnsDomain', 'dynamic_dns_domain', intersight.module.params, intersight.api_body)
    check_and_add_prop('EnableDynamicDns', 'enable_dynamic_dns', intersight.module.params, intersight.api_body)
    check_and_add_prop('EnableIpv4dnsFromDhcp', 'enable_ipv4dns_from_dhcp', intersight.module.params, intersight.api_body)
    check_and_add_prop('EnableIpv6', 'enable_ipv6', intersight.module.params, intersight.api_body)
    check_and_add_prop('EnableIpv6dnsFromDhcp', 'enable_ipv6dns_from_dhcp', intersight.module.params, intersight.api_body)
    check_and_add_prop('PreferredIpv4dnsServer', 'preferred_ipv4dns_server', intersight.module.params, intersight.api_body)
    check_and_add_prop('PreferredIpv6dnsServer', 'preferred_ipv6dns_server', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
