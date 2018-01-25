from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.device.protocol.expect.switch.vendor.hp import switchHPCommands


class SwitchHP(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchHP, self).__init__(IP, 'hp', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?:tty=(?:ansi|none) )*(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[>#]) '
        # self._PROMPT = '(?:tty=(?:ansi|none) )*([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

    @property
    def hostname(self):
        ''' strip the initial '1H' from the host name
        '''
        hostname = super(SwitchHP, self).hostname
        if not super(SwitchHP, self).hostname == 'None':
            hostname = hostname[2:]

        return hostname

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

    def expectPrompt(self, other_messages=None):
        return super(SwitchHP, self).expectPrompt(other_messages)

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

        if password is not None:
            self.connection.expect('[Pp]assword:')
            self.connection.sendline(password)
            self.logInfo('Password Sent')

        if self.expectPrompt(other_messages=["Press any key to continue"]) == 1:
            self.logInfo("got message: Press any key to continue")
            self.sendline()
            self.expectPrompt()

        self._loadPromptState()

        return True

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(self.IP))
        if self.connection.expect(['Password:', 'Press any key to continue']) == 0:
            self.connection.sendline(password)
            self.expectPrompt()
        else:
            self.connection.sendline()
            self.connection.expect('Password:')
            self.connection.sendline(password)
            self.expectPrompt()

        self._loadPromptState()

        return True

    def logout(self):
        try:
            self.execute('end')
            self.sendline('logout')
            self.expect('[y/n]?')
            self.send('y')

            self.logInfo('Logout')
            return True
        except:
            return False

    def getCommands(self):
        return switchHPCommands
