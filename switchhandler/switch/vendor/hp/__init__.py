# -*- coding: utf-8 -*-
'''
'''

from switchhandler.switch.command.command_acl_add_row import CommandACLAddRow
from switchhandler.switch.vendor.hp.action.action_auth_public_key import ActionAuthPublicKey
from switchhandler.switch.vendor.hp.action.action_create_acl import ActionCreateACL
from switchhandler.switch.vendor.hp.action.action_create_vlan import ActionCreateVlan
from switchhandler.switch.vendor.hp.command.command_acl import CommandACL
from switchhandler.switch.vendor.hp.command.command_acl_add_entry import CommandACLAddEntry
from switchhandler.switch.vendor.hp.command.command_add_tagged_vlan_to_port import CommandAddTaggedVlanToPort
from switchhandler.switch.vendor.hp.command.command_conft import CommandConft
from switchhandler.switch.vendor.hp.command.command_enable import CommandEnable
from switchhandler.switch.vendor.hp.command.command_end import CommandEnd
from switchhandler.switch.vendor.hp.command.command_exit import CommandExit
from switchhandler.switch.vendor.hp.command.command_int_vlan import CommandIntVlan
from switchhandler.switch.vendor.hp.command.command_ip_address import CommandIPAddress
from switchhandler.switch.vendor.hp.command.command_ip_helper import CommandIPHelper
from switchhandler.switch.vendor.hp.command.command_no_acl import CommandNoACL
from switchhandler.switch.vendor.hp.command.command_vlan import CommandVlan
from switchhandler.switch.vendor.hp.command.command_write import CommandWrite
from switchhandler.switch.vendor.hp.view.view_download_file_tftp import ViewDownloadFileTFTP
from switchhandler.switch.vendor.hp.view.view_ping import ViewPing
from switchhandler.switch.vendor.hp.view.view_port_from_mac import ViewPortFromMac
from switchhandler.switch.vendor.hp.view.view_save_conf_tftp import ViewSaveConfTFTP
from switchhandler.switch.vendor.hp.view.view_upload_file_tftp import ViewUploadFileTFTP


switchHPCommands = {
    "acl_add_row": CommandACLAddRow,


    "auth_public_key": ActionAuthPublicKey,
    "create_acl": ActionCreateACL,
    "create_vlan": ActionCreateVlan,

    "acl": CommandACL,
    "acl_add_entry": CommandACLAddEntry,
    "add_tagged_vlan_to_port": CommandAddTaggedVlanToPort,
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
    "save_conf_tftp": ViewSaveConfTFTP,
    "upload_file_tftp": ViewUploadFileTFTP,
}