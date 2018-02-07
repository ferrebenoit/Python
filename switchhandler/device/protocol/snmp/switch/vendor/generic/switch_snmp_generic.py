'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.device.protocol.snmp.switch.switch_snmp import SwitchSnmp
from switchhandler.device.protocol.snmp.switch.vendor.generic import switchSnmpGenericCommands


class SwitchSnmpGeneric(SwitchSnmp):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchSnmpGeneric, self).__init__(IP, 'generic', site, dryrun)

    def getCommands(self):
        return switchSnmpGenericCommands
