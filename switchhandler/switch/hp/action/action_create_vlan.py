'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.action_base import ActionBase


class ActionCreateVlan(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    def create_vlan(self, 
    :param id: l'ID du VLAN 
    :type  id: int
    :param name: Le nom du vlan
    :type  name: str
    :param ip: L'ip du vlan
    :type  ip: ip
    :default ip:None 
    :param network_id: Le netmask du vlan
    :type  network_id: netmask
    :default network_id:None 
    :param ip_helper: L'iphelper du réseau du vlan
    :type  ip_helper: ip
    :default ip_helper:None


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
        switch.execute('end')
        switch.execute('conft')

        switch.execute('vlan', id=slelf.id, name=self.name)

        # If IP mask and CIDR are provided add an IP to the vlan
        if self.IP is not None and network is not None:
            self.switch.execute(
                'ip_address',
                ip=self.ip,
                network_id=network_id
            )

            if self.ip_helper is not None:
                self.switch.execute('ip_helper', ip=self.ip_helper)

        self.switch.execute('write')
