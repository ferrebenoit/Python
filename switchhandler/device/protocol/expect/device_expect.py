'''
Created on 19 janv. 2018

@author: ferre
'''
from abc import abstractmethod

import pexpect

from switchhandler.device.device import Device
from switchhandler.device.device_exception import CommandSyntaxErrorException


try:  # to permit tests on windows platform
    from pexpect import pxssh
except ImportError:
    pass


class DeviceExpect(Device):
    '''
    classdocs
    '''

    def __init__(self, device, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        super().__init__(
            device, 'expect', IP, vendor, site, dryrun)

        self._connection = None
        self.__hostname = None
        self._PROMPT = None

    @property
    def hostname(self):
        return self.__hostname.decode('UTF-8')

    @property
    def prompt(self):
        return self._PROMPT

    @hostname.setter
    def _hostname(self, val):
        self.__hostname = val

    def connect(self):
        try:
            self._connection = pxssh.pxssh(options={
                "StrictHostKeyChecking": "no",
                "UserKnownHostsFile": "/dev/null"})
            self._connection.delaybeforesend = 0.25
            self._connection.PROMPT = self._PROMPT
        except Exception as e:
            self.log_error('Connection failed with exception ' + e)
            return False

        return True

    def before(self):
        return self.connection.before.decode('UTF-8')

    def after(self):
        return self.connection.after.decode('UTF-8')

    def send_line(self, s=''):
        if (s == ''):
            self.log_info("send : \\r\\n")
        else:
            self.log_info("send : {}".format(s))

        if not self.dryrun:
            self.connection.sendline(s)

    def send(self, s):
        self.log_info("send : {}".format(s))

        if not self.dryrun:
            self.connection.send(s)

    def send_control(self, char):
        self.log_info('send : CNTRL/{}'.format(char))

        if not self.dryrun:
            self.connection.sendcontrol(char)

    def send_intr(self):
        self.log_info('send : interrupt')

        if not self.dryrun:
            self.connection.sendintr()

    def send_eof(self):
        self.log_info('send : eof')

        if not self.dryrun:
            self.connection.sendeof()

    def safe_expect(self, pattern, timeout=-1, searchwindowsize=-1, async=False):
        ''' utility method that add pexpect.EOF, pexpect.TIMEOUT to pattern to avoid exceptions
        '''
        localPattern = [pexpect.EOF, pexpect.TIMEOUT]
        if isinstance(pattern, list):
            localPattern.extend(pattern)
        else:
            localPattern.append(pattern)

        match = self.expect(localPattern, timeout, searchwindowsize, async)
        if not self.dryrun:
            if match == 0:
                return pexpect.EOF
            elif match == 1:
                return pexpect.TIMEOUT
            else:
                return match - 2  # return the original index

    def expect(self, pattern, timeout=-1, searchwindowsize=-1, async=False):
        self.log_info('expect : {}'.format(pattern))

        if self.dryrun:
            return 0

        return self.connection.expect(pattern, timeout, searchwindowsize, async)

    @abstractmethod
    def expect_prompt(self, other_messages=None):
        '''retourne 0 si le prompt est matché
        retourne l'index de la liste other_messages en partant de 1
        '''

        self.log_info('expect : PROMPT')
        if self.dryrun:
            return

        self.connection.PROMPT
        expect_list = [self._PROMPT, '% Invalid input detected at \'\^\' marker.']
        if (other_messages is not None):
            expect_list.extend(other_messages)

        match = self.connection.expect(expect_list)

        if match == 1:
            raise CommandSyntaxErrorException(self.after())

        return match - 1  # to ignore the '^' index that indicate syntax error

    @abstractmethod
    def _ssh_login(self, login, password):
        pass

    @abstractmethod
    def _telnet_login(self, login, password):
        pass

    def try_ssh_login(self, login, password):
        try:
            self.logger.info("trying SSH Login")

            if self._ssh_login(login, password):
                self.log_info("SSH Login ok as user {}".format(login))
                return True
            else:
                self.log_warning("SSH Login failed as user {}".format(login))
                return False
        except Exception as e:
            self.log_error('Connection failed with exception')

            self.log_warning("SSH Login failed as user {}".format(login))
            self.log_debug(self.connection.before)
            self.log_debug(self.connection.after)
            self.log_debug('Exception {}'.format(e))
            return False

    def try_telnet_login(self, login, password):
        try:
            self.logger.info("trying TELNET Login")

            if self._telnet_login(login, password):
                self.logger.info("TELNET Login ok as user {}".format(login))
                return True
            else:
                self.log_warning("TELNET Login failed as user {}".format(login))
                return False
        except Exception as e:
            self.log_error('Connection failed with exception')
            self.log_warning("TELNET Login failed as user {}".format(login))
            self.log_debug('exception : {}'.format(e))
            self.log_debug(self.connection.before)
            self.log_debug(self.connection.after)
            return False

    def login(self, login, password):
        if self.dryrun:
            self.log_info("Login ok as user {}".format(login))
            return True

        if not self.try_ssh_login(login, password):
            if not self.try_telnet_login(login, password):
                self.logger.error("Connection error as user {}".format(login))
                return False

        return True
