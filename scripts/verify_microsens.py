#!/usr/bin/env python3
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class VerifyImprimante(SwitchScripter):

    def _define_args(self):
        super()._define_args()

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:

            print(switch.before())
            switch.sendline('show cdp config')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show config')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show port power')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show prio')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show vlan')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show rstp config')
            switch.expectPrompt()
            print(switch.before())
            switch.sendline('show rstp port config')
            switch.expectPrompt()
            print(switch.before())

        switch.logout()

pubkey_auth = VerifyImprimante('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
