# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.executable.command.command_base import CommandBase


class CommandEnable(CommandBase):
    '''se placer en mode de configuration enable


    Commandes exécutées::

      CommandEnable()

      prompt# enable
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('enable')
        self.switch.expectPrompt()