# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="add_tagged_vlan_to_port")
class CommandAddTaggedVlanToPort(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
    :param vlan_id: le nom de l'ACL
    :type vlan_id: int
    :param port: le port à assigner
    :type port: str
    :param description: la desription du port
    :type description: str
    :default description: None


    Commandes exécutées::

      CommandAddTaggedVlanToPort(vlan_id=80, port=port1.1.8, description="Imprimante")

      prompt# int port1.1.8
      prompt# description Imprimante
      prompt# 'switchport trunk allowed vlan add 80
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='vlan_id', required=True)
        self.add_argument(name='port', required=True)
        self.add_argument(name='description', required=True)

    def do_run(self):
        self.switch.send_line('int {}'.format(self.port))
        self.switch.expect_prompt()

        if self.description is not None:
            self.switch.send_line('description {}'.format(self.description))
            self.switch.expect_prompt()

        self.switch.send_line('switchport trunk allowed vlan add {}'.format(self.vlan_id))
        self.switch.expect_prompt()
