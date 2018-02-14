# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="ip_helper")
class CommandIPHelper(CommandBase):
    '''configurer un ip helper

    :param ip: l'adresse de l'ip helper à configurer
    :type ip: str



    Commandes exécutées::

      CommandIPHelper(ip='10.10.10.1')

      prompt# ip helper-address 10.10.10.1
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='ip', required=True)

    def do_run(self):
        self.switch.send_line('ip helper-address {}'.format(self.ip))
        self.switch.expect_prompt()
