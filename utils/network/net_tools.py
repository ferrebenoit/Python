'''
Created on 16 mars 2017

@author: ferreb
'''
#from netaddr import ip
#import ipaddress
#from ipaddress import ip_address, ip_network
#from ipaddress import IPv4Address
#IPv4Address("255.255.255.0").
#
#print(ip_address("255.255.255.0"))
#print(ip_address("255.255.255.0").)
#
#ip_network('0.0.0.0/255.255.255.0').hostmask.compressed
#ip_network('0.0.0.0/255.255.255.0').prefixlen
#ip_network('0.0.0.0/24').netmask.compressed
#
#ip_network._make_netmask('255.255.255.0')
from ipaddress import ip_network


def convert_to_cidr(value):
    try:
        return ip_network('0.0.0.0/{}'.format(value)).prefixlen
    except:
        return ''
    
def convert_to_netmask(value):
    try:
        return ip_network('0.0.0.0/{}'.format(value)).netmask.compressed
    except:
        return ''
    
def convert_to_wildcard(value):
    try:
        return ip_network('0.0.0.0/{}'.format(value)).hostmask.compressed
    except:
        return ''

class NetTools:
    
    def __init__(self, value):
        self.__ip_network = ip_network('0.0.0.0/{}'.format(value))
        
    def cidr(self):
        return self.__ip_network.prefixlen
    
    def netmask(self):
        return self.__ip_network.netmask.compressed
    
    def wildcard(self):
        return self.__ip_network.hostmask.compressed
