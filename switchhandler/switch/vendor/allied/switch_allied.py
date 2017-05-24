import re

from pexpect.exceptions import TIMEOUT, EOF

from switchhandler.network.net_tools import convert_to_cidr, convert_mac_allied
from switchhandler.switch.switch_base import SwitchBase, ConfigMode, Exec
from switchhandler.switch.vendor.allied import switchAlliedCommands


class SwitchAllied(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchAllied, self).__init__(IP, 'allied', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

    def getExecLevel(self):
        if self.exec == '>':
            return Exec.USER
        elif self.exec == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        if self.configMode == '':
            return ConfigMode.GLOBAL
        elif self.configMode == 'config':
            return ConfigMode.TERMINAL
        elif self.configMode == 'config-if':
            return ConfigMode.INTERFACE
        elif self.configMode == 'config-vlan':  # vlan database
            return ConfigMode.VLAN

    def expectPrompt(self):
        return super(SwitchAllied, self).expectPrompt()

    def login(self, login, password):
        if super(SwitchAllied, self).login(login, password):
            self.expectPrompt()
            return True
        else:
            return False

    def logout(self):
        return super(SwitchAllied, self).logout()

    def getSwitchCommands(self):
        return switchAlliedCommands
