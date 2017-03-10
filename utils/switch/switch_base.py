'''
Created on 23 nov. 2016

@author: FERREB


'''
#def command(self, *validMode, cmdStr, ) 

#liste de fontion a créer 
#utiliser ces fonctions pour simplifier la création de script 

#Enregistrer le hostname

#permettre de passer en mode enable avec le test du passage effectif
#def enable(self)
#def conft(self)

#def exit(self)
#def end(self)


#def configurePubKeyLogin(self, user, key)
#def addVlan(self, ID, DESC)
#def configureVlan(self, ID, DESC, IP)
#def osfp()
#def acl

#... autres a voir

#$ python3 ./save_switch_conf.py --IP "172.17.1.37|172.17.1.38" --login ferreb --filterby IP  --csvfile file.csv

from abc import ABCMeta, abstractmethod
from pexpect import pxssh

import pexpect
from enum import Enum
import logging

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

    def __init__(self, IP, dryrun=False):

        # Create logger
        self.logger = logging.getLogger('switch.{}'.format(IP))
        self.logger.addHandler(logging.NullHandler())
       
        self.__IP = IP
        self.__dryrun = dryrun
               
        self.__hostname = None
        self.__configModeWithParenthesis = None 
        self.__configMode = None
        self.__exec = None
        
        self._PROMPT = None
        
        self.__connection = pxssh.pxssh(options={
                                            "StrictHostKeyChecking": "no",
                                            "UserKnownHostsFile": "/dev/null"})
        
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
    def IP(self):
        return self.__IP
    
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
                return match - 2 # return the original index 
        
    def _loadPromptState(self):
        self.sendline()
        self.expectPrompt()
    
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
    def create_ACL(self, name, acl_entries, acl_replace=None, inverse_src_and_dst = False):
        pass

    @abstractmethod
    def ACL(self, name):
        pass

    @abstractmethod
    def ACL_add_row(self, name, row, acl_replace=None, inverse_src_and_dst = False):
        pass

    @abstractmethod
    def ACL_add_entry(self, name, action, protocol, src1, src2, src_port_operator, dst1, dst2, dst_port_operator, dst_port, log, inverse_src_and_dst = False):
        pass
    
    @abstractmethod
    def add_ospf_router(self, network, ospfwildcard, CIDR):
        pass
    
    @abstractmethod
    def create_vlan(self, ID, name, IP=-1, mask=-1, CIDR=-1, IP_helper=-1):
        pass
    
    @abstractmethod
    def vlan(self, ID, name=None):
        pass

    @abstractmethod
    def int_vlan(self, ID, name=None):
        pass

    @abstractmethod
    def ip_address(self, IP, mask, CIDR):
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
    def save_conf_TFTP(self):
        pass
    
    @abstractmethod
    def expectPrompt(self):
        self.logInfo('expect : PROMPT')
        if self.dryrun:
            return
            
        self.connection.expect(self._PROMPT)
        #load swtch state
        self.__hostname, self.__configModeWithParenthesis, self.__configMode, self.__exec = self.connection.match.groups()
    
    @abstractmethod
    def login(self, login, password):
        try:
            if self.dryrun:
                self.logger.info("Login ok as user {}".format(login))
                return True
            
            if self.connection.login(self.__IP, login, password, auto_prompt_reset=False):
                self._loadPromptState()
                result = True
            else:    
                result =  False
        except:
            self.logger.critical(self.connection.before)
            self.logger.critical(self.connection.after)
            result =  False
            
        if result:
            self.logger.info("Login ok as user {}".format(login))
        else:
            self.logger.error("Login error as user {}".format(login))
        
        return result
            
        
    @abstractmethod
    def logout(self):
        try:
            self.end()
            self.sendline('logout')
            
            return True
        except:
            return False
        
