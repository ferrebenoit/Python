'''
Created on 23 déc. 2017

@author: ferre
'''
from switchhandler.device.executable.view.view_base import ViewBase
from switchhandler.device.protocol.snmp.switch.vendor.cisco import CATEGORY_SNMP_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_SNMP_CISCO, registered_name='get_sysdescr')
class ViewSysdescr(ViewBase):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def define_argument(self):
        pass

    def do_run(self):
        pass
