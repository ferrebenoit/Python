from switchhandler.switch.vendor.microsens.action.action_create_vlan import ActionCreateVlan

from switchhandler.switch.vendor.microsens.command.command_write import CommandWrite

switchMicrosensCommands = {
    'create_vlan': ActionCreateVlan,

    'write': CommandWrite,
}
