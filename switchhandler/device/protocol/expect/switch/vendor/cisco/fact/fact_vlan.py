'''
Created on 4 févr. 2018

@author: ferre
'''
from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="fact_vlan")
class FactVlan(FactBase):
    '''
    classdocs
    switch.vlans().get(80).ips()
    switch.vlans().get(80).name
    switch.vlans().get(80).iphelper
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
