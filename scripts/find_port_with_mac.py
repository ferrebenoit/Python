#!/usr/bin/env python3
from _sqlite3 import Row
import csv
import os
import sys

from switchhandler.switch.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--findip', help='The IP to find')
        self._arg_parser.add_argument('--findmac', help='The mac to find')
        self._arg_parser.add_argument('--csvmac', help='CSV file that contain mac and ip')

        #self._add_mandatory_arg('findip', 'findmac')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:

            with open(args['csvmac']) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')

                for row in reader:
                    print(row['IPAddress'], ';', switch.find_port_from_mac(row['ClientId'], row['IPAddress']))

        switch.logout()

pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
