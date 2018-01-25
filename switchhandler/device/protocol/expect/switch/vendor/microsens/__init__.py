from switchhandler.device.protocol.expect.switch.vendor.microsens.action.action_create_vlan import ActionCreateVlan
from switchhandler.device.protocol.expect.switch.vendor.microsens.command.command_write import CommandWrite
from switchhandler.device.protocol.expect.switch.vendor.microsens.view.view_save_conf_file import ViewSaveConfFile

switchMicrosensCommands = {
    'create_vlan': ActionCreateVlan,

    'write': CommandWrite,

    'save_conf_file': ViewSaveConfFile,
}
