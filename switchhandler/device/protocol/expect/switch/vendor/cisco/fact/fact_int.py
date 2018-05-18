'''
Created on 4 fevr. 2018

@author: ferre
'''

import re

from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


class Interface(object):

    def __init__(self):
        self.name = ''
        self.portspeed = ''
        self.portnumber = ''
        self.description = ''
        self.trunkingmode = ''
        self.vlanaccess = ''
        self.vlantagged = ''
        self.speed = ''
        self.duplex = ''


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

    __REGEX_INTERFACE_RUN = r"(^(interface (?P<portspeed>GigabitEthernet|FastEthernet)(?P<portnumber>(([0-9]+)\/)?([0-9]+)\/([0-9]+)))\n((\s*switchport trunk allowed vlan (?P<vlantagged>[0-9]+(,[0-9]+)*)\n)|(\s*switchport access vlan (?P<vlanaccess>[0-9]+)\n)|(\s*duplex (?P<duplex>half|full)\n)|(\s*speed (?P<speed>[0-9]+)\n)|(?P<mode>\s*switchport mode (?P<trunkingmode>(trunk)|(access))\s*\n)|\s*description (?P<desc>.*)\s*\n|(^$\n)|(^.*(?!!).$\n))*^(!)$)"

    def parse_interfaces(self, switch_conf):
        # regex = re.compile(self.__REGEX_INTERFACE_RUN, re.MULTILINE)
        # print(self.__REGEX_INTERFACE_RUN)
        # return regex.finditer(switch_conf)
        # print(switch_conf)
        return re.finditer(self.__REGEX_INTERFACE_RUN, switch_conf, re.MULTILINE)

    def define_argument(self):
        pass

    def do_run(self):
        result = {}

        conf = self.switch.get_fact('config')

        if conf is None:
            return None

        interfaces = self.parse_interfaces(conf['sanitized'])

        for interface in interfaces:
            port_name = interface.groupdict(
            )["portspeed"] + interface.groupdict()["portnumber"]

            res_int = Interface()

            res_int.name = port_name
            res_int.portspeed = interface.groupdict().get("portspeed", '')
            res_int.portnumber = interface.groupdict().get("portnumber", '')
            res_int.description = interface.groupdict().get("desc", '')
            res_int.trunkingmode = interface.groupdict().get("trunkingmode", '')
            res_int.vlanaccess = interface.groupdict().get("vlanaccess", '')
            res_int.vlantagged = interface.groupdict().get("vlantagged", '')
            res_int.speed = interface.groupdict().get("speed", '')
            res_int.duplex = interface.groupdict().get("duplex", '')

            result[port_name] = res_int

        return result
