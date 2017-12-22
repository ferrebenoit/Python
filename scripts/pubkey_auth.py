#!/usr/bin/env python3
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--keyhash', help='The key hash')
        self._arg_parser.add_argument('--key', help='The key')
        self._arg_parser.add_argument('--keypath', help='The key')
        self._arg_parser.add_argument('--keyuser', help='the username for key auth')
        self._arg_parser.add_argument('--keycomment', help='the username for key auth')
        self._arg_parser.add_argument('--TFTPIP', help='The TFTP IP', default='192.168.7.20')

        self._add_mandatory_arg('keyhash', 'key', 'keypath', 'keyuser', 'keycomment')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            if switch.auth_PublicKey(args['keyuser'], args['keyhash'], args['keycomment'], ''):
                print('auth configured')
            else:
                print('Error auth not configured')

        switch.logout()

pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
