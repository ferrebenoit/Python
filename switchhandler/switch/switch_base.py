'''
Created on 22 déc. 2017

@author: ferre
'''
from abc import ABCMeta, abstractmethod
import logging


class SwitchBase(metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self, protocol, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        # Create logger
        if site:
            self.logger = logging.getLogger(
                'switch.{}.{}.{}.{}'.format(protocol, vendor, site, IP))
        else:
            self.logger = logging.getLogger(
                'switch.{}.{}.{}'.format(protocol, vendor, IP))

        self.logger.addHandler(logging.NullHandler())

        self.__IP = IP
        self.__site = site
        self.__dryrun = dryrun
        self.__vendor = vendor

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
    def dryrun(self):
        return self.__dryrun

    @dryrun.setter
    def dryrun(self, val):
        self.__dryrun = val

    def logInfo(self, message):
        self.logger.info(message)

    def log_critical(self, message):
        self.logger.critical(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def login(self, login, password):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def getSwitchCommands(self):
        pass
