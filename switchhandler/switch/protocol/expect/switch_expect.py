'''
Created on 23 nov. 2016

@author: FERREB


'''
# def command(self, *validMode, cmdStr, )

# liste de fontion a cr�er
# utiliser ces fonctions pour simplifier la cr�ation de script

# Enregistrer le hostname

# permettre de passer en mode enable avec le test du passage effectif
# def enable(self)
# def conft(self)

# def exit(self)
# def end(self)


# def configurePubKeyLogin(self, user, key)
# def addVlan(self, ID, DESC)
# def configureVlan(self, ID, DESC, IP)
# def osfp()
# def acl

# autres a voir

# $ python3 ./save_switch_conf.py --IP "172.17.1.37|172.17.1.38" --login ferreb --filterby IP  --csvfile file.csv

from abc import abstractmethod
from builtins import AttributeError
import datetime
from enum import Enum

from pexpect import pxssh
import pexpect

from switchhandler.switch.switch_base import SwitchBase

from switchhandler.switch.switch_exception import CommandNotFoundException,\
    CommandParameterNotFoundException


class Exec(Enum):
    USER = 1
    PRIVILEGED = 2


class ConfigMode(Enum):
    GLOBAL = 1
    TERMINAL = 2
    INTERFACE = 3
    VLAN = 3
    PUBKEY = 4
    PUBKEY_USER = 5


class SwitchExpect(SwitchBase):

    def __init__(self, IP, vendor, site=None, dryrun=False):
        super(SwitchExpect, self).__init__('expect', IP, vendor, site, dryrun)

        self.__hostname = None
        self.__configModeWithParenthesis = None
        self.__configMode = None
        self.__exec = None

        self._PROMPT = None

        self.__connection = None

    def connect(self):
        try:
            self.__connection = pxssh.pxssh(options={
                                            "StrictHostKeyChecking": "no",
                                            "UserKnownHostsFile": "/dev/null"})
            self.__connection.delaybeforesend = 0.25
            self.__connection.PROMPT = self._PROMPT
        except:
            return False

        return True

    @abstractmethod
    def getExecLevel(self):
        pass

    @abstractmethod
    def getConfigMode(self):
        pass

    @property
    def prompt(self):
        return self._PROMPT

    @property
    def hostname(self):
        if not self.__hostname:
            return None

        return self.__hostname.decode('UTF-8')

    @property
    def configMode(self):
        if not self.__configMode:
            return None

        return self.__configMode.decode('UTF-8')

    @property
    def exec_mode(self):
        if not self.__exec:
            return None

        return self.__exec.decode('UTF-8')

    @property
    def configModeWithParenthesis(self):
        if not self.__configModeWithParenthesis:
            return None

        return self.__configModeWithParenthesis.decode('UTF-8')

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, val):
        self.__params = val

    def before(self):
        return self.connection.before.decode('UTF-8')

    def after(self):
        return self.connection.after.decode('UTF-8')

    def safeExpect(self, pattern, timeout=-1, searchwindowsize=-1, async=False):
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

    def _loadPromptState(self):
        self.sendline()
        self.expectPrompt()

    def _build_tftp_filepath(self, folder, add_timestamp):
        filepath = "{}_{}_{}".format(self.IP, self.hostname, self.vendor)

        if folder:
            filepath = "{}/{}".format(folder, filepath)

        if add_timestamp:
            filepath = "{}_{:%Y%m%d-%H%M%S}".format(filepath, datetime.datetime.today())

        return filepath

    def sendline(self, s=''):
        if (s == ''):
            self.logInfo("send : \\r\\n")
        else:
            self.logInfo("send : {}".format(s))

        if not self.dryrun:
            self.connection.sendline(s)

    def send(self, s):
        self.logInfo("send : {}".format(s))

        if not self.dryrun:
            self.connection.send(s)

    def sendcontrol(self, char):
        self.logInfo('send : CNTRL/{}'.format(char))

        if not self.dryrun:
            self.connection.sendcontrol(char)

    def sendintr(self):
        self.logInfo('send : interrupt')

        if not self.dryrun:
            self.connection.sendintr()

    def sendeof(self):
        self.logInfo('send : eof')

        if not self.dryrun:
            self.connection.sendeof()

    def expect(self, pattern, timeout=-1, searchwindowsize=-1, async=False):
        self.logInfo('expect : {}'.format(pattern))

        if self.dryrun:
            return 0

        return self.connection.expect(pattern, timeout, searchwindowsize, async)

    @abstractmethod
    def expectPrompt(self, other_messages=None):
        '''retourne 0 si le prompt est matché
        retourne l'index de la liste other_messages en partant de 1
        '''

        self.logInfo('expect : PROMPT')
        if self.dryrun:
            return

        expect_list = [self._PROMPT]
        if (other_messages is not None):
            expect_list.extend(other_messages)

        match = self.connection.expect(expect_list)

        # load swtch state
        self.__hostname = self.connection.match.groupdict().get('hostname', None)
        self.__configModeWithParenthesis = self.connection.match.groupdict().get('configModeWithParenthesis', None)
        self.__configMode = self.connection.match.groupdict().get('configMode', None)
        self.__exec = self.connection.match.groupdict().get('exec', None)

        self.logger.debug('before {}'.format(self.connection.before))
        self.logger.debug('after {}'.format(self.connection.after))

        return match

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
                self.logger.info("SSH Login ok as user {}".format(login))
                return True
            else:
                return False
        except:

            self.logger.warning("SSH Login failed as user {}".format(login))
            self.logger.warning(self.connection.before)
            self.logger.warning(self.connection.after)
            return False

    def try_telnet_login(self, login, password):
        try:
            self.logger.info("trying TELNET Login")

            if self._telnet_login(login, password):
                self.logger.info("TELNET Login ok as user {}".format(login))
                return True
            else:
                return False
        except:
            self.logger.warning("TELNET Login failed")
            self.logger.warning(self.connection.before)
            self.logger.warning(self.connection.after)
            return False

    def login(self, login, password):
        if self.dryrun:
            self.logger.info("Login ok as user {}".format(login))
            return True

        if not self.try_ssh_login(login, password):
            if not self.try_telnet_login(login, password):
                self.logger.error("Connection error as user {}".format(login))
                return False

        return True

    def execute(self, command_name, *args, **kwargs):
        command_class = self.getSwitchCommands().get(command_name, None)

        # TODO: Raise excpetion or add an log entry warning
        if command_class is None:
            raise CommandNotFoundException("command with Name {} not implemented".format(command_name))

        command = command_class(self, *args, **kwargs)

        try:
            return command.run()
        except AttributeError as e:
            raise CommandParameterNotFoundException(e)
