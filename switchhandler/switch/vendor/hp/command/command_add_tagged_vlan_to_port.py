# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


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

      CommandAddTaggedVlanToPort(vlan_id=80, port=B1, description="Imprimante")

      prompt# vlan 80
      prompt# tagged B1
      prompt# interface B1
      prompt# Name Imprimante
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        self.switch.sendline('vlan {}'.format(self.vlan_id))
        self.switch.expectPrompt()

        self.switch.sendline('tagged {}'.format(self.port))
        self.switch.expectPrompt()

        if self.description is not None:
            self.switch.sendline('interface {}'.format(self.port))
            self.switch.expectPrompt()
            self.switch.sendline('name {}'.format(self.description))
            self.switch.expectPrompt()
