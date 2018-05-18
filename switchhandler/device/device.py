'''
Created on 22 d�c. 2017

@author: ferre
'''
from abc import ABCMeta, abstractmethod
import logging

from switchhandler.device.device_exception import CommandParameterNotFoundException, CommandSyntaxErrorException


class Device(object, metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self, device, protocol, IP, vendor, site=None, dryrun=False):
        '''
        Constructor
        '''

        self.__fact_cache = {}
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

    def log_info(self, message):
        self.logger.info(message)

    def log_critical(self, message):
        self.logger.critical(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)

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

    def get_fact(self, fact_name, *args, **kwargs):
        self.log_info('Fact : Load "{}"'.format(fact_name))
        if fact_name in self.__fact_cache:
            self.log_info('Fact : Get "{}" from cache'.format(fact_name))
            return self.__fact_cache[fact_name]
        else:
            self.log_info('Fact : Retreive "{}" from device'.format(fact_name))
            fact_result = self.execute(
                'fact_{}'.format(fact_name), *args, **kwargs)
            if fact_result is not None:
                self.__fact_cache[fact_name] = fact_result
                self.log_info('Fact : Store "{}" to cache'.format(fact_name))

            return fact_result

    def execute(self, command_name, *args, **kwargs):
        command_class = self.getCommands().get(command_name, None)

        # TODO: Raise excpetion or add an log entry warning
        if command_class is None:
            self.log_warning("command with Name {} not implemented".format(command_name))
            return False
            # raise CommandNotFoundException(
            #    "command with Name {} not implemented".format(command_name))

        command = command_class(self, *args, **kwargs)

        try:
            return command.run()
        except AttributeError as e:
            raise CommandParameterNotFoundException(e)
        except CommandSyntaxErrorException as e:
            self.log_critical(
                "Syntax error in command {}".format(command_name))
            raise e
