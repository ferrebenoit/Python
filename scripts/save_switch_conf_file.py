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
        self._arg_parser.add_argument('--path', help='the save path')

        self._add_mandatory_arg('path')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            switch.log_error('BACKUP FAILED')
            print('impossible de se connecter')
        else:
            switch.execute(
                'save_conf_file',
                folder="{}/{}".format(args['path'], args['site']),
                add_timestamp=False)
            #switch.save_conf_TFTP(args['TFTPIP'], folder="DN", add_timestamp=False)
            switch.logout()

save_conf_File = SaveSwitchConf('Save the running config', sys.argv[1:])
save_conf_File.process()
