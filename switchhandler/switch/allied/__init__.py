# -*- coding: utf-8 -*-
'''

.. automodule:: switchhandler.switch.allied.action.action_add_ospf_router
   :members:

.. automodule:: switchhandler.switch.allied.action.action_create_acl
   :members:

.. automodule:: switchhandler.switch.allied.action.action_create_vlan
   :members:

.. automodule:: switchhandler.switch.allied.command.command_acl
   :members:

.. automodule:: switchhandler.switch.allied.command.command_acl_add_entry
   :members:

.. automodule:: switchhandler.switch.allied.command.command_conft
   :members:

.. automodule:: switchhandler.switch.allied.command.command_enable
   :members:

.. automodule:: switchhandler.switch.allied.command.command_end
   :members:

.. automodule:: switchhandler.switch.allied.command.command_exit
   :members:

.. automodule:: switchhandler.switch.allied.command.command_ip_address
   :members:

.. automodule:: switchhandler.switch.allied.command.command_ip_helper
   :members:

.. automodule:: switchhandler.switch.allied.command.command_vlan
   :members:

.. automodule:: switchhandler.switch.allied.command.command_write
   :members:

.. automodule:: switchhandler.switch.allied.view.view_download_file_tftp
   :members:

.. automodule:: switchhandler.switch.allied.view.view_ping
   :members:

.. automodule:: switchhandler.switch.allied.view.view_port_from_mac
   :members:

.. automodule:: switchhandler.switch.allied.view.view_save_conf_tftp
   :members:

.. automodule:: switchhandler.switch.allied.view.view_upload_file_tftp
   :members:
'''


from switchhandler.switch.allied.action.action_add_ospf_router import ActionAddOSPFRouter
from switchhandler.switch.allied.action.action_create_acl import ActionCreateACL
from switchhandler.switch.allied.action.action_create_vlan import ActionCreateVlan
from switchhandler.switch.allied.command.command_acl import CommandACL
from switchhandler.switch.allied.command.command_acl_add_entry import CommandACLAddEntry
from switchhandler.switch.allied.command.command_conft import CommandConft
from switchhandler.switch.allied.command.command_enable import CommandEnable
from switchhandler.switch.allied.command.command_end import CommandEnd
from switchhandler.switch.allied.command.command_exit import CommandExit
from switchhandler.switch.allied.command.command_ip_address import CommandIPAddress
from switchhandler.switch.allied.command.command_ip_helper import CommandIPHelper
from switchhandler.switch.allied.command.command_vlan import CommandVlan
from switchhandler.switch.allied.command.command_write import CommandWrite
from switchhandler.switch.allied.view.view_download_file_tftp import ViewDownloadFileTFTP
from switchhandler.switch.allied.view.view_ping import ViewPing
from switchhandler.switch.allied.view.view_port_from_mac import ViewPortFromMac
from switchhandler.switch.allied.view.view_save_conf_tftp import ViewSaveConfTFTP
from switchhandler.switch.allied.view.view_upload_file_tftp import ViewUploadFileTFTP


switchAlliedCommands = {
    #    "add_acl_to_interface": ActionAddACLToInterface,
    "add_ospf_router": ActionAddOSPFRouter,
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
