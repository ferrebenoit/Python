# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.network.net_tools import convert_to_cidr

from switchhandler.switch.command.command_base import CommandBase


class CommandACLAddEntry(CommandBase):
    '''Ajoute une liegne dans l'acl courante

    :param index: L'index de la ligne d'ACL
    :type  index: int
    :param action: Permit ou Deny
    :type  action: str
    :param protocol: TCP, UDP, IP et ICMP
    :type  protocol: str
    :param src1: partie source de l'acl host ou Subnet
    :type  src1: str
    :param src2: partie source de l'acl IP ou masque
    :type  src2: str
    :param src_port_operator: operateur eq ...
    :type  src_port_operator: str
    :param src_port: Port source sur lequel s'applique la ligne d'acl
    :type  src_port: str
    :param dst1: partie destination de l'acl host ou Subnet
    :type  dst1: str
    :param dst2: partie destination de l'acl IP ou masque
    :type  dst2: str
    :param dst_port_operator: operateur eq ...
    :type  dst_port_operator: str
    :param dst_port: Port source sur lequel s'applique la ligne d'acl
    :type  dst_port: str
    :param log: mettre la valeur log dans cette variable pour que le switch
                logue les accés
    :type  log: str
    :param inverse_src_and_dst: Par défaut ajoute une entrée d'ACL en Input mettre cette valeur à True pour faire une ACL en Output
    :type  inverse_src_and_dst: bool

    :default :type  inverse_src_and_dst: False


    Commandes exécutée::

      prompt#
      prompt#

    '''

    def arg_default(self):
        self.inverse_src_and_dst = getattr(self, 'inverse_src_and_dst', False)

    def do_run(self):
        # if protocol is ICMP and not inverse_src_and_dst assign icmp-type 0 to  src_port_operator
        # if protocol is ICMP and inverse_src_and_dst assign icmp-type 8 to  dst_port_operator

        # if we ask icmp add icmp type at the end of request
        if (self.protocol.lower() == 'icmp'):
            if self.inverse_src_and_dst:
                self.src_port_operator = "8"
            else:
                self.dst_port_operator = "0"

        if (self.src1.lower() != 'host'):
            self.src2 = convert_to_cidr(self.src2)

        if (self.dst1.lower() != 'host'):
            self.dst2 = convert_to_cidr(self.dst2)

        if (self.src1.lower() == 'host'):
            self.src1 = self.src2
            self.src2 = '0'

        if (self.dst1.lower() == 'host'):
            self.dst1 = self.dst2
            self.dst2 = '0'

        if self.src2 != '':
            self.src2 = '/{}'.format(self.src2)

        if self.dst2 != '':
            self.dst2 = '/{}'.format(self.dst2)

        if self.inverse_src_and_dst:
            self.switch.sendline('{} {} {}{} {} {} {}{} {} {} {}'.format(
                self.action,
                self.protocol,
                self.dst1,
                self.dst2,
                self.dst_port_operator,
                self.dst_port,
                self.src1,
                self.src2,
                self.src_port_operator,
                self.src_port,
                self.log
            ))
        else:
            self.switch.sendline('{} {} {}{} {} {} {}{} {} {} {}'.format(
                self.action,
                self.protocol,
                self.src1,
                self.src2,
                self.src_port_operator,
                self.src_port,
                self.dst1,
                self.dst2,
                self.dst_port_operator,
                self.dst_port,
                self.log
            ))
        self.switch.expectPrompt()
