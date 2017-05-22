'''
Created on 23 nov. 2016

@author: FERREB
'''
import logging.handlers
import re

from switchhandler.arg_from_csv import ArgFromCSV

from switchhandler.switch.allied.switch_allied import SwitchAllied
from switchhandler.switch.cisco.switch_cisco import SwitchCisco
from switchhandler.switch.hp.switch_HP import SwitchHP


class SwitchScripter(ArgFromCSV):
    "Class That desactivate an wifi AP"

    def __init__(self, description, args):
        ArgFromCSV.__init__(self, description, args)

        self._logging_config(self._arguments['loglevel'].upper(), self._arguments['screenlog'] == 'yes', self._arguments['filelog'])

    def _logging_config(self, loglevel, screenlog, fileLog):
        logger = logging.getLogger('switch')
        logger.setLevel(loglevel)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if screenlog:
            screenHandler = logging.StreamHandler()
            screenHandler.setFormatter(formatter)
            logger.addHandler(screenHandler)

        if fileLog != 'none':
            fileHandler = logging.handlers.TimedRotatingFileHandler(fileLog, when='midnight')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--loglevel', help='Loglevel', choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
        self._arg_parser.add_argument('--screenlog', help='Print log on screen', choices=['yes', 'no'], default='yes')
        self._arg_parser.add_argument('--filelog', help='Save la on file', default='none')

        self._arg_parser.add_argument('--dryrun', help='No Action taken! Only print what would have been executed.', choices=['yes', 'no'], default='no')

        self._arg_parser.add_argument('--ip', help='Switch IP address')
        self._arg_parser.add_argument('--login', help='login')
        self._arg_parser.add_argument('--password', help='password')
        self._arg_parser.add_argument('--vendor', '--type', help='the vendor')
        self._arg_parser.add_argument('--switchname', help='the switch name')
        self._arg_parser.add_argument('--site', help='The switch site')

        self._add_mandatory_arg('IP', 'vendor', 'login', 'password')

    def _script_content(self, args):
        if(re.compile('cisco', flags=re.IGNORECASE).search(args['vendor'])):
            # if(args['vendor'].lower().contains('cisco')):
            self._script_content_cisco(SwitchCisco(args['ip'], args.get('site', None), args['dryrun'] == 'yes'), args)
        if(re.compile('hp', flags=re.IGNORECASE).search(args['vendor'])):
            # elif(args['vendor'].lower().contains('hp')):
            self._script_content_hp(SwitchHP(args['ip'], args.get('site', None), args['dryrun'] == 'yes'), args)
        if(re.compile('allied', flags=re.IGNORECASE).search(args['vendor'])):
            # elif(args['vendor'].lower().contains('allied')):
            self._script_content_allied(SwitchAllied(args['ip'], args.get('site', None), args['dryrun'] == 'yes'), args)

    def _script_content_cisco(self, switch_cisco, args):
        self._common_actions(switch_cisco, args)

    def _script_content_hp(self, switch_allied, args):
        self._common_actions(switch_allied, args)

    def _script_content_allied(self, switch_hp, args):
        self._common_actions(switch_hp, args)

    def _common_actions(self, switch, args):
        pass