'''
Created on 23 nov. 2016

@author: FERREB
'''
import sys

from utils.switch.switch_scripter import SwitchScripter
from utils.switch.switch_cisco import SwitchCisco



class SaveSwitchConf(SwitchScripter):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        
    def _script_content_cisco(self, args):
        cisco = SwitchCisco(args)
        if not cisco.login():
            print('impossible de se connecter')
        else:
            if cisco.save_conf():
                print('sauvegarde effectuee')
            else:
                print('sauvegarde erreur')
            
        cisco.logout()
        
save_conf = SaveSwitchConf('desc', sys.argv[1:])
save_conf.process()