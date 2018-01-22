from switchhandler.switch.protocol.expect.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.switch.protocol.expect.vendor.allied import switchAlliedCommands
from switchhandler.switch.switch_exception import CommandNotFoundException,\
    CommandParameterNotFoundException


class SwitchAllied(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchAllied, self).__init__(IP, 'allied', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[>#])$'

    def getExecLevel(self):
        if self.exec_mode == '>':
            return Exec.USER
        elif self.exec_mode == '#':
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

    def expectPrompt(self, other_messages=None):
        return super(SwitchAllied, self).expectPrompt(other_messages)

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

        # Password is found send password
        if self.expectPrompt(other_messages=['[Pp]assword:']) == 1:
            self.connection.sendline(password)
            self.logInfo('Password Sent')
            self.expectPrompt()

        # self.expectPrompt()  # need duplicate expect pompt

        return True

    # not implemented
    def _telnet_login(self, login, password):
        self.logger.info('TELNET not implemented for allied switches')
        return False

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
        return switchAlliedCommands
