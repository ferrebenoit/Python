import sys

from utils.switch.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):
    
    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--VlanID', help='The Vlan ID')
        self._arg_parser.add_argument('--Name', help='The Vlan Name')
        self._arg_parser.add_argument('--VlanIP', help='The interface vlan IP',  default=-1)
        self._arg_parser.add_argument('--VlanMask', help='The interface vlan Mask',  default=-1)
        self._arg_parser.add_argument('--VlanCIDR', help='The interface vlan CIDR',  default=-1)
        self._arg_parser.add_argument('--IPHelper', help='DHCP IP helper',  default=-1)
        self._arg_parser.add_argument('--ospfnetwork', help='if ospf must be configured',  default=-1)
        self._arg_parser.add_argument('--ospfwildcard', help='if ospf must be configured',  default=-1)
        
        self._add_mandatory_arg('VlanID', 'Name')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            switch.create_vlan(args['VlanID'], args['Name'], args['VlanIP'], args['VlanMask'], args['VlanCIDR'], args['IPHelper'])
            
            if args['ospfnetwork'] != -1:
                switch.add_ospf_router(args['ospfnetwork'], args['ospfwildcard'], args['VlanCIDR'])
            
        switch.logout()

pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()