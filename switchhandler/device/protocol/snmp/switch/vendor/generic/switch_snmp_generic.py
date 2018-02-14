'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.device.protocol.snmp.switch.switch_snmp import SwitchSnmp
from switchhandler.device.protocol.snmp.switch.vendor.generic import CATEGORY_SNMP_GENERIC
from switchhandler.utils.decorator.class_register import registered_class_scan,\
    get_registered_classes


@registered_class_scan(BasePackage='switchhandler.device.protocol.snmp.switch.vendor.generic')
class SwitchSnmpGeneric(SwitchSnmp):

    def __init__(self, IP, site=None, dryrun=False):
        super().__init__(IP, 'generic', site, dryrun)

    def getCommands(self):
        return get_registered_classes(CATEGORY_SNMP_GENERIC)
