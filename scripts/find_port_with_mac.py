#!/usr/bin/env python3
import csv
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--findip', help='The IP to ping')
        self._arg_parser.add_argument('--findmac', help='The mac to find')
        self._arg_parser.add_argument('--csvmac', help='CSV file that contain mac and ip')

        #self._add_mandatory_arg('findip', 'findmac')

    def _common_actions(self, switch, args):

        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            if 'csvmac' in args:
                with open(args['csvmac']) as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=';')

                    for row in reader:
                        print('{};{}'.format(
                            row['ipaddress'],
                            switch.execute('port_from_mac',
                                           mac=row['mac'],
                                           ip=row['ipaddress'])
                        ))
            elif ('findip' in args) and ('findmac' in args):
                switch.log_error('{};{}'.format(
                    args['findip'],
                    switch.execute('port_from_mac',
                                   mac=args['findmac'],
                                   ip=args['findip'])
                ))
            else:
                switch.log_error("Mauvaise combinaison d'option")

            switch.logout()


pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
