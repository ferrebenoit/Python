# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandIntVlan(CommandBase):
    '''Créer/se placer dans la configuration d'une interface Vlan

    :param id: l'id
    :type id: str

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
        self.switch.send_line('interface vlan{}'.format(self.id))
        self.switch.expect_prompt()

        if self.name != '':
            self.switch.send_line('description {}'.format(self.name))
            self.switch.expect_prompt()

        return True
