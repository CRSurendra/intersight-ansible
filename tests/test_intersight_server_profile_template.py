import configparser
import json

import unittest
import pytest
from unittest.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from plugins.modules import intersight_server_profile_template


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

class TesIntersightServerProfileTemplate(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('./intersight-ansible/tests/test_config.ini')
        self.api_key_id = config['vars']['api_key_id']
        self.api_private_key_path = config['vars']['api_private_key']
        self.organization = config['vars']['organization']
        self.boot_order_policy = config['vars']['boot_order_policy']
        self.lan_connectivity_policy = config['vars']['lan_connectivity_policy']
        self.server_profile_template_name = config['vars']['server_profile_template']
        self.api_private_key = open(self.api_private_key_path).read()
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json,
                                                 # get_bin_path=get_bin_path
                                                 )
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            intersight_server_profile_template.main()

    def test_module_pass_when_required_args_passed(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args({
                'api_key_id': self.api_key_id,
                'api_private_key': self.api_private_key,
                'name': self.server_profile_template_name,
                'boot_order_policy': self.boot_order_policy,
                'lan_connectivity_policy': self.lan_connectivity_policy,
                'description': 'test template',
                'organization': self.organization
            })         
            intersight_server_profile_template.main()

   
