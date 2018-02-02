# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
<<<<<<< HEAD
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.utils.net_tools import convert_to_cidr


class ActionAddOSPFRouter(ActionBase):
    '''Ajouter une route ospf

    :param network: Adresse du Réseau
    :type  network: str
    :param network_id: Peut être un CIDR un Netmask ou un wildcard
    :type  network_id:

    Commandes exécutées::

      ActionAddOSPFRouter(network=10.11.12.0, networkID=24)

      prompt# router ospf 1
      prompt# network 10.11.12.0 0.0.0.255 area 0
      prompt#

    '''

    def define_argument(self):
        self.add_argument(name='network', required=True)
        self.add_argument(name='network_id', required=True)
=======
from switchhandler.utils.net_tools import convert_to_cidr

from switchhandler.device.executable.action.action_base import ActionBase


class ActionAddOSPFRouter(ActionBase):
    '''Ajouter une route ospf

    :param network: Adresse du Réseau
    :type  network: str
    :param network_id: Peut être un CIDR un Netmask ou un wildcard
    :type  network_id:

    Commandes exécutées::

      ActionAddOSPFRouter(network=10.11.12.0, networkID=24)

      prompt# router ospf 1
      prompt# network 10.11.12.0 0.0.0.255 area 0
      prompt#

    '''
>>>>>>> refs/remotes/origin/master

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('enable')
        self.switch.execute('conft')

        self.switch.sendline('router ospf 1')
        self.switch.expectPrompt()

        self.switch.sendline('network {}/{} area 0'.format(
            self.network,
            convert_to_cidr(self.network_id)
        ))
        self.switch.expectPrompt()

        self.switch.execute('write')
