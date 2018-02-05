# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import re

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.utils.net_tools import convert_mac_cisco


class ViewPortFromMac(CommandBase):
    '''visualiser le port à l'quel une mac est associé

    :param mac: la mac à trouver
    :type mac: str

    :param ip: L'ip à pringuer pour l'apprentissage de la mac
    :type ip: str
    :default ip: None


    Commandes exécutées::

      ViewPortFromMac(mac='aa:bb:cc:dd:ee:ff', ip='127.0.0.1')

      prompt# ping 127.0.0.1
      prompt# show mac address-table | include aa:bb:cc:dd:ee:ff
      prompt#

    '''

    def define_argument(self):
        self.add_argument(name='mac', required=True)
        self.add_argument(name='ip', default=None)

    def arg_default(self):
        # self.ip = getattr(self, 'ip', None)
        pass

    def do_run(self):
        self.switch.execute('end')

        self.mac = convert_mac_cisco(self.mac)

        if self.ip is not None:
            self.switch.execute('ping', ip=self.ip, repeat=3)
            self.switch.expect_prompt()

        self.switch.send_line("show mac address-table | include {}".format(self.mac))
        self.switch.expect_prompt()

        match = re.search(
            '^[ ]*([0-9][0-9]*)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^ ^\n]*)$', self.switch.before(), re.MULTILINE)

        if match:
            return match.group(4)
        else:
            return ""
