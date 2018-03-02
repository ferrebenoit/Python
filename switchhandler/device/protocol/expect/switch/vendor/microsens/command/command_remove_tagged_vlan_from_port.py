# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.microsens import CATEGORY_MICROSENS
from switchhandler.device.protocol.expect.switch.vendor.microsens.utils import convert_vlan_id_to_vlan_filter
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_MICROSENS, registered_name='remove_tagged_vlan_from_port')
class CommandRemoveTaggedVlanFromPort(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
    :param vlan_id: le nom de l'ACL
    :type vlan_id: int
    :param port: le port à assigner
    :type port: str
    :param description: la desription du port
    :type description: str
    :default  description: None


    Commandes exécutées::

      CommandAddTaggedVlanToPort(vlan_id=80, port=1)

      prompt# set vlan filter 7 port 1 en
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='vlan_id', required=True)
        self.add_argument(name='port', required=True)
        self.add_argument(name='description', required=False)

    def do_run(self):
        self.switch.send_line(
            'set vlan filter {} port {} dis'.format(
                convert_vlan_id_to_vlan_filter(self.vlan_id), self.port
            )
        )
        self.switch.expect_prompt()

        self.switch.send_line(
            'set vlan port {} hybrid'.format(self.port)
        )
        self.switch.expect_prompt()

        self.switch.send_line(
            'set vlan port {} id {}'.format(self.port, 1)
        )
        self.switch.expect_prompt()

        self.switch.execute('write')
