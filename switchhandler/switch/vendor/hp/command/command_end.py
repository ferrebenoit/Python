# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class CommandEnd(CommandBase):
    '''Remonter dans le mode enable

    Commandes exécutées::
    prompt# end
    prompt#
    '''

    def do_run(self):
        self.switch.sendline('end')
        self.switch.expectPrompt()
