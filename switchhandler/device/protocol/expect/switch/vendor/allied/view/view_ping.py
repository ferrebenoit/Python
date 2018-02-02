# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class ViewPing(CommandBase):
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

<<<<<<< HEAD
    def define_argument(self):
        self.add_argument(name='ip', required=True)
        self.add_argument(name='repeat', default=5)

    def arg_default(self):
        # self.repeat = getattr(self, 'repeat', 5)
        pass
=======
    def arg_default(self):
        self.repeat = getattr(self, 'repeat', 5)
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.sendline('ping {} repeat {}'.format(self.ip, self.repeat))
