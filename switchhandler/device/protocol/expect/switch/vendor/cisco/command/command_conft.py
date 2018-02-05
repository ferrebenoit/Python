# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandConft(CommandBase):
    '''Se placer dans le mode configure terminal

    Commandes exécutées::
    prompt# configure terminal
    prompt#
    '''

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.send_line('configure terminal')
        self.switch.expect_prompt()
