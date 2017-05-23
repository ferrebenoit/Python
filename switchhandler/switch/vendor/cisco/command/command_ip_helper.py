# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''

from switchhandler.switch.command.command_base import CommandBase


class CommandIPHelper(CommandBase):
    '''configurer un ip helper

    :param iP: l'adresse de l'ip helper à configurer
    :type name: str



    Commandes exécutées::

      CommandIPHelper(ip='10.10.10.1')

      prompt# ip helper-address 10.10.10.1
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('ip helper-address {}'.format(self.ip))
        self.switch.expectPrompt()
