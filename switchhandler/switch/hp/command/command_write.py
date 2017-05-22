# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command_base import CommandBase


class CommandWrite(CommandBase):
    '''Ecrire la configuration

    Commandes exécutées ::

      prompt# end
      prompt# write
      prompt#
    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('write memory')
        self.switch.expectPrompt()
