# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase
from switchhandler.switch.vendor.microsens.switch_microsens import convert_vlan_id_to_vlan_filter


class CommandAddTaggedVlanToPort(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
    :param vlan_id: le nom de l'ACL
    :type vlan_id: int
    :param port: le port à assigner
    :type port: str
    :param description: la desription du port
    :type description: str
    :default description: None


    Commandes exécutées::

      CommandAddTaggedVlanToPort(vlan_id=80, port=1)

      prompt# iset vlan filter 7 port 1 en
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline(
            'set vlan filter {} port {} en'.format(
                convert_vlan_id_to_vlan_filter(self.vlan_id), self.port
            )
        )
        self.switch.expectPrompt()
