#!/usr/bin/env python3
# coding: utf-8

'''
Created oén 23 nov. 2016

@author: FERREB
'''

import sys

from switchhandler.switch.switch_scripter import SwitchScripter


class SaveSwitchConf(SwitchScripter):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--TFTPIP', help='The TFTP IP', default='192.168.7.20')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            switch.execute(
                'save_conf_tftp',
                tftp_ip=args['tftpip'],
                folder="switch.git/{}".format(args['site']),
                add_timestamp=False)
            #switch.save_conf_TFTP(args['TFTPIP'], folder="DN", add_timestamp=False)

        switch.logout()

save_conf_TFTP = SaveSwitchConf('Save the running config', sys.argv[1:])
save_conf_TFTP.process()
