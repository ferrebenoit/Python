# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command_base import CommandBase


class ActionAddACLToInterface(CommandBase):
    '''Assigner une ACL à une Interface

    :param acl_name: Nom de l'acl
    :type  acl_name: str
    :param interface_name: Nom de l'interface
    :type  interface_name:
    :param inbound: Ajouter l'acl en pour porteger L'inbound mettre à False pour l'outbound
    :type  inbound: bool
    :default  inbound: True

    Commandes exécutées pour inbound = True::

      prompt# interface interface_name
      prompt# ip access-goupe acl_name in
      prompt#

    Commandes exécutées pour inbound = False::

      prompt# interface interface_name
      prompt# ip access-goupe acl_name out
      prompt#


    '''

    def arg_default(self):
        self.inbound = getattr(self, 'inbound', True)

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.sendline('interface {}'.format(self.interface_name))
        self.switch.expectPrompt()

        if self.inbound:
            self.switch.sendline('ip access-group {} in'.format(self.acl_name))
        else:
            self.switch.sendline('ip access-group {} out'.format(self.acl_name))
        self.switch.expectPrompt()

        self.switch.execute('write')
