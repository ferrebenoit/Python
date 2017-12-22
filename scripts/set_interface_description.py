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
        result_dict = {}
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:

            with open(args['csvmac']) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')

                for row in reader:
                    port = switch.execute('port_from_mac',
                                          mac=row['mac'],
                                          ip=row['ipaddress'])
                    print('{};{}'.format(
                        row['ipaddress'], port
                    ))

                    # tester si le port n'est pas un lien vers un autre switch
                    # if not switch.execute('port_is_trunk', port) :

                    if port not in result_dict:
                        result_dict[port] = [row['ipaddress']]
                    else:
                        result_dict[port].append(row['ipaddress'])

                print(result_dict)

        switch.execute('enable')
        switch.execute('conft')
        for k, v in result_dict.items():
            switch.execute('int',
                           interface=k,
                           description="Microsens {{'ms':{}}}".format(v)
                           )
            print('int {}'.format(k))
            print("    description {{'ms':{}}}".format(v))

        switch.logout()

pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
