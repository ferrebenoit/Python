# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.switch_base import ConfigMode

from switchhandler.switch.command_base import CommandBase


class CommandEnd(CommandBase):
    '''Remonter dans le mode enable

    Commandes exécutées::
    prompt# end
    prompt#
    '''

    def do_run(self):
        if not self.switch.getConfigMode() == ConfigMode.GLOBAL:
            self.switch.sendline('end')
            self.switch.expectPrompt()
