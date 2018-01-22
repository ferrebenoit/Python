'''
Created on 8 juin 2017

@author: ferreb
'''

from switchhandler.switch.protocol.expect.switch_expect import SwitchExpect, ConfigMode, Exec

from switchhandler.switch.protocol.expect.vendor.microsens import switchMicrosensCommands
from switchhandler.switch.switch_exception import CommandNotFoundException,\
    CommandParameterNotFoundException


class SwitchMicrosens(SwitchExpect):

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

        # self.sendline()
        self.expectPrompt()

        return True

    def logout(self):
        try:
            self.execute('end')
            self.sendline('logout')
            self.logInfo('Logout')

            return True
        except CommandNotFoundException as e:
            self.log_error('raised CommandNotFoundException ' + e)
            return False
        except CommandParameterNotFoundException as e:
            self.log_error('raised CommandParameterNotFoundException ' + e)
            return False
        except Exception as e:
            self.log_error('raised unattended exception ' + e)
            return False

    def getSwitchCommands(self):
        return switchMicrosensCommands
