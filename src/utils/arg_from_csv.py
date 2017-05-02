'''
Created on 23 nov. 2016

@author: FERREB
'''
# ./save_switch_conf.py --IP 172.17.1.37 --login ferreb --vendor cisco --filterby IP
# ./save_switch_conf.py --csvfile "file.csv" --fieldfilter IP --IP 172.17.1.37 --login ferreb --vendor cisco

import csv
import getpass
import os
import re

from utils.script.custom_argparse import CustomArgumentParser


class ArgFromCSV:
    """This function does something.

        :param description: La description du script.
        :type description: str
        :arg args: Les parametres du script a parser.
        :type args: dict

    """

    def __init__(self, description, args):

        self.__needed_args = []
        # create argument parser
        self._arg_parser = CustomArgumentParser(description=description)
        # Add script arguments
        self._define_args()
        # Parse command line arguments
        self._arguments = self._parse_argv(args)

    def __remove_none_args(self, param_dict):
        return {k: v for k, v in param_dict.items() if v is not None}

    def _define_args(self):
        self._arg_parser.add_argument('--csvfile', help='A csv file holding arguments')
        self._arg_parser.add_argument('--filterby', help='Informations to retreive from field')

    def _parse_argv(self, args):
        known, unknown = self._arg_parser.parse_known_args(args)

        return self.__remove_none_args(vars(known))

    def _add_mandatory_arg(self, *arg):
        for v in arg:
            self.__needed_args.append(v.lower())

    def __ask_needed_missing_args(self, args):

        tmp_args = {}
        for v in self.__needed_args:
            if(v not in args):
                if(v == 'password'):
                    tmp_args[v] = getpass.getpass('Enter a value for {} : '.format(v))
                else:
                    tmp_args[v] = input('Enter a value for {} : '.format(v))

        # Check
        # to avoid having default values coming back
        result_args = tmp_args
        tmp_args = self._check_args(tmp_args)

        for k, v in result_args.items():
            result_args[k] = tmp_args[k]

        return result_args

    def __convert_to_argv(self, param_dict):
        result = []
        for k, v in param_dict.items():
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
        row.update(self._arguments)

        # chek for missing args from csv and command line if this is the first data line
        if(ask_needed_missing_args):
            self._arguments.update(self.__ask_needed_missing_args(row))
            row.update(self._arguments)

        # Execute script
        self._script_content(row)

    def _filter_match(self, pattern, string):
        return re.match(pattern, string, re.IGNORECASE)

    def process(self):
        """
            La fonction à appeler pour exécuter le script
        """
        if('csvfile' not in self._arguments):
            self._arguments.update(self.__ask_needed_missing_args(self._arguments))

            self._script_content(self._arguments)
        elif(not os.path.isfile(self._arguments['csvfile'])):
            print('CSV File : {} NOT FOUND'.format(self._arguments['csvfile']))
        elif('filterby' in self._arguments):
            with open(self._arguments['csvfile']) as csv_file:
                dict_reader = csv.DictReader(csv_file)
                filter_by_field_name = self._arguments['filterby']
                filter_by_field_pattern = self._arguments[filter_by_field_name]

                for row in dict_reader:
                    if(filter_by_field_name in row):  # check if parameter passed in filterby is found in csv row
                        if self._filter_match(filter_by_field_pattern, row[filter_by_field_name]):  # check if meet the condition Use regular expression instead
                            self._arguments[filter_by_field_name] = row[filter_by_field_name]
                            self.__execute_with_csv_row(row)
        else:
            with open(self._arguments['csvfile']) as csv_file:
                dict_reader = csv.DictReader(csv_file)

                for row in dict_reader:
                    self.__execute_with_csv_row(row, dict_reader.line_num == 2)
