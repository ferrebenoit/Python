# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''

from switchhandler.device.executable.command.command_acl_add_row import CommandACLAddRow
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="acl_add_row")
class CommandACLAddRow(CommandACLAddRow):
    pass
