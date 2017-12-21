# -*- coding: utf-8 -*-
'''

'''
from switchhandler.switch.command.command_acl_add_row import CommandACLAddRow

from switchhandler.switch.vendor.cisco.action.action_add_acl_to_interface import ActionAddACLToInterface
from switchhandler.switch.vendor.cisco.action.action_add_ospf_router import ActionAddOSPFRouter
from switchhandler.switch.vendor.cisco.action.action_auth_public_key import ActionAuthPublicKey
from switchhandler.switch.vendor.cisco.action.action_create_acl import ActionCreateACL
from switchhandler.switch.vendor.cisco.action.action_create_vlan import ActionCreateVlan
from switchhandler.switch.vendor.cisco.command.command_acl import CommandACL
from switchhandler.switch.vendor.cisco.command.command_acl_add_entry import CommandACLAddEntry
from switchhandler.switch.vendor.cisco.command.command_conft import CommandConft
from switchhandler.switch.vendor.cisco.command.command_enable import CommandEnable
from switchhandler.switch.vendor.cisco.command.command_end import CommandEnd
from switchhandler.switch.vendor.cisco.command.command_exit import CommandExit
from switchhandler.switch.vendor.cisco.command.command_int_vlan import CommandIntVlan
from switchhandler.switch.vendor.cisco.command.command_ip_address import CommandIPAddress
from switchhandler.switch.vendor.cisco.command.command_ip_helper import CommandIPHelper
from switchhandler.switch.vendor.cisco.command.command_no_acl import CommandNoACL
from switchhandler.switch.vendor.cisco.command.command_vlan import CommandVlan
from switchhandler.switch.vendor.cisco.command.command_write import CommandWrite
from switchhandler.switch.vendor.cisco.view.view_download_file_tftp import ViewDownloadFileTFTP
from switchhandler.switch.vendor.cisco.view.view_ping import ViewPing
from switchhandler.switch.vendor.cisco.view.view_port_from_mac import ViewPortFromMac
from switchhandler.switch.vendor.cisco.view.view_process_cpu import ViewProcessCPU
from switchhandler.switch.vendor.cisco.view.view_save_conf_file import ViewSaveConfFile
from switchhandler.switch.vendor.cisco.view.view_save_conf_tftp import ViewSaveConfTFTP
from switchhandler.switch.vendor.cisco.view.view_upload_file_tftp import ViewUploadFileTFTP


switchCiscoCommands = {
    "acl_add_row": CommandACLAddRow,

    "add_acl_to_interface": ActionAddACLToInterface,
    "add_ospf_router": ActionAddOSPFRouter,
    "auth_public_key": ActionAuthPublicKey,
    "create_acl": ActionCreateACL,
    "create_vlan": ActionCreateVlan,

    "acl": CommandACL,
    "acl_add_entry": CommandACLAddEntry,
    "conft": CommandConft,
    "enable": CommandEnable,
    "end": CommandEnd,
    "exit": CommandExit,
    "int_vlan": CommandIntVlan,
    "ip_address": CommandIPAddress,
    "ip_helper": CommandIPHelper,
    "no_acl": CommandNoACL,
    "vlan": CommandVlan,
    "write": CommandWrite,

    "download_file_tftp": ViewDownloadFileTFTP,
    "ping": ViewPing,
    "port_from_mac": ViewPortFromMac,
    "process_cpu": ViewProcessCPU,
    "save_conf_file": ViewSaveConfFile,
    "save_conf_tftp": ViewSaveConfTFTP,
    "upload_file_tftp": ViewUploadFileTFTP,
}
