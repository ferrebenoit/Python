'''
Created on 23 déc. 2017

@author: ferre
'''

from switchhandler.device.protocol.snmp.device_snmp import DeviceSnmp
# from pysnmp.hlapi import ObjectIdentity, SnmpEngine


class SwitchSnmp(DeviceSnmp):
    '''
    classdocs
    '''

    def __init__(self, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super(SwitchSnmp, self).__init__('switch', IP, vendor, site, dryrun)

    def connect(self):
        pass

    def login(self, login, password):
        pass

    def logout(self):
        pass

    def getCommands(self):
        pass
