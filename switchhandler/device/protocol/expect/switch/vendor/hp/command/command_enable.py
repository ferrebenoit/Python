# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="enable")
class CommandEnable(CommandBase):
    '''se placer en mode de configuration enable


    Commandes exécutées::

      CommandEnable()

      prompt# enable
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.send_line('enable')
        self.switch.expect_prompt()
