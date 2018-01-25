# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.utils.net_tools import convert_to_netmask

from switchhandler.device.executable.command.command_base import CommandBase


class CommandIPAddress(CommandBase):
    '''configurer un adresse ip

    :param ip: l'adresse ip à configurer
    :type ip: str

    :param network_id: le netmark/CIDR/wiildcard à utiliser
    :type network_id: str


    Commandes exécutées::

      CommandIPAddress(ip='10.10.10.1', network_id=24)

      prompt# ip address 10.10.10.1 255.255.255.0
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='ip', required=True)
        self.add_argument(name='network_id', required=True)

    def do_run(self):
        self.switch.sendline('ip address {} {}'.format(self.ip, convert_to_netmask(self.network_id)))
        self.switch.expectPrompt()
