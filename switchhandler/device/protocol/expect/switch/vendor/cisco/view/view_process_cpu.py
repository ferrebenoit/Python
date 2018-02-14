# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="process_cpu")
class ViewProcessCPU(CommandBase):
    '''Voir les processus


    '''

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.send_line('terminal length 0')
        self.switch.expect_prompt()

        self.switch.send_line('show processes cpu sorted')
        self.switch.expect_prompt()
        self.switch.log_warning(self.switch.before())
