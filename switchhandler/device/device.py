'''
Created on 22 d�c. 2017

@author: ferre
'''
from abc import ABCMeta, abstractmethod
import logging

from switchhandler.device.device_exception import CommandNotFoundException,\
    CommandParameterNotFoundException


class Device(metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self, device, protocol, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''
        # Create logger
        if site:
            self.logger = logging.getLogger(
                '{}.{}.{}.{}.{}'.format(device, protocol, vendor, site, IP))
        else:
            self.logger = logging.getLogger(
                '{}.{}.{}.{}'.format(device, protocol, vendor, IP))

        self.logger.addHandler(logging.NullHandler())

        self.__IP = IP
        self.__site = site
        self.__dryrun = dryrun
        self.__vendor = vendor

        self._connection = None

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
        return self._connection

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
    def getCommands(self):
        pass

    def execute(self, command_name, *args, **kwargs):
        command_class = self.getCommands().get(command_name, None)

        # TODO: Raise excpetion or add an log entry warning
        if command_class is None:
            raise CommandNotFoundException(
                "command with Name {} not implemented".format(command_name))

        command = command_class(self, *args, **kwargs)

        try:
            return command.run()
        except AttributeError as e:
            raise CommandParameterNotFoundException(e)
