# coding: utf-8
'''
Created on 12 juin 2017

@author: ferreb
'''

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


def convert_vlan_id_to_vlan_filter(vlan_id):

    return vlan_table.get(vlan_id, 0)


def test():
    print(test)
