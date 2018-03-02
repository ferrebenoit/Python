from switchhandler.device.device_exception import CommandNotFoundException,\
    CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import get_registered_classes,\
    registered_class_scan


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect.switch.vendor.allied')
class SwitchAllied(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super().__init__(IP, 'allied', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[>#])$'

    def getExecLevel(self):
        if self.exec_mode == '>':
            return Exec.USER
        elif self.exec_mode == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        if self.configMode is None:
            return ConfigMode.GLOBAL
        elif self.configMode == 'config':
            return ConfigMode.TERMINAL
        elif self.configMode == 'config-if':
            return ConfigMode.INTERFACE
        elif self.configMode == 'config-vlan':  # vlan database
            return ConfigMode.VLAN

    def expect_prompt(self, other_messages=None):
        return super().expect_prompt(other_messages)

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

        # Password is found send password
        if self.expect_prompt(other_messages=['[Pp]assword:']) == 1:
            self.connection.sendline(password)
            self.log_info('Password Sent')
            self.expect_prompt()

        # self.expect_prompt()  # need duplicate expect pompt

        return True

    # not implemented
    def _telnet_login(self, login, password):
        self.logger.info('TELNET not implemented for allied switches')
        return False

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
        return get_registered_classes(CATEGORY_ALLIED)
