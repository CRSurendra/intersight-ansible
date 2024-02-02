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
module: intersight_server_profile_template
short_description: Server Profile Template configuration for Cisco Intersight
description:
  - Server Profile Template configuration for Cisco Intersight.
  - Used to configure Server Profiles Template with assigned server policies.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    type: str
    choices: [present, absent]
    default: present
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    type: str
    default: default
  name:
    description:
      - The name assigned to the Server Profile Template.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  target_platform:
    description:
      - The platform for which the server profile template  is applicable.
      - Can either be a server that is operating in Standalone mode or which is attached to a Fabric Interconnect (FIAttached) managed by Intersight.
    type: str
    choices: [Standalone, FIAttached]
    default: Standalone
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  description:
    description:
      - The user-defined description of the Server Profile Template.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  adapter_config_policy:
    description:
      - Name of the Adapter Configuration Policy to be associated with this profile
  boot_order_policy:
    description:
      - Name of Boot Order Policy to associate with this profile template.
    type: str
  imc_access_policy:
    description:
      - Name of IMC Access Policy to associate with this profile tempalte.
    type: str
  lan_connectivity_policy:
    description:
      - Name of LAN Connectivity Policy to associate with this profile tempalte.
    type: str
  local_user_policy:
    description:
      - Name of Local User Policy to associate with this profile template.
    type: str
  ntp_policy:
    description:
      - Name of NTP Policy to associate with this profile template.
    type: str
  storage_policy:
    description:
      - Name of Storage Policy to associate with this profile tempalte.
    type: str
  virtual_media_policy:
    description:
      - Name of Virtual Media Policy to associate with this profile template.
    type: str
author:
  - David Soper (@dsoper2)
  - Sid Nath (@SidNath21)
  - Tse Kai "Kevin" Chan (@BrightScale)
  - Soma Tummala (@SOMATUMMALA21)
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Server Profile
  cisco.intersight.intersight_server_profile_template:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: SPT1
    target_platform: FIAttached
    tags:
      - Key: Site
        Value: SJC02
    description: Profile for Server1
    adapter_config_policy : COS-adapter-config
    boot_order_policy: COS-Boot
    imc_access_policy: sjc02-d23-access
    lan_connectivity_policy: sjc02-d23-lan
    local_user_policy: guest-admin
    ntp_policy: lab-ntp
    storage_policy: storage
    virtual_media_policy: COS-VM

- name: Delete Server Profile
  cisco.intersight.intersight_server_profile_template:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: SPT1
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "SPT1",
        "ObjectType": "server.ProfileTemplate",
        "Tags": [
            {
                "Key": "Site",
                "Value": "SJC02"
            }
        ],
        "TargetPlatform": "FIAttached",
        "Type": "instance"
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec

argument_spec = intersight_argument_spec
argument_spec.update(
    state=dict(type='str', choices=['present', 'absent'], default='present'),
    organization=dict(type='str', default='default'),
    name=dict(type='str', required=True),
    target_platform=dict(type='str', choices=['Standalone', 'FIAttached'], default='Standalone'),
    tags=dict(type='list', elements='dict'),
    description=dict(type='str', aliases=['descr']),
    adapter_config_policy=dict(type='str'),
    boot_order_policy=dict(type='str'),
    imc_access_policy=dict(type='str'),
    lan_connectivity_policy=dict(type='str'),
    local_user_policy=dict(type='str'),
    ntp_policy=dict(type='str'),
    storage_policy=dict(type='str'),
    virtual_media_policy=dict(type='str'),
)

def setup_module_object():
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )
    return module

def post_profile_template_to_policy(intersight, moid, resource_path, policy_name):
    options = {
        'http_method': 'get',
        'resource_path': resource_path,
        'query_params': {
            '$filter': "Name eq '" + policy_name + "'",
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        # get expected policy moid from 1st list element
        expected_policy_moid = response['Results'][0]['Moid']
        actual_policy_moid = ''
        # check any current profiles and delete if needed
        options = {
            'http_method': 'get',
            'resource_path': resource_path,
            'query_params': {
                '$filter': "Profiles/any(t: t/Moid eq '" + moid + "')",
            },
        }
        response = intersight.call_api(**options)
        if response.get('Results'):
            # get actual moid from 1st list element
            actual_policy_moid = response['Results'][0]['Moid']
            if actual_policy_moid != expected_policy_moid:
                if not intersight.module.check_mode:
                    # delete the actual policy
                    options = {
                        'http_method': 'delete',
                        'resource_path': resource_path + '/' + actual_policy_moid + '/Profiles',
                        'moid': moid,
                    }
                    intersight.call_api(**options)
                actual_policy_moid = ''
        if not actual_policy_moid:
            if not intersight.module.check_mode:
                # post profile to the expected policy
                options = {
                    'http_method': 'post',
                    'resource_path': resource_path + '/' + expected_policy_moid + '/Profiles',
                    'body': [
                        {
                            'ObjectType': 'server.ProfileTemplate',
                            'Moid': moid,
                        }
                    ]
                }
                intersight.call_api(**options)
            intersight.result['changed'] = True

def create_server_profile_template(intersight):
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    #
    # Argument spec above, resource path, and API body should be the only code changed in this module
    #
    resource_path = '/server/ProfileTemplates'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    intersight.result['api_response'] = {}
    
    if intersight.module.params['target_platform'] == 'FIAttached':
        intersight.api_body['TargetPlatform'] = intersight.module.params['target_platform']

    # Configure the profile
    moid = intersight.configure_policy_or_profile(resource_path=resource_path)

    if moid and intersight.module.params['adapter_config_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/adapter/ConfigPolicies', policy_name=intersight.module.params['adapter_config_policy'])

    if moid and intersight.module.params['boot_order_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/boot/PrecisionPolicies', policy_name=intersight.module.params['boot_order_policy'])

    if moid and intersight.module.params['imc_access_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/access/Policies', policy_name=intersight.module.params['imc_access_policy'])

    if moid and intersight.module.params['lan_connectivity_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/vnic/LanConnectivityPolicies', policy_name=intersight.module.params['lan_connectivity_policy'])

    if moid and intersight.module.params['local_user_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/iam/EndPointUserPolicies', policy_name=intersight.module.params['local_user_policy'])

    if moid and intersight.module.params['ntp_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/ntp/Policies', policy_name=intersight.module.params['ntp_policy'])

    if moid and intersight.module.params['storage_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/storage/StoragePolicies', policy_name=intersight.module.params['storage_policy'])

    if moid and intersight.module.params['virtual_media_policy']:
        post_profile_template_to_policy(intersight, moid, resource_path='/vmedia/Policies', policy_name=intersight.module.params['virtual_media_policy'])

def main():
    module = setup_module_object()
    intersight = IntersightModule(module)
    create_server_profile_template(intersight)
    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
