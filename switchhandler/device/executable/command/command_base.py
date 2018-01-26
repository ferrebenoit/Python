'''
Created on 9 mai 2017

@author: ferreb
'''

from abc import ABCMeta, abstractmethod
from switchhandler.device.device_exception import CommandParameterNotFoundException


class CommandBase(metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self, switch, *args, **kwargs):
        '''
        Constructor
        '''

        # register arguments in current command object
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
                self.kwargs = kwargs

        self.switch = switch

        # Assign default to args
        # self.arg_default()

        self.define_argument()

    def arg_default(self):
        pass

    def run(self):
        return self.do_run()

    def add_argument(self, *args, **kwargs):
        '''
        :param name: le nom de l'option
        :type name: str
        :param required: Argument est-il requis
        :type required: bool
        :param type: type de largument
        :type type: bool
        :param default: la valeur par d�faut
        :type default: str

        if argument is missing
        '''
        # if argument is not found
        if not hasattr(self, kwargs['name']):
            # if argument is required
            if kwargs.get('required', False):
                # raise error
                raise CommandParameterNotFoundException('Parameter {} must be set for command {}'.format(kwargs['name'], self.__class__.__name__))
            # if default is provided
            elif 'default' in kwargs:
                # assign default
                setattr(self, kwargs['name'], kwargs['default'])
        pass

    @abstractmethod
    def define_argument(self):
        pass

    @abstractmethod
    def do_run(self):
        pass
