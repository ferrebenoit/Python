'''
Created on 4 févr. 2018

@author: ferre
'''
from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="fact_int")
class FactInt(FactBase):
    '''
    vlan
    speed
    errors counters
    counters
    status (connected, notconnect, error disabled)
    switch.ints().get('fa0/1').vlans()
    switch.ints().get('fa0/1').speed
    switch.ints().get('fa0/1').status

    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def define_argument(self):
        pass

    def do_run(self):
        pass
