'''
Created on 23 nov. 2016

@author: FERREB
'''
from utils.arg_from_csv import ArgFromCSV


class SwitchScripter(ArgFromCSV):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--IP', help='AP IP address')
        self._arg_parser.add_argument('--login', help='login')
        self._arg_parser.add_argument('--password', help='password')
        self._arg_parser.add_argument('--vendor', help='the vendor')
                
        self._add_needed_arg('IP', 'vendor', 'login', 'password')
        
    def _script_content(self, args):
        if(args['vendor'] == 'cisco'):
            self._script_content_cisco(args)
        elif(args['vendor'] == 'hp'):
            self._script_content_hp(args)
        elif(args['vendor'] == 'allied'):
            self._script_content_allied(args)

    def _script_content_cisco(self, args):
        pass
        
    def _script_content_hp(self, args):
        pass
    
    def _script_content_allied(self, args):
        pass