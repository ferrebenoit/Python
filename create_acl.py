import sys

from utils.switch.switch_scripter import SwitchScripter
from _csv import reader
import csv
import os



class CreateAcl(SwitchScripter):
    
    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--Name', help='The acl Name')
        self._arg_parser.add_argument('--csvaclentries', help='The csv file that holds the contents')
        
        
        self._add_mandatory_arg('Name', 'csvaclentries')

    def _common_actions(self, switch, args):
        if not os.path.isfile(args['csvaclentries']):
            print('fichier de l acl non trouve')
            exit
        
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            with open(args['csvaclentries']) as csv_file:
                reader = csv.DictReader(csv_file)
                switch.create_ACL(args['Name'], reader)
            
            switch.logout()

create_acl = CreateAcl('Add access list', sys.argv[1:])
create_acl.process()