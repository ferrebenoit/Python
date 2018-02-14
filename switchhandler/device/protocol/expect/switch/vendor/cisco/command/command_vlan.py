# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="vlan")
class CommandVlan(CommandBase):
    '''Créer/se placer dans la configuration d'un Vlan

    :param id: l'id
    :type id: str

    :param name: le nom du Vlan
    :type name: str


    Commandes exécutées::

      CommandVlan(id='80', name='Imprimante')

      prompt# vlan80
      prompt# name Imprimante
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='id', required=True)
        self.add_argument(name='name', default='')

    def do_run(self):
        self.switch.send_line('vlan {}'.format(self.id))
        self.switch.expect_prompt()

        if self.name != '':
            self.switch.send_line('name {}'.format(self.name))
            self.switch.expect_prompt()
