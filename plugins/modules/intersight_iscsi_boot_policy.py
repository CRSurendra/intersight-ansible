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
module: intersight_iscsi_boot_policy
short_description: iSCSI Boot policy configuration for Cisco Intersight
description:
  - iSCSI Boot policy configuration for Cisco Intersight.
  - Used to configure iSCSI Boot Policy on Cisco Intersight managed devices.
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
      - The name assigned to the iSCSI Boot policy.
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
  auto_targetvendor_name:
    description:
      -  Auto target interface that is represented via the Initiator name or the DHCP vendor ID. The vendor ID can be up to 32 alphanumeric characters.
    type: str
  chap:
    description:
      -  CHAP authentication parameters for iSCSI Target.
    type: list
    elements: dict
    suboptions:
      is_password_set:
        description:
          -  Indicates whether the value of the 'password' property has been set.
        default: False
        type: bool
      password:
        description:
          -  password of Initiator/Target Interface. Enter between 12 and 16 characters, including special characters except spaces, tabs, line breaks.
        type: str
      user_id:
        description:
          -  User Id of Initiator/Target Interface. Enter between 1 and 128 characters, spaces, or special characters.
        type: str
  initiator_ip_source:
    description:
      -  Source Type of Initiator IP Address - Auto/Static/Pool.
      -  DHCP - The IP address is assigned using DHCP, if available.
      -  Static - Static IPv4 address is assigned to the iSCSI boot interface based on the information entered in this area.
      -  Pool - An IPv4 address is assigned to the iSCSI boot interface from the management IP address pool.
    choices: ['DHCP' , 'Static' , 'Pool']
    default: DHCP
    type: str
  initiator_static_ip_v4_address:
    description:
      -  Static IP address provided for iSCSI Initiator.
    type: str
  initiator_static_ip_v4_config:
    description:
      -  IPV4 configurations such as Netmask, Gateway and DNS for iSCSI Initiator.
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
  mutual_chap:
    description:
      -  Mutual CHAP authentication parameters for iSCSI Initiator. Two-way CHAP mechanism.
    type: list
    elements: dict
    suboptions:
      is_password_set:
        description:
          -  Indicates whether the value of the 'password' property has been set.
        default: False
        type: bool
      password:
        description:
          -  password of Initiator/Target Interface. Enter between 12 and 16 characters, including special characters except spaces, tabs, line breaks.
        type: str
      user_id:
        description:
          -  User Id of Initiator/Target Interface. Enter between 1 and 128 characters, spaces, or special characters.
        type: str
  target_source_type:
    description:
      -  Source Type of Targets - Auto/Static.
      -  Static - Type indicates that static target interface is assigned to iSCSI boot.
      -  Auto - Type indicates that the system selects the target interface automatically during iSCSI boot.
    choices: ['Static' , 'Auto']
    default: Static
    type: str
  initiator_ip_pool:
    description:
      -  A reference to a ippoolPool resource.
    type: str
  iscsi_adapter_policy:
    description:
      -  A reference to a vniciscsi_adapter_policy resource.
    type: str
  primary_target_policy:
    description:
      -  A reference to a vnicIscsiStaticTargetPolicy resource.
    type: str
  secondary_target_policy:
    description:
      -  A reference to a vnicIscsiStaticTargetPolicy resource.
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure iSCSI Boot Policy
  cisco.intersight.intersight_iscsi_boot_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ISBP
    target_source_type: Auto
    auto_targetvendor_name: SOMETHING
    iscsi_adapter_policy: TEST_ISAP


- name: Delete iSCSI Boot Policy
  cisco.intersight.intersight_iscsi_boot_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ISBP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-ISBP",
        "ObjectType": "vnic.IscsiBootPolicy",
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
    chap_spec = {
        "is_password_set": {
            "type": "bool",
            "default": False
        },
        "password": {
            "type": "str",
            "no_log": True
        },
        "user_id": {
            "type": "str",
        },
    }
    initiator_static_ip_v4_config_spec = {
        "gateway": {
            "type": "str",
        },
        "netmask": {
            "type": "str",
        },
        "primary_dns": {
            "type": "str",
        },
        "secondary_dns": {
            "type": "str",
        },
    }
    mutual_chap_spec = {
        "is_password_set": {
            "type": "bool",
            "default": False
        },
        "password": {
            "type": "str",
            "no_log": True
        },
        "user_id": {
            "type": "str",
        },
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        auto_targetvendor_name={
            "type": "str",
        },
        chap={
            "type": "list",
            "options": chap_spec,
            "elements": "dict",
        },
        initiator_ip_source={
            "type": "str",
            "choices": [
                'DHCP',
                'Static',
                'Pool'
            ],
            "default": "DHCP"
        },
        initiator_static_ip_v4_address={
            "type": "str",
        },
        initiator_static_ip_v4_config={
            "type": "list",
            "options": initiator_static_ip_v4_config_spec,
            "elements": "dict",
        },
        mutual_chap={
            "type": "list",
            "options": mutual_chap_spec,
            "elements": "dict",
        },
        target_source_type={
            "type": "str",
            "choices": [
                'Static',
                'Auto'
            ],
            "default": "Static"
        },
        initiator_ip_pool={
            "type": "str",
        },
        iscsi_adapter_policy={
            "type": "str",
        },
        primary_target_policy={
            "type": "str",
        },
        secondary_target_policy={
            "type": "str",
        },
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ('target_source_type', 'Auto', ('auto_targetvendor_name', )),
            ('target_source_type', 'Static', ('initiator_ip_source', 'primary_target_policy', )),
            ('initiator_ip_source', 'Pool', ('initiator_ip_pool',)),
            ('initiator_ip_source', 'Static', ('initiator_static_ip_v4_address', 'initiator_static_ip_v4_config')),
        ]
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    initiator_ip_pool = get_policy_ref(intersight, intersight.module.params['initiator_ip_pool'], '/ippool/Pools')
    iscsi_adapter_policy = get_policy_ref(intersight, intersight.module.params['iscsi_adapter_policy'], '/vnic/IscsiAdapterPolicies')
    primary_target_policy = get_policy_ref(intersight, intersight.module.params['primary_target_policy'], '/vnic/IscsiStaticTargetPolicies')
    secondary_target_policy = get_policy_ref(intersight, intersight.module.params['secondary_target_policy'], '/vnic/IscsiStaticTargetPolicies')

    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/vnic/IscsiBootPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }

    check_and_add_prop('AutoTargetvendorName', 'auto_targetvendor_name', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('Chap', 'chap', intersight.module.params, intersight.api_body)
    check_and_add_prop('InitiatorIpSource', 'initiator_ip_source', intersight.module.params, intersight.api_body)
    check_and_add_prop('InitiatorStaticIpV4Address', 'initiator_static_ip_v4_address', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('InitiatorStaticIpV4Config', 'initiator_static_ip_v4_config', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('MutualChap', 'mutual_chap', intersight.module.params, intersight.api_body)
    check_and_add_prop('TargetSourceType', 'target_source_type', intersight.module.params, intersight.api_body)
    check_and_add_prop_policy('InitiatorIpPool', 'initiator_ip_pool', initiator_ip_pool, intersight.api_body)
    check_and_add_prop_policy('IscsiAdapterPolicy', 'iscsi_adapter_policy', iscsi_adapter_policy, intersight.api_body)
    check_and_add_prop_policy('PrimaryTargetPolicy', 'primary_target_policy', primary_target_policy, intersight.api_body)
    check_and_add_prop_policy('SecondaryTargetPolicy', 'secondary_target_policy', secondary_target_policy, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
