'''
Created on 7 avr. 2017

@author: ferreb
'''

from argparse import ArgumentParser

class CustomArgumentParser(ArgumentParser):
    
    def add_argument(self, *args, **kwargs):
        lowerargs = []

        for arg in args:
            lowerargs.append(arg.lower())
        
        
        lowerargs = tuple(lowerargs)

        return super().add_argument(*lowerargs, **kwargs)
        

    def parse_known_args(self, args=None, namespace=None):
        lowerargs = []
        
        for arg in args:
            if (len(arg) > 0) and (arg[0] in ['-']):
                lowerargs.append(arg.lower())
            else:
                lowerargs.append(arg)
        
        return super().parse_known_args(lowerargs, namespace)