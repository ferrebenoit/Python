'''
Created on 23 nov. 2016

@author: FERREB


'''
# def command(self, *validMode, cmdStr, )

# liste de fontion a créer
# utiliser ces fonctions pour simplifier la création de script

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

from abc import ABCMeta, abstractmethod
import datetime
from enum import Enum
import logging

from pexpect import pxssh
import pexpect
from switchhandler.switch.switch_exception import CommandNotFoundException


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


class SwitchBase(metaclass=ABCMeta):

    def __init__(self, IP, vendor, site=None, dryrun=False):

        # Create logger
        if site:
            self.logger = logging.getLogger('switch.{}.{}.{}'.format(vendor, site, IP))
        else:
            self.logger = logging.getLogger('switch.{}.{}'.format(vendor, IP))

        self.logger.addHandler(logging.NullHandler())

        self.__IP = IP
        self.__site = site
        self.__dryrun = dryrun
        self.__vendor = vendor

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
    def exec(self):
        if not self.__exec:
            return None

        return self.__exec.decode('UTF-8')

    @property
    def configModeWithParenthesis(self):
        self.__configModeWithParenthesis = self._loadPromptState()
        return self.__configModeWithParenthesis

    @property
    def vendor(self):
        return self.__vendor

    @property
    def IP(self):
        return self.__IP

    @property
    def site(self):
        return self.__site

    @property
    def connection(self):
        return self.__connection

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, val):
        self.__params = val

    @property
    def dryrun(self):
        return self.__dryrun

    @dryrun.setter
    def dryrun(self, val):
        self.__dryrun = val

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

    def logInfo(self, message):
        self.logger.info(message)

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
    def delete_acl(self, name):
        pass

    @abstractmethod
    def create_ACL(self, name, acl_entries, acl_replace=None, inverse_src_and_dst=False):
        pass

    @abstractmethod
    def ACL(self, name):
        pass

    def ACL_add_row(self, name, row, acl_replace=None, inverse_src_and_dst=False):
        if acl_replace is not None:
            for k in row.keys():
                if(k in acl_replace):
                    row[k] = row[k].format(**acl_replace[k])

        # if condition in row['condition']:

        self.ACL_add_entry(name,
                           row['index'],
                           row['action'],
                           row['protocol'],
                           row['src1'],
                           row['src2'],
                           row['src_port_operator'],
                           row['src_port'],
                           row['dst1'],
                           row['dst2'],
                           row['dst_port_operator'],
                           row['dst_port'],
                           row['log'],
                           inverse_src_and_dst)

    @abstractmethod
    def ACL_add_entry(self, name, action, protocol, src1, src2, src_port_operator, dst1, dst2, dst_port_operator, dst_port, log, inverse_src_and_dst=False):
        pass

    @abstractmethod
    def add_acl_to_interface(self, acl_name, interface_name, inbound=True):
        pass

    @abstractmethod
    def add_ospf_router(self, network, networkID):
        pass

    @abstractmethod
    def create_vlan(self, ID, name, IP=-1, network=-1, IP_helper=-1):
        pass

    @abstractmethod
    def vlan(self, ID, name=None):
        pass

    @abstractmethod
    def int_vlan(self, ID, name=None):
        pass

    @abstractmethod
    def ip_address(self, IP, network):
        pass

    @abstractmethod
    def ip_helper(self, IP):
        pass

    @abstractmethod
    def auth_PublicKey(self, username, key, comment, TFTP_IP=''):
        pass

    @abstractmethod
    def uploadFileTFTP(self, localFilePath, RemoteFilePath):
        pass

    @abstractmethod
    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def conft(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def save_conf_TFTP(self, TFTP_IP, folder=None, add_timestamp=False):
        pass

    @abstractmethod
    def ping(self, ip, repeat=5):
        pass

    @abstractmethod
    def find_port_from_mac(self, mac, ip=None):
        pass

    @abstractmethod
    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
        pass

    @abstractmethod
    def expectPrompt(self):
        self.logInfo('expect : PROMPT')
        if self.dryrun:
            return

        self.connection.expect(self._PROMPT)
        # load swtch state
        self.__hostname, self.__configModeWithParenthesis, self.__configMode, self.__exec = self.connection.match.groups()

        self.logger.debug('before {}'.format(self.connection.before))
        self.logger.debug('after {}'.format(self.connection.after))

    @abstractmethod
    def login(self, login, password):
        try:
            if self.dryrun:
                self.logger.info("Login ok as user {}".format(login))
                return True

            self.connect()
            if self.connection.login(self.__IP, login, password, auto_prompt_reset=False):
                self._loadPromptState()
                result = True
                self.logger.info("Login ok as user {}".format(login))
            else:
                result = False
                self.logger.error("Login error as user {}".format(login))
        except:
            self.logger.critical(self.connection.before)
            self.logger.critical(self.connection.after)
            self.logger.error("Connection error")
            result = False

        return result

    @abstractmethod
    def logout(self):
        try:
            self.end()
            self.sendline('logout')

            return True
        except:
            return False

    @abstractmethod
    def getSwitchCommands(self):
        pass

    def execute(self, command_name, *args, **kwargs):
        command_class = self.getSwitchCommands().get(command_name, None)

        # TODO: Raise excpetion or add an log entry warning
        if command_class is None:
            raise CommandNotFoundException("command with Name {} not implemented".format(command_name))

        command = command_class(self, *args, **kwargs)

        return command.run()
