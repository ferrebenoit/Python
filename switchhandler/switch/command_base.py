'''
Created on 9 mai 2017

@author: ferreb
'''

from abc import ABCMeta, abstractmethod


class CommandBase(metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self, switch, *args, **kwargs):
        '''
        Constructor
        '''

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
                self.kwargs = kwargs

        self.switch = switch

        # Assign default to args
        self.arg_default

    def arg_default(self):
        pass

    def run(self):
        return self.do_run()

    @abstractmethod
    def do_run(self):
        pass
