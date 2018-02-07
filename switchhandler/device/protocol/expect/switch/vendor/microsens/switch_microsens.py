'''
Created on 8 juin 2017

@author: ferreb
'''

from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec

from switchhandler.device.protocol.expect.switch.vendor.microsens import switchMicrosensCommands
from switchhandler.device.device_exception import CommandNotFoundException,\
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

    def expect_prompt(self):
        return super(SwitchMicrosens, self).expect_prompt()

    def send_line(self, s=''):
        if (s == ''):
            self.log_info("send : \\r\\n")
        else:
            self.log_info("send : {}".format(s))

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
        self.connection.send_line('{}\r\n'.format(password))

        # self.send_line()
        self.expect_prompt()

        return True

    def logout(self):
        try:
            self.execute('end')
            self.send_line('logout')
            self.log_info('Logout')

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

    def getCommands(self):
        return switchMicrosensCommands
