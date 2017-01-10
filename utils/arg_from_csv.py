'''
Created on 23 nov. 2016

@author: FERREB
'''
#./save_switch_conf.py --IP 172.17.1.37 --login ferreb --vendor cisco --filterby IP
#./save_switch_conf.py --csvfile "file.csv" --fieldfilter IP --IP 172.17.1.37 --login ferreb --vendor cisco 

import argparse
import os
import csv
import getpass
import re
from _csv import reader

class ArgFromCSV:
    "Base class that accept arguments from CSV File"
    
    def __init__(self, description, args):
        self.__needed_args = []
        # create argument parser
        self._arg_parser = argparse.ArgumentParser(description=description)
        # Add script arguments
        self._define_args()
        # Parse command line arguments
        self.__arguments = self._parse_argv(args)
        
    def __remove_none_args(self, param_dict):
        return {k:v for k,v in param_dict.items() if v is not None}
        
    def _define_args(self):
        self._arg_parser.add_argument('--csvfile', help='A csv file holding arguments')
        self._arg_parser.add_argument('--filterby', help='Informations to retreive from field')
        
    
    def _parse_argv(self, args):
        known, unknown = self._arg_parser.parse_known_args(args)
        return self.__remove_none_args(vars(known))
        
    def _add_mandatory_arg(self, *arg):
        for v in arg:
            self.__needed_args.append(v)
          
    def __ask_needed_missing_args(self, args):
    
        tmp_args = {}
        for v in self.__needed_args:
            if(not v in args):
                if(v == 'password'):
                    tmp_args[v] = getpass.getpass('Enter a value for {} : '.format(v))
                else:
                    tmp_args[v] = input('Enter a value for {} : '.format(v))
            
        # Check 
        tmp_args = self._check_args(tmp_args)
        
        return tmp_args
    
    def __convert_to_argv(self, param_dict):
        result = []
        for k,v in param_dict.items():
            result.append('--{}'.format(k))
            result.append(v)
        return result
    
    def _script_content(self, args):
        pass
    
    def _check_args(self, args):
        return self._parse_argv(self.__convert_to_argv(args))
    
    def __execute_with_csv_row(self, row, ask_needed_missing_args=True):
        # Check csv values with argument parser
        row = self._check_args(row)
    
        # Merge command line args with csv arguments. Command line args superseed csv args
        row.update(self.__arguments)

        # chek for missing args from csv and command line if this is the first data line
        if(ask_needed_missing_args):
            self.__arguments.update(self.__ask_needed_missing_args(row))
            row.update(self.__arguments)
                        
                    
        # Execute script
        self._script_content(row)    
        
    def _filter_match(self, pattern, string):
        return re.match(pattern, string) 
        
    def process(self):
        if(not 'csvfile' in self.__arguments):
            self.__arguments.update(self.__ask_needed_missing_args(self.__arguments))
            self._script_content(self.__arguments)
        elif(not os.path.isfile(self.__arguments['csvfile'])):
            print('CSV File : {} NOT FOUND'.format(self.__arguments['csvfile']))
        elif('filterby' in self.__arguments):
            with open(self.__arguments['csvfile']) as csv_file:
                reader = csv.DictReader(csv_file)
                filter_by_field_name = self.__arguments['filterby']
                filter_by_field_pattern = self.__arguments[filter_by_field_name]
                
                
                for row in reader:
                    if(filter_by_field_name in row): # check if parameter passed in filterby is found in csv row
                        if self._filter_match(filter_by_field_pattern, row[filter_by_field_name]): # check if meet the condition Use regular expression instead
                            self.__arguments[filter_by_field_name] = row[filter_by_field_name] 
                            self.__execute_with_csv_row(row)
        else:
            with open(self.__arguments['csvfile']) as csv_file:
                reader = csv.DictReader(csv_file)
                
                for row in reader:
                    self.__execute_with_csv_row(row, reader.line_num == 2)
                   
            
    
