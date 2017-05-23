# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class CommandVlan(CommandBase):
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

    def do_run(self):
        self.switch.execute('vlan', self.id, self.name)
        self.switch.expectPrompt()
