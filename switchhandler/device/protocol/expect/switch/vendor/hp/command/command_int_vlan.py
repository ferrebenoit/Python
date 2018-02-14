# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="int_vlan")
class CommandIntVlan(CommandBase):
    '''Créer/se placer dans la configuration d'une interface Vlan

    :param id: l'id
    :type name: str

    :param name: le nom du Vlan
    :type name: str


    Commandes exécutées::

      CommandVlan(id='80', name='Imprimante')

      prompt# interface vlan80
      prompt# description Imprimante
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='id', required=True)
        self.add_argument(name='name', default='')

    def do_run(self):
        self.switch.execute('vlan', id=self.id, name=self.name)
        self.switch.expect_prompt()

        return True
