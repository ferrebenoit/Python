# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class CommandEnd(CommandBase):
    '''Remonter dans le mode enable

    Commandes exécutées::
    prompt# end
    prompt#
    '''
<<<<<<< HEAD
    def define_argument(self):
        pass
=======
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.sendline('end')
        self.switch.expectPrompt()
