'''
Created on 9 mai 2017

@author: ferreb
'''

from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.microsens import CATEGORY_MICROSENS
from switchhandler.device.protocol.expect.switch.vendor.microsens.utils import convert_vlan_id_to_vlan_filter
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_MICROSENS, registered_name='create_vlan')
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

    def define_argument(self):
        self.add_argument(name='name', required=True)
        self.add_argument(name='ip', default=None)
        self.add_argument(name='network_id', default=None)
        self.add_argument(name='ip_helper', default=None)

    def do_run(self):
        self.switch.send_line('set vlan filter {} en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))
        self.switch.send_line('set vlan filter {} id {}'.format(
            convert_vlan_id_to_vlan_filter(self.id), self.id))
        self.switch.send_line('set vlan filter {} port 5 en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))
        self.switch.send_line('set vlan filter {} port manager en'.format(
            convert_vlan_id_to_vlan_filter(self.id)))

        self.switch.send_line('set system group {}'.format(
            self.name.upper()))

        self.switch.execute('write')
