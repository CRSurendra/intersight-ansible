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
module: intersight_fabric_port_policy
short_description: Fabric Port policy configuration for Cisco Intersight
description:
  - Fabric Port policy configuration for Cisco Intersight.
  - Used to configure Fabric Port  Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Fabric Port policy.
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
      - The user-defined description of the Fabric Port policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  device_model:
    description:
      -  This field specifies the device model that this Port Policy is being configured for.
      -  UCS-FI-6454 - The standard 4th generation UCS Fabric Interconnect with 54 ports.
      -  UCS-FI-64108 - The expanded 4th generation UCS Fabric Interconnect with 108 ports.
      -  UCS-FI-6536 - The standard 5th generation UCS Fabric Interconnect with 36 ports.
      -  unknown - Unknown device type, usage is TBD.
    choices: ['UCS-FI-6454' , 'UCS-FI-64108' , 'UCS-FI-6536' , 'unknown']
    default: UCS-FI-6454
    type: str
  port_modes:
    description: port modes configuration for the switch
    type: list
    elements: dict
    suboptions:
      custom_mode:
        description:
          -  Custom Port Mode specified for the port range.
          -  FibreChannel - Fibre Channel Port Types.
          -  BreakoutEthernet10G - Breakout Ethernet 10G Port Type.
          -  BreakoutEthernet25G - Breakout Ethernet 25G Port Type.
          -  BreakoutFibreChannel8G - Breakout FibreChannel 8G Port Type.
          -  BreakoutFibreChannel16G - Breakout FibreChannel 16G Port Type.
          -  BreakoutFibreChannel32G - Breakout FibreChannel 32G Port Type.
        choices: ['FibreChannel' , 'BreakoutEthernet10G' , 'BreakoutEthernet25G' , 'BreakoutFibreChannel8G' , 'BreakoutFibreChannel16G',
                  'BreakoutFibreChannel32G']
        default: FibreChannel
        type: str
      port_id_end:
        description:
          -  Ending range of the Port Identifier.
        type: int
      port_id_start:
        description:
          -  Starting range of the Port Identifier.
        type: int
      slot_id:
        description:
          -  Slot Identifier of the switch.
        type: int
  port_roles:
    description: port roles configuration for the switch
    type: list
    elements: dict
    suboptions:
      port_role:
        description:
          -  The role of the port.
          -  Appliance - Appliance Role
          -  EthernetUplink - Ethernet Uplink Role
          -  FcUplink - Fc Uplink Role
          -  FcoeUplink - Fcoe Uplink Role
          -  FcStorage - Fc Storage Role
          -  Server - Server Roile
        choices: ['Appliance' , 'EthernetUplink', 'FcUplink', 'FcoeUplink', 'FcStorage', 'Server']
        type: str
        required: true
      port_id_end:
        description: Ending range of the Port Identifier.
        type: int
      port_id_start:
        description: Starting range of the Port Identifier.
        type: int
      slot_id:
        description: Slot Identifier of the switch.
        type: int
      aggregate_port_id:
        description:
          -  Breakout port Identifier of the Switch Interface.
          - When a port is not configured as a breakout port, the aggregatePortId is set to 0, and unused.
          - When a port is configured as a breakout port, the 'aggregatePortId' port number as labeled on the equipment,
          - e.g. the id of the port on the switch.
        type: int
        default: 0
      appliance_spec:
        description: Appliance port role specification
        type: dict
        suboptions:
          mode:
            description:
              -  Port mode to be set on the appliance port.
              -  trunk - Trunk mode Switch Port Type.
              -  access - Access mode Switch Port Type.
            choices: ['trunk' , 'access']
            default: trunk
            type: str
          priority:
            description:
              -  The 'name' of the System QoS Class.
              -  Best Effort - QoS priority for Best-effort traffic.
              -  FC - QoS priority for FC traffic.
              -  Platinum - QoS priority for Platinum traffic.
              -  Gold - QoS priority for Gold traffic.
              -  Silver - QoS priority for Silver traffic.
              -  Bronze - QoS priority for Bronze traffic.
            choices: ['Best Effort' , 'FC' , 'Platinum' , 'Gold' , 'Silver' , 'Bronze']
            default: Best Effort
            type: str
          eth_network_control_policy:
            description:
              -  A reference to a fabriceth_network_control_policy resource.
              - When the $expand query parameter is specified, the referenced resource is returned inline.
            type: str
          eth_network_group_policy:
            description:
              -  A reference to a fabriceth_network_group_policy resource.
              - When the $expand query parameter is specified, the referenced resource is returned inline.
            type: str
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          fec:
            description:
              -  Forward error correction configuration for the port.
              -  Auto - Forward error correction option 'Auto'.
              -  Cl91 - Forward error correction option 'cl91'.
              -  Cl74 - Forward error correction option 'cl74'.
            choices: ['Auto' , 'Cl91' , 'Cl74']
            default: Auto
            type: str
      server_spec:
        description: Server port role specification
        type: dict
        suboptions:
          auto_negotiation_disabled:
            description: Auto Negotiation Disabled.
            type: bool
            default: False
          fec:
            description:
              -  Forward error correction configuration for the port.
              -  Auto - Forward error correction option 'Auto'.
              -  Cl91 - Forward error correction option 'cl91'.
              -  Cl74 - Forward error correction option 'cl74'.
            choices: ['Auto' , 'Cl91' , 'Cl74']
            default: Auto
            type: str
      fc_storage_spec:
        description: FC Storage port role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  16Gbps - Admin configurable speed 16Gbps.
              -  8Gbps - Admin configurable speed 8Gbps.
              -  32Gbps - Admin configurable speed 32Gbps.
              -  Auto - Admin configurable speed AUTO ( default ).
            choices: ['16Gbps' , '8Gbps' , '32Gbps' , 'Auto']
            default: 16Gbps
            type: str
          vsan_id:
            description:
              -  Virtual San Identifier associated to the FC port.
            type: int
      fc_uplink_spec:
        description: FC Uplink port role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  16Gbps - Admin configurable speed 16Gbps.
              -  8Gbps - Admin configurable speed 8Gbps.
              -  32Gbps - Admin configurable speed 32Gbps.
              -  Auto - Admin configurable speed AUTO ( default ).
            choices: ['16Gbps' , '8Gbps' , '32Gbps' , 'Auto']
            default: 16Gbps
            type: str
          vsan_id:
            description:
              -  Virtual San Identifier associated to the FC port.
            type: int
      fcoe_uplink_spec:
        description: FCoE Uplink port role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          fec:
            description:
              -  Forward error correction configuration for the port.
              -  Auto - Forward error correction option 'Auto'.
              -  Cl91 - Forward error correction option 'cl91'.
              -  Cl74 - Forward error correction option 'cl74'.
            choices: ['Auto' , 'Cl91' , 'Cl74']
            default: Auto
            type: str
          link_control_policy:
            description:
              -  A reference to a fabriclink_control_policy resource.
            type: str
      eth_uplink_spec:
        description: Ethernet Uplink port role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          fec:
            description:
              -  Forward error correction configuration for the port.
              -  Auto - Forward error correction option 'Auto'.
              -  Cl91 - Forward error correction option 'cl91'.
              -  Cl74 - Forward error correction option 'cl74'.
            choices: ['Auto' , 'Cl91' , 'Cl74']
            default: Auto
            type: str
          eth_network_group_policy:
            description:
              -  name of the eth_network_group_policy resources.
            type: str
          flow_control_policy:
            description:
              -  name of the fabricflow_control_policy resource.
            type: str
          link_control_policy:
            description:
              -  name of the fabriclink_control_policy resource.
            type: str
  port_channels:
    description: Port Channel configuration for the switch
    type: list
    elements: dict
    suboptions:
      port_channel_role_type:
        description:  Role type of the port channel.
        type: str
        choices: ['Appliance' , 'EthernetUplink', 'FcUplink', 'FcoeUplink']
        required: true
      pc_id:
        description:
          -  Unique Identifier of the port-channel, local to this switch.
        type: int
      port_id_end:
        description: Ending range of the Port Identifier.
        type: int
      port_id_start:
        description: Starting range of the Port Identifier.
        type: int
      slot_id:
        description: Slot Identifier of the switch.
        type: int
      aggregate_port_id:
        description:
          -  Breakout port Identifier of the Switch Interface.
          - When a port is not configured as a breakout port, the aggregatePortId is set to 0, and unused.
          - When a port is configured as a breakout port, the 'aggregatePortId' port number as labeled on the equipment,
          - e.g. the id of the port on the switch.
        type: int
        default: 0
      appliance_pc_spec:
        description: Appliance port channel role specification
        type: dict
        suboptions:
          mode:
            description:
              -  Port mode to be set on the appliance port.
              -  trunk - Trunk mode Switch Port Type.
              -  access - Access mode Switch Port Type.
            choices: ['trunk' , 'access']
            default: trunk
            type: str
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          priority:
            description:
              -  The 'name' of the System QoS Class.
              -  Best Effort - QoS priority for Best-effort traffic.
              -  FC - QoS priority for FC traffic.
              -  Platinum - QoS priority for Platinum traffic.
              -  Gold - QoS priority for Gold traffic.
              -  Silver - QoS priority for Silver traffic.
              -  Bronze - QoS priority for Bronze traffic.
            choices: ['Best Effort' , 'FC' , 'Platinum' , 'Gold' , 'Silver' , 'Bronze']
            default: Best Effort
            type: str
          eth_network_control_policy:
            description:
              -  A reference to a ethernet network control policy resource.
            type: str
          eth_network_group_policy:
            description:
              -  A reference to a ethernet network group policy resource.
            type: str
          link_aggregation_policy:
            description:
              -  A reference to a link aggregation policy resource.
            type: str
      fc_uplink_pc_spec:
        description: FC Uplink port channel role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  16Gbps - Admin configurable speed 16Gbps.
              -  8Gbps - Admin configurable speed 8Gbps.
              -  32Gbps - Admin configurable speed 32Gbps.
              -  Auto - Admin configurable speed AUTO ( default ).
            choices: ['16Gbps' , '8Gbps' , '32Gbps' , 'Auto']
            default: 16Gbps
            type: str
          vsan_id:
            description:
              -  Virtual San Identifier associated to the FC port.
            type: int
      fcoe_uplink_pc_spec:
        description: FCoE Uplink port channel role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          link_control_policy:
            description:
              -  A reference to a link control policy resource.
            type: str
          link_aggregation_policy:
            description:
              -  A reference to a fabriclink_aggregation_policy resource.
            type: str
      eth_uplink_pc_spec:
        description: Ethernet Uplink port channel role specification
        type: dict
        suboptions:
          admin_speed:
            description:
              -  Admin configured speed for the port.
              -  Auto - Admin configurable speed AUTO ( default ).
              -  1Gbps - Admin configurable speed 1Gbps.
              -  10Gbps - Admin configurable speed 10Gbps.
              -  25Gbps - Admin configurable speed 25Gbps.
              -  40Gbps - Admin configurable speed 40Gbps.
              -  100Gbps - Admin configurable speed 100Gbps.
            choices: ['Auto' , '1Gbps' , '10Gbps' , '25Gbps' , '40Gbps' , '100Gbps']
            default: Auto
            type: str
          flow_control_policy:
            description:
              -  A reference to a flow control policy resource.
            type: str
          eth_network_group_policy:
            description:
              -  A reference to a ethernet network group policy resource.
            type: str
          link_control_policy:
            description:
              -  A reference to a link control policy resource.
            type: str
          link_aggregation_policy:
            description:
              -  A reference to a fabriclink_aggregation_policy resource.
            type: str
  pin_groups:
    description: pin groups configuration for the switch
    type: list
    elements: dict
    suboptions:
      name:
        description: The name of the pin group.
        type: str
      type:
        description: The type of the pin group.
        type: str
        choices: ['LAN', 'SAN']
      pin_target_interface_type:
        description: The type of the pin target interface.
        type: str
        choices: ['Port', 'PortChannel']
      port_spec:
        description: The port specification for the target port.
        type: dict
        suboptions:
          port_id:
            description: The end port identifier.
            type: int
          slot_id:
            description: The slot identifier.
            type: int
          aggregate_port_id:
            description: The aggregate port identifier.
            type: int
            default: 0
          port_role:
            description: The role of the port.
            type: str
            choices: ['EthernetUplink', 'FcUplink', 'FcoeUplink']
      port_channel_spec:
        description: The port channel specification for the target port.
        type: dict
        suboptions:
          pc_id:
            description: The port channel identifier.
            type: int
          pc_role:
            description: The role of the port channel.
            type: str
            choices: ['EthernetUplink', 'FcUplink', 'FcoeUplink']
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Fabric Port Policy
  cisco.intersight.intersight_fabric_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FPP
    description: Fabric Port policy for COS
    tags:
      - Key: Site
        Value: RCDN
    device_model: UCS-FI-6454
    port_modes:
      - custom_mode: FibreChannel
        port_id_end: 10
        port_id_start: 1
        slot_id: 1
      - custom_mode: BreakoutEthernet10G
        port_id_end: 50
        port_id_start: 49
        slot_id: 1
    port_roles:
      - port_role: Appliance
        port_id_end: 10
        port_id_start: 8
        slot_id: 1
        aggregate_port_id: 0
        appliance_spec:
          mode: trunk
          priority: Best Effort
          eth_network_control_policy: COS-ENC
          eth_network_group_policy: COS-ENG
    port_channels:
      - port_channel_role_type: Appliance
        pc_id: 1
        port_id_end: 10
        port_id_start: 8
        slot_id: 1
        aggregate_port_id: 0
        appliance_pc_spec:
          mode: trunk
          admin_speed: Auto
          priority: Best Effort
          eth_network_control_policy: COS-ENC
          eth_network_group_policy: COS-ENG
          link_aggregation_policy: COS-LAP
    pin_groups:
      - name: MY-PIN-GROUP1
        type: LAN
        pin_target_interface_type: Port
        port_spec:
          port_id: 1
          slot_id: 1
          aggregate_port_id: 0
          port_role: EthernetUplink


