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
import re


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

def convert_mac_allied(mac):
    mac = mac.lower()
    
    matchgroup = re.match('([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])', mac)
    return "{}{}.{}{}.{}{}".format(matchgroup.group(1), 
                                   matchgroup.group(2), 
                                   matchgroup.group(3), 
                                   matchgroup.group(4), 
                                   matchgroup.group(5), 
                                   matchgroup.group(6))

def convert_mac_cisco(mac):
    mac = mac.lower()
    
    matchgroup = re.match('([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])', mac)
    return "{}{}.{}{}.{}{}".format(matchgroup.group(1), 
                                   matchgroup.group(2), 
                                   matchgroup.group(3), 
                                   matchgroup.group(4), 
                                   matchgroup.group(5), 
                                   matchgroup.group(6))


class NetTools:
    
    def __init__(self, value):
        self.__ip_network = ip_network('0.0.0.0/{}'.format(value))
        
    def cidr(self):
        return self.__ip_network.prefixlen
    
    def netmask(self):
        return self.__ip_network.netmask.compressed
    
    def wildcard(self):
        return self.__ip_network.hostmask.compressed
