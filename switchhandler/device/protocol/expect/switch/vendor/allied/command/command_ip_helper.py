# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandIPHelper(CommandBase):
    '''configurer un ip helper

<<<<<<< HEAD
    :param ip: l'adresse de l'ip helper à configurer
    :type ip: str



    Commandes exécutées::

      CommandIPHelper(ip='10.10.10.1')

      prompt# ip helper-address 10.10.10.1
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='ip', required=True)
=======
    :param iP: l'adresse de l'ip helper à configurer
    :type name: str



    Commandes exécutées::

      CommandIPHelper(ip='10.10.10.1')

      prompt# ip helper-address 10.10.10.1
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.sendline('ip dhcp-relay server-address {}'.format(self.ip))
        self.switch.expectPrompt()
        self.switch.sendline('ip helper-address {}'.format(self.ip))
        self.switch.expectPrompt()
