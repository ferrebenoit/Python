# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.protocol.expect.switch.switch_expect import ConfigMode

from switchhandler.device.executable.command.command_base import CommandBase


class CommandEnd(CommandBase):
    '''Remonter dans le mode enable

    Commandes exécutées::

      prompt# end
      prompt#
    '''
    def define_argument(self):
        pass

    def do_run(self):
        if not self.switch.getConfigMode() == ConfigMode.GLOBAL:
            self.switch.sendline('end')
            self.switch.expectPrompt()
