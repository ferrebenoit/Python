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
        self._arg_parser.add_argument('--keycomment', help='the comment for the key')
        self._arg_parser.add_argument('--tftpip', help='The TFTP IP', default='192.168.7.20')

        self._arg_parser.add_argument('--createuser', help='Create the username before adding the key', choices=['yes', 'no'], default='no')
        self._arg_parser.add_argument('--userpassword', help='Password for the newly created user')
        self._arg_parser.add_argument('--userlevel', help='Choose if user has admin or read rights', choices=['admin', 'read'])

        self._add_mandatory_arg('keyhash', 'key', 'keypath', 'keyuser', 'keycomment')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:

            if args['createuser'] == 'yes':
                if args['userlevel'] == 'read':
                    switch.execute('create_read_username',
                                   username=args['keyuser'],
                                   userpassword=args['userpassword'])
                else:
                    switch.execute('create_admin_username',
                                   username=args['username'],
                                   userpassword=args['userpassword'])

            if switch.execute('auth_public_key',
                              key=args['key'],
                              keyuser=args['keyuser'],
                              keyhash=args['keyhash'],
                              keypath=args['keypath'],
                              keycomment=args['keycomment'],
                              tftpip=args['tftpip']):
                print('auth configured')
            else:
                print('Error auth not configured')

        switch.logout()


pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
