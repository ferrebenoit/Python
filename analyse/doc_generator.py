# coding: utf-8
'''
Created on 12 avr. 2017

@author: ferreb
'''
from pathlib import Path
import re

from jinja2 import Template


# class DocGenerator:
__REGEX_INTERFACE = "((interface (?P<portspeed>GigabitEthernet|FastEthernet)(?P<portnumber>(([0-9]+)\/)?([0-9]+)\/([0-9]+)))\n((\s*switchport trunk allowed vlan (?P<vlantagged>[0-9]+(,[0-9]+)*)\n)|(\s*switchport access vlan (?P<vlanaccess>[0-9]+)\n)|(\s*duplex (?P<duplex>half|full)\n)|(\s*speed (?P<speed>[0-9]+)\n)|(?P<mode>\s*switchport mode (?P<trunkingmode>(trunk)|(access))\s*\n)|\s*description (?P<desc>.*)\s*\n|(^$\n)|(^.*(?!!).$\n))*^(!)$)"
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


def parse_interfaces(switch_conf):
    regex = re.compile(__REGEX_INTERFACE, re.MULTILINE)
    return regex.finditer(switch_conf)


def parse_info(switch_conf):
    regex = re.compile(__REGEX_INFO, re.MULTILINE)
    return regex.search(switch_conf).groupdict()


def gen_switch_page(self, switch_conf, template_str, switch_ip):
    interfaces = self.parse_interfaces(switch_conf)
    infos = self.parse_info(switch_conf)

    template = Template(template_str)

    return template.render(host_name=infos['hostname'], switch_ip=switch_ip, interfaces=interfaces)


# with open("C:/Users/ferreb/git/SwitchHandler/resources/switchports.jinja", "r") as tpl:
#    doc_generator = DocGenerator()
#    tpl_str = tpl.read()

#    with open("C:/Users/ferreb/git/SwitchHandler/resources/cisco_conf.cnfg", "r") as cisco_conf:
#        cisco_conf_str = cisco_conf.read()
#        print(doc_generator.gen_switch_page(cisco_conf_str, tpl_str, "192.168.80.1"))


template_path = Path("C:/Users/ferreb/git/SwitchHandler/resources/switchports.jinja")
template_str = template_path.read_text()

template_index_path = Path("C:/Users/ferreb/git/SwitchHandler/resources/index.jinja")
template_index_str = template_index_path.read_text()

index_list = []

sites_path = Path("C:/Users/ferreb/Desktop/backup plan ip/csv/switch")
for site_path in sites_path.iterdir():
    if site_path.is_dir() and not site_path.name == '.git':
        index_list.append(site_path.name)
        switchs = []
        for switch_path in site_path.iterdir():
            if (switch_path.name.split('_')[-1] == 'cisco'):
                # print(switch_path)
                # print(switch_path.read_text())
                switch_conf = switch_path.read_text()

                interfaces = parse_interfaces(switch_conf)
                infos = parse_info(switch_conf)
                ip = switch_path.name.split("_")[0]

                switchs.append({'hostname': infos['hostname'],
                                'ip': ip,
                                'interfaces': interfaces
                                })
        print(switchs)

        template = Template(template_str)
        # print(template_str)
        # dest_path.mkdir(exist_ok=True)
        rendered = template.render(site_name=site_path.name, switchs=switchs)

        dest_path = Path('C:/Users/ferreb/Documents/documentation_switch/source/{}.rst'.format(site_path.name))
        dest_path.write_text(rendered)


template = Template(template_index_str)
rendered = template.render(sites=index_list)

dest_path = Path('C:/Users/ferreb/Documents/documentation_switch/source/index.rst')
dest_path.write_text(rendered)
