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

class Exec(Enum):
    USER = 1
    PRIVILEGED = 2
    
class ConfigMode(Enum):
    GLOBAL = 1
    TERMINAL = 2
    INTERFACE = 3    
    VLAN = 3    

class SwitchBase(metaclass=ABCMeta):

    def __init__(self, IP):
       
       
        self.__IP = IP
               
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
            return 'None'
        
        return self.__hostname.decode('UTF-8')

    @property
    def configMode(self):
        if not self.__configMode:
            return 'None'

        return self.__configMode.decode('UTF-8')

    @property
    def exec(self):
        if not self.__exec:
            return 'None'
        
        return self.__exec.decode('UTF-8')

    @property
    def configModeWithParenthesis(self):
        self.__configModeWithParenthesis = self._loadPromptState()
        return self.__configModeWithParenthesis
        
    @property
    def connection(self):
        return self.__connection
    
    @property
    def params(self):
        return self.__params
    
    @params.setter
    def params(self, val):
        self.__params = val
        
    def safeExpect(self, pattern, timeout=-1, searchwindowsize=-1, async=False):
        ''' utility method that add pexpect.EOF, pexpect.TIMEOUT to pattern to avoid exceptions
        '''
        localPattern = [pexpect.EOF, pexpect.TIMEOUT]
        if isinstance(pattern, list):
            localPattern.extend(pattern)
        else:
            localPattern.append(pattern)
        
        match = self.connection.expect(localPattern, timeout, searchwindowsize, async)
        if match == 0:
            return pexpect.EOF
        elif match == 1:
            return pexpect.TIMEOUT
        else:
            return match - 2 # return the original index 
        
    def _loadPromptState(self):
        self.connection.sendline()
        self.expectPrompt()
        
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
    def save_conf_TFTP(self):
        pass
    
    @abstractmethod
    def expectPrompt(self):
        self.connection.expect(self._PROMPT)
        #load swtch state
        self.__hostname, self.__configModeWithParenthesis, self.__configMode, self.__exec = self.connection.match.groups()
    
    @abstractmethod
    def login(self, login, password):
        try:
            if self.connection.login(self.__IP, login, password, auto_prompt_reset=False):
                self._loadPromptState()
                return True
            else:    
                return False
        except:
            print('login failed')
            print(self.connection.before)
            print(self.connection.after)
            return False
        
    @abstractmethod
    def logout(self):
        try:
            self.connection.logout()
            
            return True
        except:
            return False
        
