# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class
from switchhandler.utils.net_tools import convert_to_wildcard


@registered_class(category=CATEGORY_CISCO, registered_name="add_ospf_router")
class ActionAddOSPFRouter(ActionBase):
    '''Ajouter un route ospf

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

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.send_line('router ospf 1')
        self.switch.expect_prompt()

        self.switch.send_line('network {} {} area 0'.format(
            self.network,
            convert_to_wildcard(self.network_id)
        ))
        self.switch.expect_prompt()

        self.switch.execute('write')
