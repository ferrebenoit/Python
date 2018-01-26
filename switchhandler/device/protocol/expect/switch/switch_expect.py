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
import datetime
from enum import Enum

from switchhandler.device.protocol.expect.device_expect import DeviceExpect


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


class SwitchExpect(DeviceExpect):

    def __init__(self, IP, vendor, site=None, dryrun=False):
        super(SwitchExpect, self).__init__('switch', IP, vendor, site, dryrun)

        self.__configModeWithParenthesis = None
        self.__configMode = None
        self.__exec = None

    @abstractmethod
    def getExecLevel(self):
        pass

    @abstractmethod
    def getConfigMode(self):
        pass

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

    def _loadPromptState(self):
        self.sendline()
        self.expectPrompt()

    def _build_tftp_filepath(self, folder, add_timestamp):
        filepath = "{}_{}_{}".format(self.IP, self.hostname, self.vendor)

        if folder:
            filepath = "{}/{}".format(folder, filepath)

        if add_timestamp:
            filepath = "{}_{:%Y%m%d-%H%M%S}".format(
                filepath, datetime.datetime.today())

        return filepath

    def expectPrompt(self, other_messages=None):
        match = super(SwitchExpect, self).expectPrompt(other_messages)

        # load swtch state
        self._hostname = self.connection.match.groupdict().get('hostname', None)
        self.__configModeWithParenthesis = self.connection.match.groupdict().get(
            'configModeWithParenthesis', None)
        self.__configMode = self.connection.match.groupdict().get('configMode', None)
        self.__exec = self.connection.match.groupdict().get('exec', None)

        return match
