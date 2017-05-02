#!/usr/bin/env python3
import os
import sys

from utils.switch.switch_scripter import SwitchScripter


class PubkeyAuth(SwitchScripter):

    def _define_args(self):
        super()._define_args()

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            # switch.conft()
            switch.sendline('sh run int vlan 262')
            switch.expectPrompt()
            print(switch.before())

            switch.sendline('sh run int vlan 252')
            switch.expectPrompt()
            print(switch.before())

        switch.logout()

pubkey_auth = PubkeyAuth('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
