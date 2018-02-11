'''
Created on 9 mai 2017

@author: ferreb
'''
from builtins import Exception


class deviceHandlerException(Exception):
    pass


class CommandNotFoundException(deviceHandlerException):
    pass


class CommandParameterNotFoundException(deviceHandlerException):
    pass


class CommandSyntaxErrorException(deviceHandlerException):
    pass
