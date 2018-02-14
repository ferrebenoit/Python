# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="ping")
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

    def define_argument(self):
        self.add_argument(name='ip', required=True)
        self.add_argument(name='repeat', default=5)

    def do_run(self):
        self.switch.send_line('ping {} repeat {}'.format(self.ip, self.repeat))
