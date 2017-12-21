# coding: utf-8
'''
Created on 12 juin 2017

@author: ferreb
'''
import re

# from jinja2 import Template

vlan_table = {
    '1': '1',
    '30': '2',
    '252': '3',
    '262': '4',
    '160': '5',
    '29': '6',
    '80': '7',
    '15': '8',
    '10': '9',
    '70': '10',
    '100': '11',
}
__REGEX_VLAN = 'VLAN filtering is globally (?P<status>enabled)|Port default VLAN ID is (?P<forcevid>not forced)|VLAN ID   (?P<voicevlan>\d*) is used for voice|(?P<vlanport>\s*(?P<port>[\dM])\s*(Port \d|Manager)\s*(?P<mode>hybrid|trunk|access)\s*(?P<defaultvid>\d*))|(?P<vlanfilter>^\s*(?P<vlanidx>[\d]*)\s*(?P<vlanenable>on|off)\s*VLAN filter\s\d*\s*(?P<vid>\d+)\s*off\s*0\s*(?P<portmembers>([-\dM]\s*)*)$)'


def convert_vlan_id_to_vlan_filter(vlan_id):

    return vlan_table.get(vlan_id, 0)


def parse_vlan(switch_conf):
    regex = re.compile(__REGEX_VLAN, re.MULTILINE)
    vlans = regex.finditer(switch_conf)

    result = []

    for vlan in vlans:
        if vlan.groupdict()['status'] is not None:
            if vlan.groupdict()['status'] == 'enabled':
                result.append('set vlan en')
        elif vlan.groupdict()['voicevlan'] is not None:
            result.append('set vlan voicevid {}'.format(vlan.groupdict()['voicevlan']))
        elif vlan.groupdict()['vlanport'] is not None:
            result.append('set vlan port {} {}'.format(vlan.groupdict()['port'], vlan.groupdict()['mode']))
            result.append('set vlan port {} id {}'.format(vlan.groupdict()['port'], vlan.groupdict()['defaultvid']))
        elif vlan.groupdict()['vlanfilter'] is not None:
            if vlan.groupdict()['vlanenable'] == 'on':
                result.append('set vlan filter {} en'.format(vlan.groupdict()['vlanidx']))
            if not vlan.groupdict()['vid'] == '0':
                result.append('set vlan filter {} id {}'.format(vlan.groupdict()['vlanidx'], vlan.groupdict()['vid']))

            for port in re.compile('(?P<port>[-\dM])', re.MULTILINE).finditer(vlan.groupdict()['portmembers']):
                if not port.groupdict()['port'] == '-':
                    result.append('set vlan filter {} port {} en'.format(vlan.groupdict()['vlanidx'], port.groupdict()['port']))

    return "\n".join(result)
