'''
Created on 19 janv. 2018

@author: ferre
'''
from switchhandler.device.protocol.expect.unix.unix_expect import UnixExpect
from switchhandler.utils.decorator.class_register import get_registered_classes,\
    registered_class_scan, registered_class
from switchhandler.device.protocol.expect.unix.vendor.bash import CATEGORY_BASH
from switchhandler.device import CATEGORY_DEVICE_EXPECT


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect.unix.vendor.bash')
@registered_class(category=CATEGORY_DEVICE_EXPECT, registered_name='bash')
class BashExpect(UnixExpect):
    '''
    classdocs
    '''

    def __init__(self, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super().__init__('bash', IP, vendor, site, dryrun)

    def getCommands(self):
        return get_registered_classes(CATEGORY_BASH)
