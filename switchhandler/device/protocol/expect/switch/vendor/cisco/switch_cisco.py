# coding: utf-8
'''
Created on 23 nov. 2016

@author: FERREB
'''

from switchhandler.device.device_exception import CommandNotFoundException,\
    CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class_scan,\
    get_registered_classes


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect.switch.vendor.cisco')
class SwitchCisco(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super().__init__(IP, 'cisco', site, dryrun)

        # prompt rexex
        self._PROMPT = '(?P<hostname>[A-Za-z0-9\-]*)(?P<configModeWithParenthesis>\((?P<configMode>.*)\))*(?P<exec>[$#])$'

    def getExecLevel(self):
        if self.exec_mode == '$':
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
        elif self.configMode == 'config-vlan':
            return ConfigMode.VLAN
        elif self.configMode == 'conf-ssh-pubkey':
            return ConfigMode.PUBKEY
        elif self.configMode == 'conf-ssh-pubkey-user':
            return ConfigMode.PUBKEY_USER

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

        return True

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(self.IP))

        self.connection.expect('Username:')
        self.connection.sendline(login)

        self.connection.expect('Password:')
        self.connection.sendline(password)

        # self._loadPromptState()

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
        return get_registered_classes(CATEGORY_CISCO)
