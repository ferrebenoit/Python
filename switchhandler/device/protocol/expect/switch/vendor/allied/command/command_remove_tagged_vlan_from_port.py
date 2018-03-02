# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="remove_tagged_vlan_from_port")
class CommandRemoveTaggedVlanFromPort(CommandBase):
    '''enlever un vlan d'un port

    def remove_tagged_vlan_from_port(self, vlan_id, port, description=None):
    :param vlan_id: le nom du vlan
    :type vlan_id: int
    :param port: le port
    :type port: str
    :param description: la desription du port
    :type description: str
    :default description: None


    Commandes exécutées::

      CommandRemoveTaggedVlanFromPort(vlan_id=80, port=port1.1.8, description="Microsens")

      prompt# int port1.1.8
      prompt# description Microsens
      prompt# 'switchport trunk allowed vlan remove 80
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='vlan_id', required=True)
        self.add_argument(name='port', required=True)
        self.add_argument(name='description', required=False, default=None)

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('enable')
        self.switch.execute('conft')

        self.switch.send_line('int {}'.format(self.port))
        self.switch.expect_prompt()

        if self.description is not None:
            self.switch.send_line('description {}'.format(self.description))
            self.switch.expect_prompt()

        self.switch.send_line('switchport trunk allowed vlan remove {}'.format(self.vlan_id))
        self.switch.expect_prompt()
        self.switch.execute('write')
