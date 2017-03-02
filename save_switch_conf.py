'''
Created on 23 nov. 2016

@author: FERREB
'''
import sys

from utils.switch.switch_scripter import SwitchScripter


class SaveSwitchConf(SwitchScripter):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--TFTPIP', help='The TFTP IP', default='192.168.7.20')
        
    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            if switch.save_conf_TFTP(args['TFTPIP']):
            #if cisco.save_conf_TFTP('172.17.6.28'):
                print('sauvegarde effectuee')
            else:
                print('sauvegarde erreur')
        switch.logout()

save_conf_TFTP = SaveSwitchConf('Save the running config', sys.argv[1:])
save_conf_TFTP.process()