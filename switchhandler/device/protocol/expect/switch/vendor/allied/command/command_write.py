# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandWrite(CommandBase):
    '''Ecrire la configuration

    Commandes exécutées ::

      prompt# end
      prompt# write
      prompt#
    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL
    def define_argument(self):
        pass

    def do_run(self):
        self.switch.execute('end')
        self.switch.send_line('write')
        self.switch.expect_prompt()
