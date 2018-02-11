'''
Created on 10 févr. 2018

@author: ferre
'''
import importlib
import pkgutil


REGISTERED_CLASSES = {}


def registered_class(*decorator_args, **decorator_kwargs):
    '''
    tell that this class should be redistrered
    @registered_class(category='cisco', registered_name='int_vlan')
    '''

    def decorated(cls):
        # get dict name containing the registered classes if no category is given
        # get 'unnamed' category
        category_name = decorator_kwargs.get('category', 'unnamed')

        # get the dict if not found create a new
        category = REGISTERED_CLASSES.get(category_name, None)
        if not category:
            category = REGISTERED_CLASSES[category_name] = {}

        registered_name = decorator_kwargs.get('registered_name', None)

        category[registered_name] = cls

        return cls
    return decorated


def registered_class_scan(*decorator_args, **decorator_kwargs):
    '''
    Tell engine that components must be registered and where to scan
    it import modules in subpackages Not in basepackage
    @registered_class_scan(BasePackage='switchhandler.device.protocol.expect.switch.vendor.cisco')
    '''
    def decorated(cls):
        # import base package
        package = importlib.import_module(decorator_kwargs['BasePackage'])
        # for each module check if this is a package
        for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                # if this is a package scan its content and import modules not packages
                sub_package = importlib.import_module('.' + modname, package.__name__)
                for _, sub_modname, sub_ispkg in pkgutil.iter_modules(sub_package.__path__):
                    if not sub_ispkg:
                        importlib.import_module('.' + sub_modname, sub_package.__name__)

        return cls
        # use wrapt if subclassing
        # class Wrap(cls):
        #    def __init__(self, *args, **kwargs):
        #        print(args)
        #        print(kwargs)
        #        print(self)
        #        print(super(Wrap, self))
        #        super().__init__(*args, **kwargs)

        # return Wrap
    return decorated


def get_registered_classes(category):
    try:
        return REGISTERED_CLASSES[category]
    except Exception:
        raise RegisteredClassCategoryNotFound(
            'Registered class category not found: {}'.format(category))


class RegisteredClassExcpetion(Exception):
    pass


class RegisteredClassExcpetionArg(RegisteredClassExcpetion):
    pass


class RegisteredClassCategoryNotFound(RegisteredClassExcpetion):
    pass
