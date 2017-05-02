# coding: utf-8
'''
Created on 12 avr. 2017

@author: ferreb
'''
import re


class DocGenerator:
    __REGEX_INTERFACE = "((interface (?P<portspeed>GigabitEthernet|FastEthernet)(?P<portnumber>(([0-9]+)\/)?([0-9]+)\/([0-9]+)))\n((\s*switchport trunk allowed vlan (?P<vlantagged>[0-9]+(,[0-9]+)*)\n)|(\s*switchport access vlan (?P<vlanaccess>[0-9]+)\n)|(?P<mode>\s*switchport mode (?P<trunkingmode>(trunk)|(access))\s*\n)|\s*description (?P<desc>.*)\s*\n|(^$\n)|(^.*(?!!).$\n))*^(!)$)"
    __REGEX_INFO = "^hostname +(?P<hostname>.*)"

    # "((interface (?P<portspeed>GigabitEthernet|FastEthernet)(?P<portnumber>(([0-9]+)\/)?([0-9]+)\/([0-9]+)))\n\
    #                    (\
    #                        (\s*switchport trunk allowed vlan (?P<vlantagged>[0-9]+(,[0-9]+)*)\n)|\
    #                        (\s*switchport access vlan (?P<vlanaccess>[0-9]+)\n)|\
    #                        (?P<mode>\s*switchport mode (?P<trunkingmode>(trunk)|(access))\s*\n)|\
    #                        \s*description (?P<desc>.*)\s*\n|\
    #                        (^$\n)|\
    #                        (^.*(?!!).$\n)\
    #                    )*\
    #                    ^(!)$)"

    __template_interface = "   * - {portspeed}{portnumber}\n     - {desc}\n     - {trunkingmode}\n     - {vlanaccess}"

    def __init__(self):
        pass

    def gen_switch(self, interfaces, infos, template):
        return template.format(**interfaces, **infos)

    def gen_switch_interfaces(self, template, interfaces):
        result = ''
        for interface in interfaces:
            result = "{}\n{}".format(
                result,
                self.gen_switch_interface(interface.groupdict(), template))

        return result

    def parse_interfaces(self, switch_conf):
        regex = re.compile(self.__REGEX_INTERFACE, re.MULTILINE)
        return regex.finditer(switch_conf)

    def parse_info(self, switch_conf):
        regex = re.compile(self.__REGEX_INTERFACE, re.MULTILINE)
        return regex.search(switch_conf).groupdict()

    def gen_switch_page(self, switch_conf, template_str):
        interfaces = self.parse_interfaces(switch_conf)
        generated_interfaces = (
            self.gen_switch_interfaces(
                self.__template_interface,
                interfaces)
        )

        infos = self.parse_info(switch_conf)

        return template_str.format(infos, interfaces=generated_interfaces)
