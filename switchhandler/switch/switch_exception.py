'''
Created on 9 mai 2017

@author: ferreb
'''
from builtins import Exception


class switchHandlerException(Exception):
    pass


class CommandNotFoundException(switchHandlerException):
    pass


class CommandParameterNotFoundException(switchHandlerException):
    pass
