# coding: utf-8
'''
Created on 23 nov. 2016

@author: FERREB
'''

from switchhandler.device.protocol.expect.switch.switch_expect import SwitchExpect, ConfigMode, Exec
from switchhandler.device.protocol.expect.switch.vendor.cisco import switchCiscoCommands
from switchhandler.device.device_exception import CommandNotFoundException,\
    CommandParameterNotFoundException


class SwitchCisco(SwitchExpect):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchCisco, self).__init__(IP, 'cisco', site, dryrun)

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

    def expectPrompt(self, other_messages=None):
        return super(SwitchCisco, self).expectPrompt(other_messages)

    def _ssh_login(self, login, password):
        self.connect()
        self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

        # Password is found send password
        if self.expectPrompt(other_messages=['[Pp]assword:']) == 1:
            self.connection.sendline(password)
            self.logInfo('Password Sent')
            self.expectPrompt()

        return True

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(self.IP))

        self.connection.expect('Username:')
        self.connection.sendline(login)

        self.connection.expect('Password:')
        self.connection.sendline(password)

        # self._loadPromptState()

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

    def getCommands(self):
        return switchCiscoCommands
