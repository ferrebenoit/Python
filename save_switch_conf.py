'''
Created on 23 nov. 2016

@author: FERREB
'''
import sys

from utils.switch.switch_scripter import SwitchScripter
from utils.switch.switch_cisco import SwitchCisco
from utils.switch.switch_allied import SwitchAllied
from utils.switch.switch_HP import SwitchHP



class SaveSwitchConf(SwitchScripter):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        
    def _script_content_cisco(self, args):
        cisco = SwitchCisco(args['IP'])
        
        if not cisco.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            #if cisco.save_conf_TFTP('192.168.7.20'):
            if cisco.save_conf_TFTP('172.17.6.28'):
                print('sauvegarde effectuee')
            else:
                print('sauvegarde erreur')
            
        cisco.logout()
    
    def _script_content_allied(self, args):
        allied = SwitchAllied(args['IP'])
        
               
        if not allied.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            allied.enable()
            if allied.save_conf_TFTP('172.17.6.28'):
                print('sauvegarde effectuee')
            else:
                print('sauvegarde erreur')
            
        allied.logout()
    
    def _script_content_hp(self, args):
        HP = SwitchHP(args['IP'])
        
               
        if not HP.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            if HP.save_conf_TFTP('172.17.6.28'):
                print('sauvegarde effectuee')
            else:
                print('sauvegarde erreur')
            
        HP.logout()
        
        
        
save_conf_TFTP = SaveSwitchConf('desc', sys.argv[1:])
save_conf_TFTP.process()