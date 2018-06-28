'''
Created on 23 nov. 2016

@author: FERREB
'''
# ./save_switch_conf.py --IP 172.17.1.37 --login ferreb --vendor cisco --filterby IP
# ./save_switch_conf.py --csvfile "file.csv" --fieldfilter IP --IP 172.17.1.37 --login ferreb --vendor cisco

from concurrent.futures.thread import ThreadPoolExecutor
from configparser import ConfigParser
import csv
import getpass
import os
from pathlib import Path
import re

from switchhandler.script.custom_argparse import CustomArgumentParser


class ArgFromCSV(object):
    """This class accept a csv file as argument to fill options
        ini file example
            [global]
            username=cg60admin
            csvfile=/opt/cd60.../switchs-all.csv
            jinja...=...
            [172.17.1.1]
            password=test123
            [192.168.100.1]
            password=test1234
            # microsens example
            [10.252.96.[20-255]]
            password=*****


            # microsens password with siteid >> configparser.SECTCRE
            [siteid=100]
            password=****


        ini file localisation (should be configurable by __init__ parameter?)
        /etc/switch_scripter.ini
        ~/.switch_scripter.ini
        subsequent entry in the list override settings from upper


        first load ini_file [global] parameters

        if a csv file is configured by preference order :
            1: from command line args
            2: from ini file
            ouvrir le fichier CSV

            for each line of csv file :
                if filter is enabled check if line must be executed
                    load settings from csv row
                    look at the ip in ini file section
                        if found load settings
                    combine settings from ini file [global] section, ini file [ip] section, csv row and commandline if parameter is redifined the later win

                    prompt for missing settings from the combined settings

                    execute script
        else
            look at the ip in ini file section if found load settings
            combine settings from ini file, and commandline

            prompt for missing settings from the combined settings

            execute script

    """

    def __init__(self, description, args, future_function):

        self.__needed_args = []
        # create argument parser
        self._arg_parser = CustomArgumentParser(description=description)
        # Add script arguments
        self._define_args()
        # Parse command line arguments
        self._arguments = self._parse_argv(args)

        self.future_function = future_function

        self.__csv_file_path = ''

        # Load ini_parameters
        self.__ini_file_path = {'/etc/switchhandler/switchhandler.ini', '{}/.switchhandler/ini_passwd.ini'.format(Path.home())}
        self.__ini_parameters = ConfigParser()
        self.__ini_parameters.read(self.__ini_file_path)  # could pass list of file

        self.__asked_parameters = {}

    def before_process(self):
        pass

    def after_process(self):
        pass

    def _define_args(self):
        self._arg_parser.add_argument('--csvfile', help='A csv file holding arguments')
        self._arg_parser.add_argument('--filterby', help='Informations to retreive from field')
        self._arg_parser.add_argument('--workers', help='Number of threads that will be used', default=5)

    def _add_mandatory_arg(self, *arg):
        for v in arg:
            self.__needed_args.append(v.lower())

    def _script_content(self, args, executor):
        # change here to support thread or disable it for debug
        executor.submit(self.future_function, args)
        # self.future_function(args)

    def _parse_argv(self, args):
        # _ or *_ is for throwing away unneeded values
        known, _ = self._arg_parser.parse_known_args(args)

        return self.__remove_none_args(vars(known))

    def __remove_none_args(self, param_dict):
        return {k: v for k, v in param_dict.items() if v is not None}

    def __ask_arg(self, arg_name):
        tmp_args = {}
        tmp_args[arg_name] = input('Enter a value for {} : '.format(arg_name))

        return self._check_partial_args(tmp_args)

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
        return self._check_partial_args(tmp_args)

    def __convert_to_argv(self, param_dict):
        result = []
        for k, v in param_dict.items():
            result.append('--{}'.format(k))
            result.append(v)
        return result

    # Check
    # to avoid having default values coming back
    def _check_partial_args(self, args):
        result_args = args
        args = self._check_args(args)

        for k, _ in result_args.items():
            if k in args.keys():
                result_args[k] = args[k]

        return result_args

    def _check_args(self, args):
        return self._parse_argv(self.__convert_to_argv(args))

    def _filter_match(self, pattern, string):
        return re.match(pattern, string, re.IGNORECASE)

    def __get_ini_parameters(self, ini_parameters, section):
        if section not in ini_parameters.keys():
            return {}
        else:
            return ini_parameters[section]

    def __need_execution(self, row, filter_by_field_name, filter_by_field_pattern):
        if(filter_by_field_name in row):  # check if parameter passed in filterby is found in csv row
            if self._filter_match(filter_by_field_pattern, row[filter_by_field_name]):  # check if meet the condition Use regular expression instead
                return True
            else:
                return False
        else:
            return True

    def __get_ini_credentials(self, section_value):
        if not section_value or section_value not in self.__ini_parameters.keys():
            return self.__ini_parameters["DEFAULT"]

        # return full ini section
        return self.__ini_parameters[section_value]

    def combine_arguments(self, csv_row=None, ini_file=None, cmd_line_parameters={}):

        # Load default parameters
        if ini_file:
            parameters_ini = self.__get_ini_parameters(ini_file, 'COMMON')
        else:
            parameters_ini = {}

        # load csv parameters
        if csv_row:
            # Check csv values with argument parser
            parameters_csv = self._check_partial_args(csv_row)
        else:
            parameters_csv = {}

        # combine parameters
        arg_result = {**parameters_ini, **parameters_csv, **cmd_line_parameters, **self.__asked_parameters}

        # if ini provided and no password at his time update password with one found in ini file
        if ini_file:
            section_key = arg_result.get('sectionkey', 'ip')
            section_value = arg_result.get(section_key, None)
            ini_section = self.__get_ini_credentials(section_value)

            arg_result = {**ini_section, **arg_result}

        self.__asked_parameters = self.__ask_needed_missing_args(arg_result)
        arg_result.update(self.__asked_parameters)

        return arg_result

    def process(self):
        self.before_process()

        # when reached the end of the with statement self.executor.shutdown() is called that wait for all thread completion
        with ThreadPoolExecutor(max_workers=int(self._arguments['workers'])) as executor:
            # Script called without csv file
            if('csvfile' not in self._arguments):
                self._script_content(self.combine_arguments(cmd_line_parameters=self._arguments, ini_file=self.__ini_parameters), executor)
            # CSV file is not found
            elif(not os.path.isfile(self._arguments['csvfile'])):
                print('CSV File : {} NOT FOUND'.format(self._arguments['csvfile']))
            # CSV file found and filterby argument is provided :
            # Execute script with csv row that matches the filterby argument
            else:
                with open(self._arguments['csvfile']) as csv_file:
                    dict_reader = csv.DictReader(csv_file)
                    filter_by_field_name = self._arguments.get('filterby', None)
                    filter_by_field_pattern = self._arguments.get(filter_by_field_name, None)

                    for row in dict_reader:
                        if self.__need_execution(row, filter_by_field_name, filter_by_field_pattern):
                            # args_builded to not keep values from other ini sections
                            self._script_content(self.combine_arguments(cmd_line_parameters=self._arguments, ini_file=self.__ini_parameters, csv_row=row), executor)

        self.after_process()
