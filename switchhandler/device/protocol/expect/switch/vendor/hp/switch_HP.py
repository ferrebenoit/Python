from switchhandler.device.device_exception import CommandNotFoundException,\
    CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import get_registered_classes,\
    registered_class_scan


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect.switch.vendor.hp')
class SwitchHP(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super().__init__(IP, 'hp', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?:tty=(?:ansi|none) )*(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[>#]) '
        # self._PROMPT = '(?:tty=(?:ansi|none) )*([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

    @property
    def hostname(self):
        ''' strip the initial '1H' from the host name
        '''
        hostname = super().hostname
        if not super().hostname == 'None':
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

    def expect_prompt(self, other_messages=None):
        return super(SwitchHP, self).expect_prompt(other_messages)

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

        if password is not None:
            self.connection.expect('[Pp]assword:')
            self.connection.sendline(password)
            self.log_info('Password Sent')

        if self.expect_prompt(other_messages=["Press any key to continue"]) == 1:
            self.log_info("got message: Press any key to continue")
            self.send_line()
            self.expect_prompt()

        self._loadPromptState()

        return True

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(self.IP))
        if self.connection.expect(['Password:', 'Press any key to continue']) == 0:
            self.connection.sendline(password)
            self.expect_prompt()
        else:
            self.connection.sendline()
            self.connection.expect('Password:')
            self.connection.sendline(password)
            self.expect_prompt()

        self._loadPromptState()

        return True

    def logout(self):
        try:
            self.execute('end')
            self.send_line('logout')
            self.expect('[y/n]?')
            self.send('y')

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
        return get_registered_classes(CATEGORY_HP)
