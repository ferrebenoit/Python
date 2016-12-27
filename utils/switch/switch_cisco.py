'''
Created on 23 nov. 2016

@author: FERREB
'''

from utils.switch.switch_base import SwitchBase
from pexpect.exceptions import TIMEOUT, EOF

class SwitchCisco(SwitchBase):

    def __init__(self, params):
        super(SwitchCisco, self).__init__(params)
        
        self._PROMPT = '#'
        self.connection.PROMPT = self._PROMPT
        
        
        
    def _login(self, IP, login, password):
        return super(SwitchCisco, self)._login(IP, login, password)
        
    def _logout(self):
        return super(SwitchCisco, self)._logout()
        
    def _save_conf(self):
        try:
            self.connection.sendline('copy system:running-config tftp://172.17.6.28/{}.cnfg'.format(self.params['name']))
            
            #host confirmation
            self.connection.expect('Address or name of remote host \[.*\]\?')
            self.connection.sendline()
            
                   
            #check if host is correct and filename confirmation
            match = self.connection.expect(['Invalid host address or name', 'Destination filename \[.*\]\?'])
            if(match == 0):
                print('Hote inconnu')
                return False
            
            self.connection.sendline()
            
            # check if all good
            match = self.connection.expect(['[0-9]* bytes copied in .*\r\n', '%Error opening tftp.*\r\n'], timeout=60 )
            if(match == 0):
                return True
            elif(match == 1):
                print('sauvegarde Echouee')
                print(self.connection.before)
                return False
            
        except TIMEOUT :
            print("Sauvegarde echouee a cause d'un timeout")
            print(self.connection.before)
        except EOF :
            print("Sauvegarde echouee a cause d'une deconnexion")
            print(self.connection.before)
        except Exception as e:
            print('exception')
            #print(e)
            print(self.connection.before)
            print(self.connection.after)
        