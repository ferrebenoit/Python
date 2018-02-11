# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="int")
class CommandInt(CommandBase):
    '''Créer/se placer dans la configuration d'une interface

    :param interface: le nom de l'interface
    :type interface: str

    :param description: la description de l'interface
    :type description: str


    Commandes exécutées::

      CommandInt(interface='port1.0.3', description='*** Microsens ***')

      prompt# interface port1.0.3
      prompt# description *** Microsens ***
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='interface', required=True)
        self.add_argument(name='description', default='')

    def do_run(self):
        self.switch.send_line('interface {}'.format(self.interface))
        self.switch.expect_prompt()

        if self.description != '':
            self.switch.send_line('description {}'.format(self.description))
            self.switch.expect_prompt()
