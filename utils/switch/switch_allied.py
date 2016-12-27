'''
Created on 27 déc. 2016

@author: ferreb
'''
from utils.switch.switch_base import SwitchBase
from pexpect.exceptions import TIMEOUT

class SwitchAllied(SwitchBase):

    def __init__(self, params):
        super(SwitchAllied, self).__init__(params)
        
        self._PROMPT = '#'
        self.connection.PROMPT = self._PROMPT
    
        
    def _login(self, login, password):
        return super(SwitchAllied, self)._login()
        
        
    def _logout(self):
        return super(SwitchAllied, self)._logout()
        
    def _save_conf(self):
        
        try:
            pass
        except TIMEOUT :
            print("Sauvegarde echouee a cause d'un timeout")
            print(self.connection.before)
        except Exception as e:
            print('exception')
            #print(e)
            print(self.connection.before)
            print(self.connection.after)