# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="add_tagged_vlan_to_port")
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

      CommandAddTaggedVlanToPort(vlan_id=80, port=B1, description="Imprimante")

      prompt# vlan 80
      prompt# tagged B1
      prompt# interface B1
      prompt# Name Imprimante
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

        self.switch.send_line('vlan {}'.format(self.vlan_id))
        self.switch.expect_prompt()

        self.switch.send_line('tagged {}'.format(self.port))
        self.switch.expect_prompt()

        if self.description is not None:
            self.switch.send_line('interface {}'.format(self.port))
            self.switch.expect_prompt()
            self.switch.send_line('name {}'.format(self.description))
            self.switch.expect_prompt()

        self.switch.execute('write')
