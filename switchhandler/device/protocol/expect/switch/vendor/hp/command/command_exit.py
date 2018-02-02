# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandExit(CommandBase):
    '''remonter d'un niveau


    Commandes exécutées::

      CommandExit()

      prompt# exit
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL
<<<<<<< HEAD
    def define_argument(self):
        pass
=======
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.sendline('exit')
        self.switch.expectPrompt()
