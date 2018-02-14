# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="end")
class CommandEnd(CommandBase):
    '''Remonter dans le mode enable

    Commandes exécutées::

      prompt# end
      prompt#
    '''

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.send_line('end')
        self.switch.expect_prompt()
