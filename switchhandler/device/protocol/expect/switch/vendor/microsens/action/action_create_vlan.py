'''
Created on 9 mai 2017

@author: ferreb
'''

from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.microsens.utils import convert_vlan_id_to_vlan_filter


class ActionCreateVlan(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    :param id: l'ID du VLAN
    :type  id: int
    :param name: Le nom du vlan
    :type  name: str
    :param ip: L'ip du vlan
    :type  ip: ip **default:** None
    :param network_id: Le netmask du vlan
    :type  network_id: netmask **default:** None
    :param ip_helper: L'iphelper du réseau du vlan
    :type  ip_helper: ip **default:** None

    Commandes exécutées::

      ActionCreateVlan(id=80,
                       name=Imprimante,
                       ip=10.80.10.0,
                       network_id=24,
                       ip_Helper=10.2.2.2)

      prompt# router ospf 1
      prompt# network 10.11.12.0 0.0.0.255 area 0
      prompt#
    '''

    def arg_default(self):
        self.ip = getattr(self, 'ip', None)
        self.network_id = getattr(self, 'network_id', None)
        self.ip_helper = getattr(self, 'ip_helper', None)

    def do_run(self):
        self.switch.sendline('set vlan filter {} en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))
        self.switch.sendline('set vlan filter {} id {}'.format(
            convert_vlan_id_to_vlan_filter(self.id), self.id))
        self.switch.sendline('set vlan filter {} port 5 en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))
        self.switch.sendline('set vlan filter {} port manager en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))

        self.switch.execute('write')
