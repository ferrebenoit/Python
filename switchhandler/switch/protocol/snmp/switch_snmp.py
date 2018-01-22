'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.switch.switch_base import SwitchBase
# from pysnmp.hlapi import ObjectIdentity, SnmpEngine


class SwitchSnmp(SwitchBase):
    '''
    classdocs
    '''

    def __init__(self, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super(SwitchSnmp, self).__init__('snmp', IP, vendor, site, dryrun)

    def connect(self):
        pass

    def login(self, login, password):
        pass

    def logout(self):
        pass

    def getSwitchCommands(self):
        pass
