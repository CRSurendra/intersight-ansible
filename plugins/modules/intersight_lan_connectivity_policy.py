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
module: intersight_lan_connectivity_policy
short_description: LAN Connectivity policy configuration for Cisco Intersight
description:
  - LAN connectivity policy configuration for Cisco Intersight.
  - Used to configure LAN Connectivity Policy on Cisco Intersight managed devices.
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
      - The name assigned to the LAN Connectivity policy.
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
  azure_qos_enabled:
    description:
      -  Enabling AzureStack-Host QoS on an adapter allows the user to carve out traffic classes for RDMA traffic which
      -  ensures that a desired portion of the bandwidth is allocated to it.
    default: False
    type: bool
  iqn_allocation_type:
    description:
      -  Allocation Type of iSCSI Qualified Name - Static/Pool/None.
      -  None - Type indicates that there is no IQN associated to an interface.
      -  Static - Type represents that static IQN is associated to an interface.
      -  Pool - Type indicates that IQN value is sourced from an associated pool.
    choices: ['None' , 'Static' , 'Pool']
    default: None
    type: str
  static_iqn_name:
    description:
      -  User provided static iSCSI Qualified Name (IQN) for use as initiator identifiers by iSCSI vNICs in a Fabric Interconnect domain.
    type: str
    default: ''
  placement_mode:
    description:
      -  The mode used for placement of vNICs on network adapters. It can either be Auto or Custom.
      -  custom - The placement of the vNICs / vHBAs on network adapters is manually chosen by the user.
      -  auto - The placement of the vNICs / vHBAs on network adapters is automatically determined by the system.
    choices: ['custom' , 'auto']
    default: custom
    type: str
  target_platform:
    description:
      -  The platform for which the server profile is applicable. It can either be a server that is operating in standalone mode or
      -  which is attached to a Fabric Interconnect managed by Intersight.
      -  Standalone - Servers which are operating in standalone mode i.e. not connected to a Fabric Interconnected.
      -  FIAttached - Servers which are connected to a Fabric Interconnect that is managed by Intersight.
    choices: ['Standalone' , 'FIAttached']
    default: Standalone
    type: str
  iqn_pool:
    description:
      -  A reference to a iqnpoolPool resource.
    type: str
    default: ''
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure LAN Connectivity Policy
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-LCP
    description: LAN connectivity policy for COS
    tags:
      - Key: Site
        Value: RCDN
    target: FIAttached

- name: Delete LAN Connectivity Policy
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-LCP
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
        "ObjectType": "vnic.LanConnectivityPolicy",
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


def check_and_add_prop_policy(prop, prop_key, params, api_body):
    api_body[prop] = {}
    for key in params.keys():
        api_body[prop][key] = params[key]


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
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        azure_qos_enabled=dict(
            type='bool',
            default=False
        ),
        iqn_allocation_type=dict(
            type='str',
            choices=[
                 'None',
                 'Static',
                 'Pool'
            ],
            default='None'
        ),
        placement_mode=dict(
            type='str',
            choices=[
                 'custom',
                 'auto'
            ],
            default='custom'
        ),
        static_iqn_name=dict(
            type='str',
            default=''
        ),
        target_platform=dict(
            type='str',
            choices=[
                 'Standalone',
                 'FIAttached'
            ],
            default='Standalone'
        ),
        iqn_pool=dict(
            type='str',
            default=''
        ),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    iqn_pool = get_policy_ref(intersight, intersight.module.params['iqn_pool'], '/iqnpool/Pools')

    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/vnic/LanConnectivityPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('AzureQosEnabled', 'azure_qos_enabled', intersight.module.params, intersight.api_body)
    check_and_add_prop('IqnAllocationType', 'iqn_allocation_type', intersight.module.params, intersight.api_body)
    check_and_add_prop('PlacementMode', 'placement_mode', intersight.module.params, intersight.api_body)
    check_and_add_prop('StaticIqnName', 'static_iqn_name', intersight.module.params, intersight.api_body)
    check_and_add_prop('TargetPlatform', 'target_platform', intersight.module.params, intersight.api_body)
    check_and_add_prop_policy('IqnPool', 'iqn_pool', iqn_pool, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
