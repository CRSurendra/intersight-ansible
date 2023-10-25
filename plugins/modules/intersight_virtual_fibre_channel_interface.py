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
module: intersight_virtual_fibre_channel_interface
short_description: Virtual Fibre Channel Interface configuration for Cisco Intersight
description:
  - Virtual Fibre Channel Interface configuration for Cisco Intersight.
  - Used to configure Virtual Fibre Channel Interface on Cisco Intersight managed devices.
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
      - The name assigned to the virtual fibre channel interface.
      - The name must be between 1 and 31 alphanumeric characters, allowing special characters :-_.
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements : dict
  order:
    description:
      - The order in which the virtual interface is brought up. The order assigned to an interface should
      - be unique for all the Ethernet and Fibre-Channel interfaces on each PCI link on a VIC adapter.
      - The order should start from zero with no overlaps. The maximum value of PCI order is limited by the number
      - of virtual interfaces (Ethernet and Fibre-Channel) on each PCI link on a VIC adapter.
      - All VIC adapters have a single PCI link except VIC 1340, VIC 1380 and VIC 1385 which have two.
    type: int
    default: 0
  persistent_bindings:
    description:
      -  Enables retention of LUN ID associations in memory until they are manually cleared.
    type: bool
    default: False
  pin_group_name:
    description:
      - Pingroup name associated to vfc for static pinning. SCP deploy will resolve pingroup name and fetches the correspoding uplink port/port
      - channel to pin the vfc traffic.
    type: str
    default: ''
  placement:
    description:
      -  placement Settings for the virtual interface.
    type: list
    elements: dict
    suboptions:
      auto_pci_link:
        description:
          - Enable or disable automatic assignment of the PCI Link in a dual-link adapter. This option applies only to 13xx series VICs that support dual-link.
          - If enabled, the system determines the placement of the vNIC/vHBA on either of the PCI Links.
        type: bool
        default: False
      auto_slot_id:
        description:
          - Enable or disable automatic assignment of the VIC slot ID. If enabled and the server has only one VIC, the same VIC is chosen for all the vNICs.
          - If enabled and the server has multiple VICs, the vNIC/vHBA are deployed on the first VIC.
          - The Slot ID determines the first VIC. MLOM is the first Slot ID and the ID increments to 2, 3, and so on.
        type: bool
        default: False
      id:
        description:
          - PCIe Slot where the VIC adapter is installed. Supported values are (1-15) and MLOM.
        type: str
        default: ''
      pci_link:
        description:
          - The PCI Link used as transport for the virtual interface. PCI Link is only applicable for select
          - Cisco UCS VIC 1300 models (UCSC-PCIE-C40Q-03, UCSB-MLOM-40G-03, UCSB-VIC-M83-8P) that support two PCI links.
          - The value, if specified, for any other VIC model will be ignored.
        type: int
        default: 0
      pci_link_assignment_mode:
        description:
          - If the autoPciLink is disabled, the user can either choose to place the vNICs manually or based on a policy.
          - If the autoPciLink is enabled, it will be set to None.
          - Custom - The user needs to specify the PCI Link manually.
          - Load-Balanced - The system will uniformly distribute the interfaces across the PCI Links.
          - None - Assignment is not applicable and will be set when the AutoPciLink is set to true.
        type: str
        choices: ['Custom', 'Load-Balanced', 'None']
        default: Custom
      switch_id:
        description:
          - The fabric port to which the vNICs will be associated.
          - None - Fabric Id is not set to either A or B for the standalone case where the server is not connected to Fabric Interconnects.
          - 'A - Fabric A of the FI cluster.'
          - 'B - Fabric B of the FI cluster.'
        type: str
        choices: ['None', 'A', 'B']
        default: None
      uplink:
        description:
          - Adapter port on which the virtual interface will be created.
        type: int
        default: 0
  static_wwpn_address:
    description:
      - 'The WWPN address must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx.'
      - 'Allowed ranges are 20:00:00:00:00:00:00:00 to 20:FF:FF:FF:FF:FF:FF:FF or from 50:00:00:00:00:00:00:00 to 5F:FF:FF:FF:FF:FF:FF:FF.'
      - 'To ensure uniqueness of WWNs in the SAN fabric, you are strongly encouraged to use the WWN prefix - 20:00:00:25:B5:xx:xx:xx.'
    type: str
    default: ''
  type:
    description:
      -  VHBA type configuration for SAN Connectivity Policy. This configuration is supported only on Cisco VIC 14XX series and higher series of adapters.
      -  fc-initiator - The default value set for vHBA type Configuration. Fc-initiator specifies vHBA as a consumer of storage. Enables SCSI commands
         to transfer data and status information between host and target storage systems.
      -  fc-nvme-initiator - Fc-nvme-initiator specifies vHBA as a consumer of storage. Enables NVMe-based message commands to transfer data and status
         information between host and target storage systems.
      -  fc-nvme-target - Fc-nvme-target specifies vHBA as a provider of storage volumes to initiators. Enables NVMe-based message commands to transfer
         data and status information between host and target storage systems. Currently tech-preview, only enabled with an asynchronous driver.
      -  fc-target - Fc-target specifies vHBA as a provider of storage volumes to initiators. Enables SCSI commands to transfer data and status information
         between host and target storage systems. fc-target is enabled only with an asynchronous driver.
    choices: ['fc-initiator' , 'fc-nvme-initiator' , 'fc-nvme-target' , 'fc-target']
    default: fc-initiator
    type: str
  wwpn_address_type:
    description:
      -  Type of allocation selected to assign a WWPN address to the vhba.
      -  POOL - The user selects a pool from which the mac/wwn address will be leased for the Virtual Interface.
      -  STATIC - The user assigns a static mac/wwn address for the Virtual Interface.
    choices: ['POOL' , 'STATIC']
    default: POOL
    type: str
  fc_adapter_policy:
    description:
      -  A reference to a vnicfc_adapter_policy resource.
      - When the $expand query parameter is specified, the referenced resource is returned inline.
    type: str
    default: ''
  fc_network_policy:
    description:
      -  A reference to a vnicfc_network_policy resource.
      - When the $expand query parameter is specified, the referenced resource is returned inline.
    type: str
    default: ''
  fc_qos_policy:
    description:
      -  A reference to a vnicfc_qos_policy resource.
      - When the $expand query parameter is specified, the referenced resource is returned inline.
    type: str
    default: ''
  san_connectivity_policy:
    description:
      -  A reference to a vnicsan_connectivity_policy resource.
    type: str
    default: ''
  wwpn_pool:
    description:
      -  A reference to a fcpoolPool resource.
    type: str
    default: ''

