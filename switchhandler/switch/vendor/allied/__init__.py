# -*- coding: utf-8 -*-
'''
'''


from switchhandler.switch.command.command_acl_add_row import CommandACLAddRow

from switchhandler.switch.vendor.allied.action.action_add_ospf_router import ActionAddOSPFRouter
from switchhandler.switch.vendor.allied.action.action_auth_public_key import ActionAuthPublicKey
from switchhandler.switch.vendor.allied.action.action_create_acl import ActionCreateACL
from switchhandler.switch.vendor.allied.action.action_create_vlan import ActionCreateVlan
from switchhandler.switch.vendor.allied.command.command_acl import CommandACL
from switchhandler.switch.vendor.allied.command.command_acl_add_entry import CommandACLAddEntry
from switchhandler.switch.vendor.allied.command.command_conft import CommandConft
from switchhandler.switch.vendor.allied.command.command_enable import CommandEnable
from switchhandler.switch.vendor.allied.command.command_end import CommandEnd
from switchhandler.switch.vendor.allied.command.command_exit import CommandExit
from switchhandler.switch.vendor.allied.command.command_ip_address import CommandIPAddress
from switchhandler.switch.vendor.allied.command.command_ip_helper import CommandIPHelper
from switchhandler.switch.vendor.allied.command.command_vlan import CommandVlan
from switchhandler.switch.vendor.allied.command.command_write import CommandWrite
from switchhandler.switch.vendor.allied.view.view_download_file_tftp import ViewDownloadFileTFTP
from switchhandler.switch.vendor.allied.view.view_ping import ViewPing
from switchhandler.switch.vendor.allied.view.view_port_from_mac import ViewPortFromMac
from switchhandler.switch.vendor.allied.view.view_save_conf_tftp import ViewSaveConfTFTP
from switchhandler.switch.vendor.allied.view.view_upload_file_tftp import ViewUploadFileTFTP


switchAlliedCommands = {
    "command_acl_add_row": CommandACLAddRow,


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
    "ip_address": CommandIPAddress,
    "ip_helper": CommandIPHelper,
    "vlan": CommandVlan,
    "write": CommandWrite,

    "download_file_tftp": ViewDownloadFileTFTP,
    "ping": ViewPing,
    "port_from_mac": ViewPortFromMac,
    "save_conf_tftp": ViewSaveConfTFTP,
    "upload_file_tftp": ViewUploadFileTFTP,
}
