import re

from pexpect.exceptions import TIMEOUT, EOF

from switchhandler.network.net_tools import convert_to_netmask, convert_to_wildcard,\
    convert_mac_HP
from switchhandler.switch.switch_base import SwitchBase, ConfigMode, Exec
from switchhandler.switch.vendor.hp import switchHPCommands


class SwitchHP(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchHP, self).__init__(IP, 'hp', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

    @property
    def hostname(self):
        ''' strip the initial '1H' from the host name
        '''
        hostname = super(SwitchHP, self).hostname
        if not super(SwitchHP, self).hostname == 'None':
            hostname = hostname[2:]

        return hostname

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

    def expectPrompt(self):
        return super(SwitchHP, self).expectPrompt()

    def login(self, login, password):
        try:
            if self.dryrun:
                self.logger.info("Login ok as user {}".format(login))
                return True

            self.connect()
            self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

            self.connection.expect('password:')
            self.connection.sendline(password)

            self.sendline()
            self._loadPromptState()

            self.expectPrompt()

            self.logger.info("Login ok as user {}".format(login))
            return True
        except:
            self.logger.critical(self.connection.before)
            self.logger.critical(self.connection.after)
            self.logger.error("Connection error")
            return False

        return False

    def logout(self):
        if super(SwitchHP, self).logout():
            self.expect('[y/n]?')
            self.send('y')
            return True
        else:
            return False

    def getSwitchCommands(self):
        return switchHPCommands
