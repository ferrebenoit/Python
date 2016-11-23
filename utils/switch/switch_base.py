'''
Created on 23 nov. 2016

@author: FERREB
'''
from abc import ABCMeta, abstractmethod
from pexpect import pxssh

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
        
    def login(self, login=None, password=None):
        if(login is None): 
            login = self.__params['login']
        if(password is None):
            password = self.__params['password']

        return self._login(login, password)
        
    def logout(self):
        return self._logout()
        
    def save_conf(self):
        return self._save_conf()
        
    @abstractmethod
    def _login(self, login, password):
        pass
        
    @abstractmethod
    def _logout(self):
        pass
        
    @abstractmethod
    def _save_conf(self):
        pass