author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Virtual Fibre Channel Interface
  cisco.intersight.intersight_virtual_fibre_channel_interface_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: hba0
    tags:
      - Key: Site
        Value: RCDN
    type: fc-initiator
    order: 1
    placement:
      - id : 2
        uplink : 0
    fc_adapter_policy: TEST_FAP
    fc_network_policy: TEST_FNP
    fc_qos_policy: TEST_FQOS
    san_connectivity_policy: TEST_SCP

- name: Delete Virtual Fibre Channel Interface
  cisco.intersight.intersight_virtual_fibre_channel_interface_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: hba0
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "eth0",
        "ObjectType": "vnic.FcIf",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, compare_values


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = params[prop_key]


def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for item in params[prop_key]:
                for key in item.keys():
                    api_body[prop][to_camel_case(key)] = item[key]


def check_and_add_prop_policy(prop, prop_key, params, api_body):
    api_body[prop] = {}
    for key in params.keys():
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

    placement_settings_spec = {
        "auto_pci_link" : {"type": "bool", "default": "False"},
        "auto_slot_id" : {"type": "bool", "default": "False"},
        "id" : {"type": "str", "default": ''},
        "pci_link" : {"type": "int", "default": 0},
        "pci_link_assignment_mode" : {"type": "str", "choices": ['Custom', 'Load-Balanced', 'None'], "default": 'Custom'},
        "switch_id" : {"type": "str", "choices": ['None', 'A', 'B'], "default": 'None'},
        "uplink" : {"type": "int", "default": 0}
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        name={"type": "str", "required": True},
        tags={"type": "list", "elements": "dict"},
        order={"type": "int", "default": 0},
        persistent_bindings={"type": "bool", "default": False},
        pin_group_name={"type": "str", "default": ""},
        placement={
            "type": "list",
            "elements": "dict",
            "options": placement_settings_spec
        },
        static_wwpn_address={
            "type": "str",
            "default": ""
        },
        type={
            "type": "str",
            "choices": [
                'fc-initiator',
                'fc-nvme-initiator',
                'fc-nvme-target',
                'fc-target'
            ],
            "default": "fc-initiator"
        },
        wwpn_address_type={
            "type": "str",
            "choices": [
                'POOL',
                'STATIC'
            ],
            "default": "POOL"
        },
        fc_adapter_policy={
            "type": "str",
            "default": ""
        },
        fc_network_policy={
            "type": "str",
            "default": ""
        },
        fc_qos_policy={
            "type": "str",
            "default": ""
        },
        san_connectivity_policy={
            "type": "str",
            "default": ""
        },
        wwpn_pool={
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

    fc_adapter_policy = get_policy_ref(intersight, intersight.module.params['fc_adapter_policy'], '/vnic/FcAdapterPolicies')
    fc_network_policy = get_policy_ref(intersight, intersight.module.params['fc_network_policy'], '/vnic/FcNetworkPolicies')
    fc_qos_policy = get_policy_ref(intersight, intersight.module.params['fc_qos_policy'], '/vnic/FcQosPolicies')
    san_connectivity_policy = get_policy_ref(intersight, intersight.module.params['san_connectivity_policy'], '/vnic/SanConnectivityPolicies')
    wwpn_pool = get_policy_ref(intersight, intersight.module.params['wwpn_pool'], '/fcpool/Pools')

    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/vnic/FcIfs'
    # Define API body used in compares or create
    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
    }
    check_and_add_prop('Order', 'order', intersight.module.params, intersight.api_body)
    check_and_add_prop('PersistentBindings', 'persistent_bindings', intersight.module.params, intersight.api_body)
    check_and_add_prop('PinGroupName', 'pin_group_name', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('Placement', 'placement', intersight.module.params, intersight.api_body)
    check_and_add_prop('StaticWwpnAddress', 'static_wwpn_address', intersight.module.params, intersight.api_body)
    check_and_add_prop('Type', 'type', intersight.module.params, intersight.api_body)
    check_and_add_prop('WwpnAddressType', 'wwpn_address_type', intersight.module.params, intersight.api_body)
    check_and_add_prop_policy('FcAdapterPolicy', 'fc_adapter_policy', fc_adapter_policy, intersight.api_body)
    check_and_add_prop_policy('FcNetworkPolicy', 'fc_network_policy', fc_network_policy, intersight.api_body)
    check_and_add_prop_policy('FcQosPolicy', 'fc_qos_policy', fc_qos_policy, intersight.api_body)
    check_and_add_prop_policy('SanConnectivityPolicy', 'san_connectivity_policy', san_connectivity_policy, intersight.api_body)
    check_and_add_prop_policy('WwpnPool', 'wwpn_pool', wwpn_pool, intersight.api_body)

    # Get the current state of the resource
    filter_str = "Name eq '" + intersight.module.params['name'] + "'"
    filter_str += "and Parent.Moid eq '" + san_connectivity_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    vnic_moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        vnic_moid = intersight.result['api_response']['Moid']
        resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if not resource_values_match:
        intersight.configure_resource(moid=vnic_moid, resource_path=resource_path, body=intersight.api_body, query_params=None)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
