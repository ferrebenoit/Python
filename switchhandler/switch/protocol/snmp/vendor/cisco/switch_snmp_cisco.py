'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.switch.protocol.snmp.switch_snmp import SwitchSnmp
from switchhandler.switch.protocol.snmp.vendor.cisco import switchSnmpCiscoCommands


class SwitchSnmpCisco(SwitchSnmp):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchSnmpCisco, self).__init__(IP, 'cisco', site, dryrun)

    def getSwitchCommands(self):
        return switchSnmpCiscoCommands
