'''
Created on 15 mai 2018

@author: ferreb
'''

from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.device.protocol.expect.switch.vendor.cisco.switch_cisco import SwitchCisco
from switchhandler.device.protocol.expect.switch.vendor.nexus import CATEGORY_NEXUS
from switchhandler.utils.decorator.class_register import registered_class_scan,\
    get_registered_classes


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect.switch.vendor.nexus')
class SwitchNexus(SwitchCisco):

    def getCommands(self):
        # merge two dict category nexus replace category cisco
        # return {**get_registered_classes(CATEGORY_CISCO),
        # **get_registered_classes(CATEGORY_NEXUS)}
        return get_registered_classes(CATEGORY_CISCO)
