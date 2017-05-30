# coding: utf-8
'''
Created on 23 nov. 2016

@author: FERREB
'''

from switchhandler.switch.switch_base import SwitchBase, ConfigMode, Exec
from switchhandler.switch.vendor.cisco import switchCiscoCommands


class SwitchCisco(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchCisco, self).__init__(IP, 'cisco', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([$#])'

    def getExecLevel(self):
        if self.exec == '$':
            return Exec.USER
        elif self.exec == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        if self.configMode is None:
            return ConfigMode.GLOBAL
        elif self.configMode == 'config':
            return ConfigMode.TERMINAL
        elif self.configMode == 'config-if':
            return ConfigMode.INTERFACE
        elif self.configMode == 'config-vlan':
            return ConfigMode.VLAN
        elif self.configMode == 'conf-ssh-pubkey':
            return ConfigMode.PUBKEY
        elif self.configMode == 'conf-ssh-pubkey-user':
            return ConfigMode.PUBKEY_USER

    def expectPrompt(self):
        return super(SwitchCisco, self).expectPrompt()

    def login(self, login, password):
        if super(SwitchCisco, self).login(login, password):
            return True
        else:
            return False

    def logout(self):
        return super(SwitchCisco, self).logout()

    def getSwitchCommands(self):
        return switchCiscoCommands
