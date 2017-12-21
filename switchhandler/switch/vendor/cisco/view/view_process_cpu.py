# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class ViewProcessCPU(CommandBase):
    '''Créer/se placer dans la configuration d'un Vlan

    :param ip: l'ip a pinger
    :type name: str

    :param repeat: Le nombre de ping
    :type repeat: int
    :default repeat: 5


    Commandes exécutées::

      ViewPing(ip='127.0.0.1', repeat=3)

      prompt# ping 127.0.0.1 repeat 3
      prompt#

    '''

    def arg_default(self):
        pass

    def do_run(self):
        self.switch.sendline('terminal length 0')
        self.switch.expectPrompt()

        self.switch.sendline('show processes cpu sorted')
        self.switch.expectPrompt()
        self.switch.log_warning(self.switch.before())
