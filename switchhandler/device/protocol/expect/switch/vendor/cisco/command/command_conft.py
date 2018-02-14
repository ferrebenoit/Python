# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="conft")
class CommandConft(CommandBase):
    '''Se placer dans le mode configure terminal

    Commandes exécutées::
    prompt# configure terminal
    prompt#
    '''

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.send_line('configure terminal')
        self.switch.expect_prompt()
