'''
Created on 23 nov. 2016

@author: FERREB
'''
import logging.handlers
import re
import sys
import traceback

from switchhandler.script.arg_from_csv import ArgFromCSV
from switchhandler.utils.decorator.class_register import registered_class_scan,\
    get_registered_classes
from switchhandler.device import CATEGORY_DEVICE_EXPECT, CATEGORY_DEVICE_SNMP


@registered_class_scan(BasePackage='switchhandler.device.protocol.expect', MaxDepth=4)
class SwitchScripter(ArgFromCSV):
    "Class That add common options for switch handling"

    def __init__(self, description, args):
        ArgFromCSV.__init__(self, description, args, self._script_worker)

        self._logging_config(self._arguments['loglevel'].upper(
        ), self._arguments['screenlog'] == 'yes', self._arguments['filelog'])
        self._sharedResult = {}

    def _logging_config(self, loglevel, screenlog, fileLog):
        logger = logging.getLogger('switch')
        logger.setLevel(loglevel)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if screenlog:
            screenHandler = logging.StreamHandler()
            screenHandler.setFormatter(formatter)
            logger.addHandler(screenHandler)

        if fileLog != 'none':
            fileHandler = logging.handlers.TimedRotatingFileHandler(
                fileLog, when='midnight')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--loglevel', help='Loglevel', choices=[
                                      'debug', 'info', 'warning', 'error', 'critical'], default='info')
        self._arg_parser.add_argument(
            '--screenlog', help='Print log on screen', choices=['yes', 'no'], default='yes')
        self._arg_parser.add_argument(
            '--filelog', help='Save la on file', default='none')

        self._arg_parser.add_argument(
            '--dryrun', help='No Action taken! Only print what would have been executed.', choices=['yes', 'no'], default='no')

        self._arg_parser.add_argument('--ip', help='Switch IP address')
        self._arg_parser.add_argument('--login', help='login')
        self._arg_parser.add_argument(
            '--password', help='For authenticating with pivate key enter a fake password like "keyauth"')
        self._arg_parser.add_argument('--vendor', '--type', help='the vendor')
        self._arg_parser.add_argument(
            '--protocol', help='query protocol default : expect', choices=['expect', 'snmp'], default='expect')
        self._arg_parser.add_argument('--switchname', help='the switch name')
        self._arg_parser.add_argument('--site', help='The switch site')
        self._arg_parser.add_argument('--siteid', help='The switch siteid')
        self._arg_parser.add_argument(
            '--auth', help='The authentication method', choices=['password', 'key'], default='password')

        self._add_mandatory_arg('IP', 'vendor', 'login', 'password')

    def process(self):

        if self._arguments['auth'] == 'key':
            self._arguments['password'] = None

        return super().process()

    def _script_worker(self, args):
        try:
            if(re.compile('expect', flags=re.IGNORECASE).search(args['protocol'])):
                for device_key, device_class in get_registered_classes(CATEGORY_DEVICE_EXPECT):
                    if(re.compile(device_key, flags=re.IGNORECASE).search(args['vendor'])):
                        self._common_actions(device_class(args['ip'], args.get(
                            'site', None), args['dryrun'] == 'yes'), args)
            elif(re.compile('expect', flags=re.IGNORECASE).search(args['protocol'])):
                for device_key, device_class in get_registered_classes(CATEGORY_DEVICE_SNMP):
                    if(re.compile(device_key, flags=re.IGNORECASE).search(args['vendor'])):
                        self._common_actions(device_class(args['ip'], args.get(
                            'site', None), args['dryrun'] == 'yes'), args)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # exc_type below is ignored on 3.5 and later
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

    def _script_content_cisco(self, switch_cisco, args):
        self._common_actions(switch_cisco, args)

    def _script_content_nexus(self, switch_nexus, args):
        self._common_actions(switch_nexus, args)

    def _script_content_hp(self, switch_hp, args):
        self._common_actions(switch_hp, args)

    def _script_content_allied(self, switch_allied, args):
        self._common_actions(switch_allied, args)

    def _script_content_microsens(self, switch_microsens, args):
        self._common_actions(switch_microsens, args)

    def _script_content_snmp_cisco(self, switch_snmp_cisco, args):
        self._common_actions(switch_snmp_cisco, args)

    def _common_actions(self, switch, args):
        pass
