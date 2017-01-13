from utils.switch.switch_base import SwitchBase, ConfigMode, Exec
from pexpect.exceptions import TIMEOUT, EOF
import datetime

class SwitchAllied(SwitchBase):

    def __init__(self, IP):
        super(SwitchAllied, self).__init__(IP)
        
        #prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>,#])'
        self.connection.PROMPT = self._PROMPT

    def getExecLevel(self):
        if self.exec == '>':
            return Exec.USER
        elif self.exec == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        if self.configMode == '':
            return ConfigMode.GLOBAL
        elif self.configMode == 'config':
            return ConfigMode.TERMINAL   
        elif self.configMode == 'config-if':
            return ConfigMode.INTERFACE
        elif self.configMode == 'config-vlan': #vlan database
            return ConfigMode.VLAN 
    
    def auth_PublicKey(self, username, key, comment, TFTP_IP=''):
        self.connection.sendline('crypto key pubkey-chain userkey {}'.format(username))
        self.connection.expect('Type CNTL/D to finish:')
        self.connection.send('key')
        self.connection.sendcontrol('D')
        self.expectPrompt()
        
        
    def uploadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        self.connection.sendline('copy tftp://{} flash:/{}'.format(TFTP_IP, localFilePath, RemoteFilePath))
        self.expectPrompt()
            
    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        # copy running-config tftp://192.168.0.1/
        try:
            self.connection.sendline('copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))
            
            match = self.connection.expect(['Successful operation', '% Network is unreachable', '% Invalid tftp destination'])
            if match > 0 :
                print('Sauvegarde echouee ')
                return False
            elif match == 0: 
                return True
            
            
            self.expectPrompt()
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
            
    def enable(self):
        self.connection.sendline('enable')
        self.expectPrompt()
    
    def conft(self):
        self.connection.sendline('configure terminal')
        self.expectPrompt()
    
    def exit(self):
        self.connection.sendline('exit')
        self.expectPrompt()
            
    def end(self):
        self.connection.sendline('end')
        self.expectPrompt()

    def save_conf_TFTP(self, TFTP_IP):
        return self.downloadFileTFTP(TFTP_IP, 'running-config', '{}_{:%Y%m%d-%H%M%S}.cnfg'.format(self.hostname, datetime.datetime.today()))
    
    def expectPrompt(self):
        return super(SwitchAllied, self).expectPrompt()
             
    def login(self, login, password):
#        try:
#            self.connection.expect('login as:')
#            self.connection.sendline(login)
#
#            self.connection.expect('Password:')
#            self.connection.sendline(password)
#            
#            # check errors before
#            self.expectPrompt()
#            
#            return True
#        except:
#            print('login failed')
#            print(self.connection.before)
#            print(self.connection.after)
#            return False
        return super(SwitchAllied, self).login(login, password)
            
    def logout(self):
        return super(SwitchAllied, self).logout()
        
        
        