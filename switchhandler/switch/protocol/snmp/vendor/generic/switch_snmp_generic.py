'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.switch.protocol.snmp.switch_snmp import SwitchSnmp
from switchhandler.switch.protocol.snmp.vendor.generic import switchSnmpGenericCommands


class SwitchSnmpGeneric(SwitchSnmp):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchSnmpGeneric, self).__init__(IP, 'generic', site, dryrun)

    def getSwitchCommands(self):
        return switchSnmpGenericCommands