- name: Delete Fabric Port Policy
  cisco.intersight.intersight_fabric_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-FPP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-FPP",
        "ObjectType": "fabric.PortPolicy",
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


# checks if the property is present in the params and adds it to the api_body
def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        if params[prop_key]:
            api_body[prop] = params[prop_key]


# checks if the policy moid is present in the params and adds it to the api_body
def check_and_add_prop_policy(prop, prop_key, params, api_body):
    api_body[prop] = {}
    for key in params.keys():
        if params[key]:
            api_body[prop][key] = params[key]


# checks if the property is present in the params and adds it to the api_body as an array
def check_and_add_prop_policy_toarray(prop, prop_key, params, api_body):
    api_body[prop] = []
    item_dict = {}
    for key in params.keys():
        if params[key]:
            item_dict[key] = params[key]
    api_body[prop].append(item_dict)


def main():

    port_modes_spec = dict(
        custom_mode={
            "type": "str",
            "choices": [
                'FibreChannel',
                'BreakoutEthernet10G',
                'BreakoutEthernet25G',
                'BreakoutFibreChannel8G',
                'BreakoutFibreChannel16G',
                'BreakoutFibreChannel32G'
            ],
            "default": "FibreChannel"
        },
        port_id_end={"type": "int"},
        port_id_start={"type": "int"},
        slot_id={"type": "int"},
    )

    appliance_specification = dict(
        mode={"type": "str", "choices": ['trunk', 'access'], "default": "trunk"},
        priority={"type": "str", "choices": ['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze'], "default": "Best Effort"},
        admin_speed={"type": "str", "choices": ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], "default": "Auto"},
        fec={"type": "str", "choices": ['Auto', 'Cl91', 'Cl74'], "default": "Auto"},
        eth_network_control_policy={"type": "str"},
        eth_network_group_policy={"type": "str"},
    )

    server_specification = dict(
        auto_negotiation_disabled={
            "type": "bool",
            "default": False
        },
        fec={
            "type": "str",
            "choices": [
                'Auto',
                'Cl91',
                'Cl74'
            ],
            "default": "Auto"
        },

    )

    fc_uplink_or_storage_specification = dict(
        admin_speed={
            "type": "str",
            "choices": [
                '16Gbps',
                '8Gbps',
                '32Gbps',
                'Auto'
            ],
            "default": "16Gbps"
        },
        vsan_id={"type": "int"},
    )

    fcoe_uplink_specificaiton = dict(
        admin_speed={
            "type": "str",
            "choices": [
                'Auto',
                '1Gbps',
                '10Gbps',
                '25Gbps',
                '40Gbps',
                '100Gbps'
            ],
            "default": "Auto"
        },
        fec={
            "type": "str",
            "choices": [
                'Auto',
                'Cl91',
                'Cl74'
            ],
            "default": "Auto"
        },
        link_control_policy={"type": "str"},
    )

    eth_uplink_specification = dict(
        admin_speed={
            "type": "str",
            "choices": [
                'Auto',
                '1Gbps',
                '10Gbps',
                '25Gbps',
                '40Gbps',
                '100Gbps'
            ],
            "default": "Auto"
        },
        fec={
            "type": "str",
            "choices": [
                'Auto',
                'Cl91',
                'Cl74'
            ],
            "default": "Auto"
        },
        eth_network_group_policy={"type": "str"},
        flow_control_policy={"type": "str"},
        link_control_policy={"type": "str"},
    )

    port_roles_spec = dict(
        port_role={"type": "str", "choices": ['Appliance' , 'EthernetUplink', 'FcUplink', 'FcoeUplink', 'FcStorage', 'Server'], "required": True},
        port_id_end={"type": "int"},
        port_id_start={"type": "int"},
        slot_id={"type": "int"},
        aggregate_port_id={"type": "int", "default": 0},
        appliance_spec={"type": "dict", "options": appliance_specification},
        server_spec={"type": "dict", "options": server_specification},
        fc_storage_spec={"type": "dict", "options": fc_uplink_or_storage_specification},
        fc_uplink_spec={"type": "dict", "options": fc_uplink_or_storage_specification},
        fcoe_uplink_spec={"type": "dict", "options": fcoe_uplink_specificaiton},
        eth_uplink_spec={"type": "dict", "options": eth_uplink_specification},
    )

    appliance_pc_specification = dict(
        mode={"type": "str", "choices": ['trunk', 'access'], "default": "trunk"},
        admin_speed={"type": "str", "choices": ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], "default": "Auto"},
        priority={"type": "str", "choices": ['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze'], "default": "Best Effort"},
        eth_network_control_policy={"type": "str"},
        eth_network_group_policy={"type": "str"},
        link_aggregation_policy={"type": "str"},
    )

    fc_uplink_pc_specification = dict(
        admin_speed={"type": "str", "choices": ['16Gbps', '8Gbps', '32Gbps', 'Auto'], "default": "16Gbps"},
        vsan_id={"type": "int"},
    )

    fcoe_pc_specificaiton = dict(
        admin_speed={"type": "str", "choices": ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], "default": "Auto"},
        link_control_policy={"type": "str"},
        link_aggregation_policy={"type": "str"},
    )

    eth_pc_specification = dict(
        admin_speed={"type": "str", "choices": ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], "default": "Auto"},
        flow_control_policy={"type": "str"},
        eth_network_group_policy={"type": "str"},
        link_control_policy={"type": "str"},
        link_aggregation_policy={"type": "str"},
    )

    port_channel_roles_spec = dict(
        port_channel_role_type={"type": "str", "choices": ['Appliance' , 'EthernetUplink', 'FcUplink', 'FcoeUplink'], "required": True},
        pc_id={"type": "int"},
        port_id_end={"type": "int"},
        port_id_start={"type": "int"},
        slot_id={"type": "int"},
        aggregate_port_id={"type": "int", "default": 0},
        appliance_pc_spec={"type": "dict", "options": appliance_pc_specification},
        fc_uplink_pc_spec={"type": "dict", "options": fc_uplink_pc_specification},
        fcoe_uplink_pc_spec={"type": "dict", "options": fcoe_pc_specificaiton},
        eth_uplink_pc_spec={"type": "dict", "options": eth_pc_specification}
    )

    pin_groups_spec = dict(
        name={"type": "str"},
        type={"type": "str", "choices": ['LAN', 'SAN']},
        pin_target_interface_type={"type": "str", "choices": ['Port', 'PortChannel']},
        port_spec={"type": "dict", "options": {
            "port_id": {"type": "int"},
            "slot_id": {"type": "int"},
            "aggregate_port_id": {"type": "int", "default": 0},
            "port_role": {"type": "str", "choices": ['EthernetUplink', 'FcUplink', 'FcoeUplink']},
        }},
        port_channel_spec={"type": "dict", "options": {
            "pc_id": {"type": "int"},
            "pc_role": {"type": "str", "choices": ['EthernetUplink', 'FcUplink', 'FcoeUplink']},

        }}
    )

    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        device_model={
            "type": "str",
            "choices": [
                'UCS-FI-6454',
                'UCS-FI-64108',
                'UCS-FI-6536',
                'unknown'
            ],
            "default": "UCS-FI-6454"
        },
        port_modes={"type": "list", "elements": "dict", "options": port_modes_spec},
        port_roles=dict(
            type="list",
            elements="dict",
            options=port_roles_spec,
            required_if=[
                ('port_role', 'Appliance', ('appliance_spec', ), False),
                ('port_role', 'Server', ('server_spec', ), False),
                ('port_role', 'FcStorage', ('fc_storage_spec', ), False),
                ('port_role', 'FcUplink', ('fc_uplink_spec', ), False),
                ('port_role', 'FcoeUplink', ('fcoe_uplink_spec', ), False),
                ('port_role', 'EthernetUplink', ('eth_uplink_spec', ), False)
            ]
        ),
        port_channels={
            "type": "list",
            "elements": "dict",
            "options": port_channel_roles_spec,
            "required_if": [
                ('port_channel_role_type', 'Appliance', ('appliance_pc_spec', ), False),
                ('port_channel_role_type', 'FcUplink', ('fc_uplink_pc_spec', ), False),
                ('port_channel_role_type', 'FcoeUplink', ('fcoe_uplink_pc_spec', ), False),
                ('port_channel_role_type', 'EthernetUplink', ('eth_uplink_pc_spec', ), False)
            ]
        },
        pin_groups={
            "type": "list",
            "elements": "dict",
            "options": pin_groups_spec,
            "required_if": [
                ('pin_target_interface_type', 'Port', ('port_spec', ), False),
                ('pin_target_interface_type', 'PortChannel', ('port_channel_spec', ), False)
            ]
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
    resource_path = '/fabric/PortPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('DeviceModel', 'device_model', intersight.module.params, intersight.api_body)

    # create/update Port Policy if state is present
    if intersight.module.params['state'] == 'present':
        intersight.configure_policy_or_profile(resource_path=resource_path)
        if intersight.result['api_response'].get('Moid'):
            port_policy = {"Moid": intersight.result['api_response'].get('Moid')}
        else:
            module.fail_json(msg="Port Policy not found")
    elif intersight.module.params['state'] == 'absent':
        # don't delete the port policy before deleting the other port configuraitons
        port_policy = get_policy_ref(intersight, intersight.module.params['name'], resource_path)
        if not port_policy['Moid']:
            # policy does not exist
            module.exit_json(**intersight.result)
    #
    # Configure Port Mode
    #
    if 'port_modes' in intersight.module.params:
        port_modes = intersight.module.params['port_modes']
        if port_modes and intersight.module.params['state'] == 'present':
            configure_port_modes(module, intersight, port_policy, port_modes)
    if 'port_roles' in intersight.module.params:
        port_roles = intersight.module.params['port_roles']
        if port_roles and intersight.module.params['state'] == 'present':
            configure_port_roles(module, intersight, port_policy, port_roles)
    if 'port_channels' in intersight.module.params:
        port_channels = intersight.module.params['port_channels']
        if port_channels and intersight.module.params['state'] == 'present':
            configure_port_channels(module, intersight, port_policy, port_channels)
    if 'pin_groups' in intersight.module.params:
        pin_groups = intersight.module.params['pin_groups']
        if pin_groups and intersight.module.params['state'] == 'present':
            configure_pin_groups(module, intersight, port_policy, pin_groups)

    if intersight.module.params['state'] == 'absent':
        # first delete pin groups, port channels, port roles and then modes
        if pin_groups:
            configure_pin_groups(module, intersight, port_policy, pin_groups)
        if port_channels:
            configure_port_channels(module, intersight, port_policy, port_channels)
        if port_roles:
            configure_port_roles(module, intersight, port_policy, port_roles)
        if port_modes:
            configure_port_modes(module, intersight, port_policy, port_modes)
        # yes now is the time to delete the port policy
        intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


def configure_pin_groups(module, intersight, port_policy, pin_groups):
    for pin_group in pin_groups:
        interface_role = {}
        if pin_group['pin_target_interface_type'] == 'Port':
            port_spec = pin_group['port_spec']
            interface_role = get_interface_role_from_port_specification(intersight, port_spec, port_policy)
        elif pin_group['pin_target_interface_type'] == 'PortChannel':
            port_channel_spec = pin_group['port_channel_spec']
            interface_role = get_interface_role_from_port_channel_specification(intersight, port_channel_spec, port_policy)
        process_pin_group_specification(intersight, pin_group['name'], pin_group['type'], interface_role, port_policy)


def get_interface_role_from_port_specification(intersight, port_spec, port_policy):
    if port_spec['port_role'] == 'EthernetUplink':
        resource_path = '/fabric/UplinkRoles'
    elif port_spec['port_role'] == 'FcUplink':
        resource_path = '/fabric/FcUplinkRoles'
    elif port_spec['port_role'] == 'FcoeUplink':
        resource_path = '/fabric/FcoeUplinkRoles'

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_spec['port_id']) + " "
    filter_str += "and AggregatePortId eq " + str(port_spec['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_spec['slot_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    moid = ''
    object_type = ''
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        moid = intersight.result['api_response']['Moid']
        object_type = intersight.result['api_response']['ObjectType']

    return {"Moid": moid, "ObjectType": object_type}


def get_interface_role_from_port_channel_specification(intersight, port_channel_spec, port_policy):
    if port_channel_spec['pc_role'] == 'EthernetUplink':
        resource_path = '/fabric/UplinkPcRoles'
    elif port_channel_spec['pc_role'] == 'FcUplink':
        resource_path = '/fabric/FcUplinkPcRoles'
    elif port_channel_spec['pc_role'] == 'FcoeUplink':
        resource_path = '/fabric/FcoeUplinkPcRoles'

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Get the current state of the resource
    filter_str = "PcId eq " + str(port_channel_spec['pc_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"
    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    moid = ''
    object_type = ''
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        moid = intersight.result['api_response']['Moid']
        object_type = intersight.result['api_response']['ObjectType']

    return {"Moid": moid, "ObjectType": object_type}


def process_pin_group_specification(intersight, name, type, interface_role, port_policy):
    resource_path = ''
    if type == 'LAN':
        resource_path = '/fabric/LanPinGroups'
    elif type == 'SAN':
        resource_path = '/fabric/SanPinGroups'

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    intersight.api_body = {
        'Name': name
    }
    check_and_add_prop_policy('PinTargetInterfaceRole', 'PinTargetInterfaceRole', interface_role, intersight.api_body)
    check_and_add_prop_policy('PortPolicy', 'PortPolicy', port_policy, intersight.api_body)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Get the current state of the resource
    filter_str = "Name eq '" + name + "' "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"
    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def configure_port_channels(module, intersight, port_policy, port_channels):
    for port_channel in port_channels:
        port_id_start = port_channel['port_id_start']
        port_id_end = port_channel['port_id_end']
        if port_id_start > port_id_end:
            module.fail_json(msg="Port Id Start should be less than Port Id End")

        if port_channel['port_channel_role_type'] == 'Appliance':
            eth_network_control_policy = get_policy_ref(intersight,
                                                        port_channel['appliance_pc_spec']['eth_network_control_policy'],
                                                        '/fabric/EthNetworkControlPolicies')
            if not eth_network_control_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Eth Network Control Policy not found")
            eth_network_group_policy = get_policy_ref(intersight,
                                                      port_channel['appliance_pc_spec']['eth_network_group_policy'],
                                                      '/fabric/EthNetworkGroupPolicies')
            if not eth_network_group_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Eth Network Group Policy not found")
            link_aggregation_policy = get_policy_ref(intersight,
                                                     port_channel['appliance_pc_spec']['link_aggregation_policy'],
                                                     '/fabric/LinkAggregationPolicies')
            if not link_aggregation_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Link Aggregation Policy not found")
            process_appliance_pc_specification(intersight, port_id_start, port_id_end, port_channel, port_policy, eth_network_control_policy,
                                               eth_network_group_policy, link_aggregation_policy)
        elif port_channel['port_channel_role_type'] == 'FcUplink':
            process_fc_pc_specification(intersight, port_id_start, port_id_end, port_channel, port_policy)
        elif port_channel['port_channel_role_type'] == 'FcoeUplink':
            link_control_policy = get_policy_ref(
                intersight,
                port_channel['fcoe_uplink_pc_spec']['link_control_policy'],
                '/fabric/LinkControlPolicies'
            )
            if not link_control_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Link Control Policy not found")
            link_aggregation_policy = get_policy_ref(
                intersight,
                port_channel['fcoe_uplink_pc_spec']['link_aggregation_policy'],
                '/fabric/LinkAggregationPolicies'
            )
            if not link_aggregation_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Link Aggregation Policy not found")
            process_fcoe_uplink_pc_specification(intersight,
                                                 port_id_start,
                                                 port_id_end,
                                                 port_channel,
                                                 port_policy,
                                                 link_control_policy,
                                                 link_aggregation_policy)
        elif port_channel['port_channel_role_type'] == 'EthernetUplink':
            eth_network_group_policy = get_policy_ref(
                intersight,
                port_channel['eth_uplink_pc_spec']['eth_network_group_policy'],
                '/fabric/EthNetworkGroupPolicies'
            )
            if not eth_network_group_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Eth Network Group Policy not found")
            flow_control_policy = get_policy_ref(
                intersight,
                port_channel['eth_uplink_pc_spec']['flow_control_policy'],
                '/fabric/FlowControlPolicies'
            )
            if not flow_control_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Flow Control Policy not found")
            link_aggregation_policy = get_policy_ref(
                intersight,
                port_channel['eth_uplink_pc_spec']['link_aggregation_policy'],
                '/fabric/LinkAggregationPolicies'
            )
            if not link_aggregation_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Link Aggregation Policy not found")
            link_control_policy = get_policy_ref(
                intersight,
                port_channel['eth_uplink_pc_spec']['link_control_policy'],
                '/fabric/LinkControlPolicies'
            )
            if not link_control_policy['Moid']:
                # policy does not exist
                module.fail_json(**intersight.result, msg="Link Control Policy not found")
            process_eth_uplink_pc_specification(
                intersight,
                port_id_start, port_id_end,
                port_channel, port_policy,
                eth_network_group_policy, flow_control_policy,
                link_aggregation_policy, link_control_policy
            )


def process_eth_uplink_pc_specification(intersight,
                                        port_id_start, port_id_end,
                                        port_channel, port_policy,
                                        eth_network_group_policy, flow_control_policy,
                                        link_aggregation_policy, link_control_policy):
    resource_path = '/fabric/UplinkPcRoles'
    eth_uplink_pc_spec = port_channel['eth_uplink_pc_spec']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    intersight.api_body = {
        'Tags': intersight.module.params['tags'],
    }

    check_and_add_prop("PcId", "pc_id", port_channel, intersight.api_body)
    check_and_add_prop('AdminSpeed', 'admin_speed', eth_uplink_pc_spec, intersight.api_body)
    check_and_add_prop_policy('FlowControlPolicy', 'flow_control_policy', flow_control_policy, intersight.api_body)
    check_and_add_prop_policy_toarray('EthNetworkGroupPolicy', 'eth_network_group_policy', eth_network_group_policy, intersight.api_body)
    check_and_add_prop_policy('LinkAggregationPolicy', 'link_aggregation_policy', link_aggregation_policy, intersight.api_body)
    check_and_add_prop_policy('LinkControlPolicy', 'link_control_policy', link_control_policy, intersight.api_body)
    check_and_add_ports(intersight, port_id_start, port_id_end, port_channel['slot_id'], port_channel['aggregate_port_id'])
    check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PcId eq " + str(port_channel['pc_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_fcoe_uplink_pc_specification(intersight,
                                         port_id_start, port_id_end,
                                         port_channel, port_policy,
                                         link_control_policy, link_aggregation_policy):
    resource_path = '/fabric/FcoeUplinkPcRoles'
    fcoe_uplink_pc_spec = port_channel['fcoe_uplink_pc_spec']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    intersight.api_body = {
        'Tags': intersight.module.params['tags'],
    }

    check_and_add_prop("PcId", "pc_id", port_channel, intersight.api_body)
    check_and_add_prop('AdminSpeed', 'admin_speed', fcoe_uplink_pc_spec, intersight.api_body)
    check_and_add_prop_policy('LinkControlPolicy', 'link_control_policy', link_control_policy, intersight.api_body)
    check_and_add_prop_policy('LinkAggregationPolicy', 'link_aggregation_policy', link_aggregation_policy, intersight.api_body)
    check_and_add_ports(intersight, port_id_start, port_id_end, port_channel['slot_id'], port_channel['aggregate_port_id'])
    check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PcId eq " + str(port_channel['pc_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_fc_pc_specification(intersight, port_id_start, port_id_end, port_channel, port_policy):
    resource_path = '/fabric/FcUplinkPcRoles'
    fc_uplink_pc_spec = port_channel['fc_uplink_pc_spec']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    intersight.api_body = {
        'Tags': intersight.module.params['tags'],
    }

    check_and_add_prop("PcId", "pc_id", port_channel, intersight.api_body)
    check_and_add_prop('AdminSpeed', 'admin_speed', fc_uplink_pc_spec, intersight.api_body)
    check_and_add_prop('VsanId', 'vsan_id', fc_uplink_pc_spec, intersight.api_body)
    check_and_add_ports(intersight, port_id_start, port_id_end, port_channel['slot_id'], port_channel['aggregate_port_id'])
    check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PcId eq " + str(port_channel['pc_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_appliance_pc_specification(intersight,
                                       port_id_start, port_id_end,
                                       port_channel, port_policy,
                                       eth_network_control_policy, eth_network_group_policy,
                                       link_aggregation_policy):
    resource_path = '/fabric/AppliancePcRoles'
    appliance_pc_spec = port_channel['appliance_pc_spec']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    intersight.api_body = {
        'Tags': intersight.module.params['tags'],
    }

    check_and_add_prop("PcId", "pc_id", port_channel, intersight.api_body)
    check_and_add_prop('Mode', 'mode', appliance_pc_spec, intersight.api_body)
    check_and_add_prop('AdminSpeed', 'admin_speed', appliance_pc_spec, intersight.api_body)
    check_and_add_prop('Priority', 'priority', appliance_pc_spec, intersight.api_body)
    check_and_add_prop_policy('EthNetworkControlPolicy', 'eth_network_control_policy', eth_network_control_policy, intersight.api_body)
    check_and_add_prop_policy('EthNetworkGroupPolicy', 'eth_network_group_policy', eth_network_group_policy, intersight.api_body)
    check_and_add_prop_policy('LinkAggregationPolicy', 'link_aggregation_policy', link_aggregation_policy, intersight.api_body)
    check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)
    check_and_add_ports(intersight, port_id_start, port_id_end, port_channel['slot_id'], port_channel['aggregate_port_id'])
    # Get the current state of the resource
    filter_str = "PcId eq " + str(port_channel['pc_id']) + " "
    filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def check_and_add_ports(intersight, port_id_start, port_id_end, slot_id, aggregate_port_id):
    intersight.api_body['Ports'] = []
    for port_id in range(port_id_start, port_id_end + 1):
        intersight.api_body['Ports'].append({
            'PortId': port_id,
            'SlotId': slot_id,
            'AggregatePortId': aggregate_port_id
        })


def configure_port_modes(module, intersight, port_policy, port_modes):
    resource_path = '/fabric/PortModes'
    for port_mode in port_modes:
        intersight.result['api_response'] = {}
        intersight.result['trace_id'] = ''

        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('CustomMode', 'custom_mode', port_mode, intersight.api_body)
        check_and_add_prop('PortIdEnd', 'port_id_end', port_mode, intersight.api_body)
        check_and_add_prop('PortIdStart', 'port_id_start', port_mode, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_mode, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)

        # Get the current state of the resource
        filter_str = "PortIdStart eq " + str(port_mode['port_id_start']) + " "
        filter_str += "and PortIdEnd eq " + str(port_mode['port_id_end']) + " "
        filter_str += "and PortPolicy.Moid eq '" + port_policy['Moid'] + "'"

        intersight.get_resource(
            resource_path=resource_path,
            query_params={
                '$filter': filter_str,
            }
        )
        check_and_add_resource(intersight, resource_path)


def configure_port_roles(module, intersight, port_policy, port_roles):
    for port_role in port_roles:
        port_id_start = port_role['port_id_start']
        port_id_end = port_role['port_id_end']

        if port_id_start > port_id_end:
            module.fail_json(msg="Port Id Start should be less than Port Id End")

        for port_id in range(port_id_start, port_id_end + 1):
            if port_role['port_role'] == 'Appliance':
                eth_network_control_policy = get_policy_ref(intersight,
                                                            port_role['appliance_spec']['eth_network_control_policy'],
                                                            '/fabric/EthNetworkControlPolicies')
                if not eth_network_control_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Eth Network Control Policy not found")

                eth_network_group_policy = get_policy_ref(intersight, port_role['appliance_spec']['eth_network_group_policy'],
                                                          '/fabric/EthNetworkGroupPolicies')
                if not eth_network_group_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Eth Network Group Policy not found")
                process_appliance_specification(intersight, port_id, port_role, port_policy, eth_network_control_policy, eth_network_group_policy)
            elif port_role['port_role'] == 'Server':
                process_server_specification(intersight, port_id, port_role, port_policy)
            elif port_role['port_role'] == 'FcStorage':
                process_fc_uplink_or_storage_specification(intersight, port_id, port_role, port_policy, port_role['fc_storage_spec'], '/fabric/FcStorageRoles')
            elif port_role['port_role'] == 'FcUplink':
                process_fc_uplink_or_storage_specification(intersight, port_id, port_role, port_policy, port_role['fc_uplink_spec'], '/fabric/FcUplinkRoles')
            elif port_role['port_role'] == 'FcoeUplink':
                link_control_policy = get_policy_ref(intersight, port_role['fcoe_uplink_spec']['link_control_policy'], '/fabric/LinkControlPolicies')
                if not link_control_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Link Control Policy not found")
                process_fcoe_uplink_specification(intersight, port_id, port_role, port_policy, link_control_policy)
            elif port_role['port_role'] == 'EthernetUplink':
                eth_network_group_policy = get_policy_ref(intersight,
                                                          port_role['eth_uplink_spec']['eth_network_group_policy'],
                                                          '/fabric/EthNetworkGroupPolicies')
                if not eth_network_group_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Eth Network Group Policy not found")
                flow_control_policy = get_policy_ref(intersight, port_role['eth_uplink_spec']['flow_control_policy'], '/fabric/FlowControlPolicies')
                if not flow_control_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Flow Control Policy not found")
                link_control_policy = get_policy_ref(intersight, port_role['eth_uplink_spec']['link_control_policy'], '/fabric/LinkControlPolicies')
                if not link_control_policy['Moid']:
                    # policy does not exist
                    module.fail_json(**intersight.result, msg="Link Control Policy not found")
                process_eth_uplink_specification(intersight,
                                                 port_id, port_role, port_policy,
                                                 eth_network_group_policy, flow_control_policy,
                                                 link_control_policy)


def process_eth_uplink_specification(intersight, port_id, port_role, port_policy, eth_network_group_policy, flow_control_policy, link_control_policy):
    resource_path = '/fabric/UplinkRoles'
    eth_uplink_spec = port_role['eth_uplink_spec']

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present':
        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('PortId', 'port_id', {'port_id': port_id}, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_role, intersight.api_body)
        check_and_add_prop('AggregatePortId', 'aggregate_port_id', port_role, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)
        check_and_add_prop('AdminSpeed', 'admin_speed', eth_uplink_spec, intersight.api_body)
        check_and_add_prop('Fec', 'fec', eth_uplink_spec, intersight.api_body)
        check_and_add_prop_policy_toarray('EthNetworkGroupPolicy', 'eth_network_group_policy', eth_network_group_policy, intersight.api_body)
        check_and_add_prop_policy('FlowControlPolicy', 'flow_control_policy', flow_control_policy, intersight.api_body)
        check_and_add_prop_policy('LinkControlPolicy', 'link_control_policy', link_control_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_id) + " "
    filter_str += "and AggregatePortId eq " + str(port_role['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_role['slot_id']) + " "
    filter_str += "and Parent.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_fcoe_uplink_specification(intersight, port_id, port_role, port_policy, link_control_policy):
    resource_path = '/fabric/FcoeUplinkRoles'
    fcoe_uplink_spec = port_role['fcoe_uplink_spec']

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present':
        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('PortId', 'port_id', {'port_id': port_id}, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_role, intersight.api_body)
        check_and_add_prop('AggregatePortId', 'aggregate_port_id', port_role, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)
        check_and_add_prop('AdminSpeed', 'admin_speed', fcoe_uplink_spec, intersight.api_body)
        check_and_add_prop('Fec', 'fec', fcoe_uplink_spec, intersight.api_body)
        check_and_add_prop_policy('LinkControlPolicy', 'link_control_policy', link_control_policy
                                  , intersight.api_body)

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_id) + " "
    filter_str += "and AggregatePortId eq " + str(port_role['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_role['slot_id']) + " "
    filter_str += "and Parent.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_fc_uplink_or_storage_specification(intersight, port_id, port_role, port_policy, fc_spec, resource_path):
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present':
        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('PortId', 'port_id', {'port_id': port_id}, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_role, intersight.api_body)
        check_and_add_prop('AggregatePortId', 'aggregate_port_id', port_role, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)
        check_and_add_prop('AdminSpeed', 'admin_speed', fc_spec, intersight.api_body)
        check_and_add_prop('VsanId', 'vsan_id', fc_spec, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_id) + " "
    filter_str += "and AggregatePortId eq " + str(port_role['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_role['slot_id']) + " "
    filter_str += "and Parent.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_server_specification(intersight, port_id, port_role, port_policy):
    resource_path = '/fabric/ServerRoles'
    server_spec = port_role['server_spec']

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present':
        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('PortId', 'port_id', {'port_id': port_id}, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_role, intersight.api_body)
        check_and_add_prop('AggregatePortId', 'aggregate_port_id', port_role, intersight.api_body)
        check_and_add_prop('AutoNegotiationDisabled', 'auto_negotiation_disabled', server_spec, intersight.api_body)
        check_and_add_prop('Fec', 'fec', server_spec, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_id) + " "
    filter_str += "and AggregatePortId eq " + str(port_role['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_role['slot_id']) + " "
    filter_str += "and Parent.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


def process_appliance_specification(intersight, port_id, port_role, port_policy, eth_network_control_policy, eth_network_group_policy):
    resource_path = '/fabric/ApplianceRoles'
    appliance_spec = port_role['appliance_spec']

    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    if intersight.module.params['state'] == 'present':
        intersight.api_body = {
            'Tags': intersight.module.params['tags'],
        }
        check_and_add_prop('PortId', 'port_id', {'port_id': port_id}, intersight.api_body)
        check_and_add_prop('SlotId', 'slot_id', port_role, intersight.api_body)
        check_and_add_prop('AggregatePortId', 'aggregate_port_id', port_role, intersight.api_body)
        check_and_add_prop_policy('PortPolicy', 'port_policy', port_policy, intersight.api_body)
        check_and_add_prop('Mode', 'mode', appliance_spec, intersight.api_body)
        check_and_add_prop('Priority', 'priority', appliance_spec, intersight.api_body)
        check_and_add_prop('AdminSpeed', 'admin_speed', appliance_spec, intersight.api_body)
        check_and_add_prop('Fec', 'fec', appliance_spec, intersight.api_body)
        check_and_add_prop_policy('EthNetworkControlPolicy', 'eth_network_control_policy', eth_network_control_policy, intersight.api_body)
        check_and_add_prop_policy('EthNetworkGroupPolicy', 'eth_network_group_policy', eth_network_group_policy, intersight.api_body)

    # Get the current state of the resource
    filter_str = "PortId eq " + str(port_id) + " "
    filter_str += "and AggregatePortId eq " + str(port_role['aggregate_port_id']) + " "
    filter_str += "and SlotId eq " + str(port_role['slot_id']) + " "
    filter_str += "and Parent.Moid eq '" + port_policy['Moid'] + "'"

    intersight.get_resource(
        resource_path=resource_path,
        query_params={
            '$filter': filter_str,
        }
    )
    check_and_add_resource(intersight, resource_path)


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


def check_and_add_resource(intersight, resource_path):
    res_moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        res_moid = intersight.result['api_response']['Moid']
        if intersight.module.params['state'] == 'present' :
            resource_values_match = (intersight.api_body, intersight.result['api_response'])
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    if intersight.module.params['state'] == 'present' and not resource_values_match:
        intersight.configure_resource(moid=res_moid, resource_path=resource_path, body=intersight.api_body, query_params=None)
    elif intersight.module.params['state'] == 'absent':
        if res_moid:
            intersight.delete_resource(moid=res_moid, resource_path=resource_path)
            res_moid = None


if __name__ == '__main__':
    main()
