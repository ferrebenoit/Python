# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.network.net_tools import convert_to_wildcard

from switchhandler.switch.command_base import CommandBase


class ActionAddOSPFRouter(CommandBase):
    '''Ajouter un route ospf

    :param network: Adresse du Réseau
    :type  network: str
    :param networkID: Peut être un CIDR un Netmask ou un wildcard
    :type  networkID:

    Commandes exécutées::

      ActionAddOSPFRouter(network=10.11.12.0, networkID=24)

      prompt# router ospf 1
      prompt# network 10.11.12.0 0.0.0.255 area 0
      prompt#

    '''

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.sendline('router ospf 1')
        self.switch.expectPrompt()

        self.switch.sendline('network {} {} area 0'.format(
            self.network,
            self.convert_to_wildcard(networkID)
        ))
        self.switch.expectPrompt()

        self.switch.execute('write')
