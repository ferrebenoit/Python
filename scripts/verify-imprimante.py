#!/usr/bin/env python3
import os
import re
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class VerifyImprimante(SwitchScripter):

    def _define_args(self):
        super()._define_args()

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            switch.sendline('terminal length 0')
            switch.expectPrompt()

            switch.execute('conft')

            switch.sendline('ip access-list resequence ACL-Imprimante-In 10 10')
            switch.expectPrompt()
            switch.sendline('ip access-list resequence ACL-Imprimante-Out 10 10')
            switch.expectPrompt()

            switch.execute('write')

            switch.execute('end')

            switch.sendline('sh access-lists ACL-Imprimante-In')
            switch.expectPrompt()

            if re.search('550 deny ip any any log', switch.before(), re.MULTILINE):
                switch.logInfo('ACL ACL-Imprimante-In OK')
            else:
                switch.log_error('ACL ACL-Imprimante-In NOK')

            switch.sendline('sh access-lists ACL-Imprimante-Out')
            switch.expectPrompt()

            if re.search('550 deny ip any any log', switch.before(), re.MULTILINE):
                switch.logInfo('ACL ACL-Imprimante-Out OK')
            else:
                switch.log_error('ACL ACL-Imprimante-Out NOK')

        switch.logout()

pubkey_auth = VerifyImprimante('Configure ssh public key authentication', sys.argv[1:])
pubkey_auth.process()
