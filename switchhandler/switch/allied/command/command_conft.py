# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command_base import CommandBase


class CommandConft(CommandBase):
    '''Se placer dans le mode configure terminal

    Commandes exécutées::

      prompt# configure terminal
      prompt#
    '''

    def do_run(self):
        self.switch.sendline('configure terminal')
        self.switch.expectPrompt()
