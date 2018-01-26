'''
Created on 19 janv. 2018

@author: ferre
'''
from switchhandler.device.device import Device


class DeviceSnmp(Device):
    '''
    classdocs
    '''

    def __init__(self, device, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super(DeviceSnmp, self).__init__(
            device, 'snmp', IP, vendor, site, dryrun)
