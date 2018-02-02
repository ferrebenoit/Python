# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandInt(CommandBase):
    '''Créer/se placer dans la configuration d'une interface

    :param interface: le nom de l'interface
    :type interface: str

    :param description: la description de l'interface
    :type description: str


    Commandes exécutées::

      CommandInt(interface='port1.0.3', description='*** Microsens ***')

      prompt# interface port1.0.3
      prompt# description *** Microsens ***
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

<<<<<<< HEAD
    def define_argument(self):
        self.add_argument(name='interface', required=True)
        self.add_argument(name='description', default='')

    def do_run(self):
        self.switch.sendline('interface {}'.format(self.interface))
        self.switch.expectPrompt()

        if self.description != '':
            self.switch.sendline('description {}'.format(self.description))
            self.switch.expectPrompt()
=======
    def do_run(self):
        self.switch.sendline('interface {}'.format(self.interface))
        self.switch.expectPrompt()

        self.switch.sendline('description {}'.format(self.description))
        self.switch.expectPrompt()
>>>>>>> refs/remotes/origin/master
