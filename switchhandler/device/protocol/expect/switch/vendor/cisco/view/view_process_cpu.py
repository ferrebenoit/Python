# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class ViewProcessCPU(CommandBase):
    '''Voir les processus


    '''

    def do_run(self):
        self.switch.send_line('terminal length 0')
        self.switch.expect_prompt()

        self.switch.send_line('show processes cpu sorted')
        self.switch.expect_prompt()
        self.switch.log_warning(self.switch.before())
