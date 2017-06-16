'''
Created on 8 juin 2017

@author: ferreb
'''

from switchhandler.switch.switch_base import ConfigMode
from switchhandler.switch.switch_base import Exec
from switchhandler.switch.switch_base import SwitchBase

from switchhandler.switch.vendor.microsens import switchMicrosensCommands


class SwitchMicrosens(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchMicrosens, self).__init__(IP, 'microsens', site, dryrun)

        self._PROMPT = 'Console(?P<exec>[>#])'

    def getExecLevel(self):
        if self.exec_mode == '>':
            return Exec.USER
        elif self.exec_mode == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        ConfigMode.GLOBAL

    def expectPrompt(self):
        return super(SwitchMicrosens, self).expectPrompt()

    def sendline(self, s=''):
        if (s == ''):
            self.logInfo("send : \\r\\n")
        else:
            self.logInfo("send : {}".format(s))

        if not self.dryrun:
            self.connection.send(s + '\r\n')

    def _ssh_login(self, login, password):
        self.logger.info('SSH not implemented for microsens switches')
        return False

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(self.IP))

        # in telnet microsens switch expect only password
        self.connection.expect('Password:')
        self.connection.sendline('{}\r\n'.format(password))

        self.sendline()
        self.expectPrompt()

        return True

    def logout(self):
        try:
            self.execute('end')
            self.sendline('logout')
            self.logInfo('Logout')

            return True
        except:
            return False

    def getSwitchCommands(self):
        return switchMicrosensCommands
