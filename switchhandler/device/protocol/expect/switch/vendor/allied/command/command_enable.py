# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandEnable(CommandBase):
    '''se placer en mode de configuration enable


    Commandes exécutées::

      CommandEnable()

      prompt# enable
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL
<<<<<<< HEAD
    def define_argument(self):
        pass
=======
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.sendline('enable')
        self.switch.expectPrompt()
