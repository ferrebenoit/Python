# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class CommandWrite(CommandBase):
    '''Ecrire la configuration

    Commandes exécutées ::

      prompt# save settings
      prompt#
    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('save settings')
        self.switch.expectPrompt()
