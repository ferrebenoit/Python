#!/usr/bin/env python3
import sys

from switchhandler.network.net_tools import convert_to_wildcard
from switchhandler.switch.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--vlanname', help='The Vlan Name')
        self._arg_parser.add_argument('--vlan1octet', help='The Vlan first ID', default=10)
        self._arg_parser.add_argument('--vlanid', help='The Vlan ID')
        self._arg_parser.add_argument('--siteid', help='The Site ID')
        self._arg_parser.add_argument('--vlancidr', help='The interface vlan CIDR', default=None)
        self._arg_parser.add_argument('--iphelper', help='DHCP IP helper', default=None)
        self._arg_parser.add_argument('--ospfnetwork', help='if ospf must be configured')


#        self._arg_parser.add_argument('--VlanIP', help='The interface vlan IP',  default=-1)
#        self._arg_parser.add_argument('--VlanMask', help='The interface vlan Mask',  default=-1)
#        self._arg_parser.add_argument('--VlanCIDR', help='The interface vlan CIDR',  default=-1)
#        self._arg_parser.add_argument('--ospfwildcard', help='if ospf must be configured',  default=-1)

        self._add_mandatory_arg('siteid', 'vlanid', 'vlanname')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            switch.execute('create_vlan',
                           id=args['vlanid'],
                           name=args['vlanname'],
                           ip='{}.{}.{}.1'.format(args['vlan1octet'],
                                                  args['vlanid'],
                                                  args['siteid']
                                                  ),
                           network_id=args['vlancidr'],
                           ip_helper=args['iphelper']
                           )

            if (args['ospfnetwork'] == 'yes') or (args['ospfnetwork'] == 'ospf') or (args['ospfnetwork'] == 'central'):
                switch.execute('add_ospf_router',
                               network='{}.{}.{}.0'.format(args['vlan1octet'], args['vlanid'], args['siteid']),
                               network_id=args['vlancidr']
                               )

        switch.logout()

pubkey_auth = PubkeyAuth('Create a vlan with ip address', sys.argv[1:])
pubkey_auth.process()
