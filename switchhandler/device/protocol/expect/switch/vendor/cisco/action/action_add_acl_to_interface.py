# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="add_acl_to_interface")
class ActionAddACLToInterface(ActionBase):
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

    def define_argument(self):
        self.add_argument(name='acl_name', required=True)
        self.add_argument(name='interface_name', required=True)
        self.add_argument(name='inbound', default=True)

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.send_line('interface {}'.format(self.interface_name))
        self.switch.expect_prompt()

        if self.inbound:
            self.switch.send_line('ip access-group {} in'.format(self.acl_name))
        else:
            self.switch.sendl_ine('ip access-group {} out'.format(self.acl_name))
        self.switch.expect_prompt()

        self.switch.execute('write')
