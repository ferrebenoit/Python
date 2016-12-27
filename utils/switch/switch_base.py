'''
Created on 23 nov. 2016

@author: FERREB
'''
from abc import ABCMeta, abstractmethod
from pexpect import pxssh

import pexpect

class SwitchBase(metaclass=ABCMeta):

    def __init__(self, params = None):
        if(params == None):
            params = {}
        else:
            self.params = params
        
        self.__connection = pxssh.pxssh(options={
                                            "StrictHostKeyChecking": "no",
                                            "UserKnownHostsFile": "/dev/null"})
        
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
        
        
    def login(self, IP=None, login=None, password=None):
        if(IP is None):
            IP = self.__params['IP']
        if(login is None): 
            login = self.__params['login']
        if(password is None):
            password = self.__params['password']

        return self._login(IP, login, password)
        
    def logout(self):
        return self._logout()
        
    def save_conf(self):
        return self._save_conf()
        
    @abstractmethod
    def _login(self, IP, login, password):
        try:
            return self.connection.login(self.params['IP'], self.params['login'], self.params['password'], auto_prompt_reset=False)
        except:
            print('login failed')
            return False
        
    @abstractmethod
    def _logout(self):
        try:
            self.connection.logout()
            
            return True
        except:
            return False

        
    @abstractmethod
    def _save_conf(self):
        pass
