'''
Created on 19 janv. 2018

@author: ferre
'''
from switchhandler.device.protocol.expect.device_expect import DeviceExpect


class BashExpect(DeviceExpect):
    '''
    classdocs
    '''

    def __init__(self, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super(BashExpect, self).__init__('bash', IP, vendor, site, dryrun)
