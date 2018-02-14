'''
Created on 23 déc. 2017

@author: ferre
'''
from switchhandler.device.executable.view.view_base import ViewBase
from switchhandler.device.protocol.snmp.switch.vendor.generic import CATEGORY_SNMP_GENERIC
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_SNMP_GENERIC, registered_name='get_sysdescr')
class ViewSysdescr(ViewBase):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def arg_default(self):
        pass

    def do_run(self):
        pass
