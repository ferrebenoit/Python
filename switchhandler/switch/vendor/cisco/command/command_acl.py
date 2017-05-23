# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class CommandACL(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    :param name: le nom de l'ACL
    :type name: str


    Commandes exécutées::

      prompt# ip access-list extended NAME
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('ip access-list extended {}'.format(self.name))
        self.switch.expectPrompt()
