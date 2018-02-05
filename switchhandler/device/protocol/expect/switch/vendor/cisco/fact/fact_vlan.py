'''
Created on 4 févr. 2018

@author: ferre
'''
from switchhandler.device.executable.fact.fact_base import FactBase


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
