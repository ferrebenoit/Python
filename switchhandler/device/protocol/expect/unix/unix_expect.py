'''
Created on 19 janv. 2018

@author: ferre
'''
from switchhandler.device.protocol.expect.device_expect import DeviceExpect
from switchhandler.device.device_exception import CommandSyntaxErrorException


class UnixExpect(DeviceExpect):
    '''
    classdocs
    '''

    def __init__(self, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super().__init__('unix', IP, vendor, site, dryrun)

    def execute(self, command_name, *args, **kwargs):
        try:
            return super().execute(command_name, *args, **kwargs)
        except CommandSyntaxErrorException:
            self.log_critical("Script will terminate changes are not written")
            self.log_debug(self.before())
            self.log_debug(self.after())
            quit()
