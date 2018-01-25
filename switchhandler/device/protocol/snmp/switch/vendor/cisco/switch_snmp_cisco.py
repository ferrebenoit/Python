'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.device.protocol.snmp.switch.switch_snmp import SwitchSnmp
from switchhandler.device.protocol.snmp.switch.vendor.cisco import switchSnmpCiscoCommands


class SwitchSnmpCisco(SwitchSnmp):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchSnmpCisco, self).__init__(IP, 'cisco', site, dryrun)

    def getCommands(self):
        return switchSnmpCiscoCommands
