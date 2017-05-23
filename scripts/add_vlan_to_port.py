#!/usr/bin/env python3
import csv
import sys

from switchhandler.switch.switch_scripter import SwitchScripter


class AddVlanToPort(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--port', help='The Port to configure')
        self._arg_parser.add_argument('--vlan', help='The vlan to add')
        self._arg_parser.add_argument('--description', help='set the port description')
        self._arg_parser.add_argument('--portcsv', help='CSV file that contains port list')

        #self._add_mandatory_arg('findip', 'findmac')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:

            with open(args['portcsv']) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')

                switch.execute('enable')
                switch.execute('conft')
                for row in reader:
                    switch.execute('add_tagged_vlan_to_port',
                                   args['vlan'],
                                   row['port'],
                                   args['description']
                                   )

                switch.execute('write')

        switch.logout()

pubkey_auth = AddVlanToPort('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
