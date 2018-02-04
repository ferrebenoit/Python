'''
Created on 4 févr. 2018

@author: ferre
'''
from switchhandler.device.executable.fact.fact_base import FactBase


class FactInt(FactBase):
    '''
    vlan
    speed
    errors counters
    counters
    status (connected, notconnect, error disabled)
    switch.ints().get('fa0/1').vlans()
                              .speed
                              .status

    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def define_argument(self):
        pass

    def do_run(self):
        pass
