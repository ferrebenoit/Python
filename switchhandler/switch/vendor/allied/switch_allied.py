from switchhandler.switch.switch_base import SwitchBase, ConfigMode, Exec
from switchhandler.switch.vendor.allied import switchAlliedCommands


class SwitchAllied(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchAllied, self).__init__(IP, 'allied', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[>#])$'

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

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))
        self.connection.expect('password:')
        self.connection.sendline(password)

        self._loadPromptState()

        self.expectPrompt()
        self.expectPrompt()  # need duplicate expect pompt

        return True

    # not implemented
    def _telnet_login(self, login, password):
        self.logger.info('TELNET not implemented for allied switches')
        return False

    def logout(self):
        return super(SwitchAllied, self).logout()

    def getSwitchCommands(self):
        return switchAlliedCommands
