# coding: utf-8
'''

'''

from ipaddress import ip_network
import re


def convert_to_cidr(value):
    """Cette fonction convertie un wildcard ou un netmask en CIDR Device::

        >> convert_to_cidr(255.255.255.0)
        24
        >> convert_to_cidr(0.0.0.255)
        24

    :param value: Le wildcard ou le netmask à convertir
    :type value: str
    :returns: le cidr correspondant ou "" si value n'est pas valide
    :rtype: str.

    """

    try:
        return ip_network('0.0.0.0/{}'.format(value)).prefixlen
    except Exception:
        return ''


def convert_to_netmask(value):
    try:
        return ip_network('0.0.0.0/{}'.format(value)).netmask.compressed
    except Exception:
        return ''


def convert_to_wildcard(value):
    try:
        return ip_network('0.0.0.0/{}'.format(value)).hostmask.compressed
    except:
        return ''


def convert_mac_HP(mac):
    mac = mac.lower()

    matchgroup = re.match('([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])[:-]([0-9a-f][0-9a-f])', mac)
    return "{}{}{}-{}{}{}".format(matchgroup.group(1),
                                  matchgroup.group(2),
                                  matchgroup.group(3),
                                  matchgroup.group(4),
                                  matchgroup.group(5),
                                  matchgroup.group(6))


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
