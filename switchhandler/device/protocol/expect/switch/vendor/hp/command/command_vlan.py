# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandVlan(CommandBase):
    '''Créer/se placer dans la configuration d'un Vlan

    :param id: l'id
    :type name: str

    :param name: le nom du Vlan
    :type name: str


    Commandes exécutées::

      CommandVlan(id='80', name='Imprimante')

      prompt# interface vlan80
      prompt# name Imprimante
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL
<<<<<<< HEAD
    def define_argument(self):
        self.add_argument(name='id', required=True)
        self.add_argument(name='name', default='')

    def do_run(self):
        self.switch.sendline('vlan {}'.format(self.id))
        self.switch.expectPrompt()

        if self.name != '':
            self.switch.sendline('name "{}"'.format(self.name))
            self.switch.expectPrompt()
=======

    def do_run(self):
        self.switch.sendline('vlan {}'.format(self.id))
        self.switch.expectPrompt()

        self.switch.sendline('name "{}"'.format(self.name))
        self.switch.expectPrompt()
>>>>>>> refs/remotes/origin/master
