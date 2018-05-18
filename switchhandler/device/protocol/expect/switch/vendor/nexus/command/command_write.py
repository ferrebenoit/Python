# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.nexus import CATEGORY_NEXUS
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_NEXUS, registered_name="write")
class CommandWrite(CommandBase):
    '''Ecrire la configuration

    Commandes exécutées ::

      prompt# end
      prompt# write
      prompt#
    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        pass

    def do_run(self):
        self.switch.execute('end')
        self.switch.send_line('copy running-config startup-config')
        self.switch.expect_prompt()
        return True
