'''
Created on 23 nov. 2016

@author: FERREB
'''

from utils.switch.switch_base import SwitchBase, ConfigMode, Exec
from pexpect.exceptions import TIMEOUT, EOF
import datetime

class SwitchCisco(SwitchBase):

    def __init__(self, IP):
        super(SwitchCisco, self).__init__(IP)
        
        #prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([$#])'
        
        self.connection.PROMPT = self._PROMPT
        
    def getExecLevel(self):
        if self.exec == '$':
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
        elif self.configMode == 'config-vlan':
            return ConfigMode.VLAN 
        elif self.configMode == 'conf-ssh-pubkey':
            return ConfigMode.PUBKEY
        elif self.configMode == 'conf-ssh-pubkey-user':
            return ConfigMode.PUBKEY_USER
    
    
    def auth_PublicKey(self, username, key, comment, TFTP_IP=''):
        print('ip ssh pubkey-chain')
        self.connection.sendline('ip ssh pubkey-chain')
        self.expectPrompt()
        print('username {}'.format(username))
        self.connection.sendline('username {}'.format(username))
        self.expectPrompt()
        print('key-hash ssh-rsa {} {}'.format(key, comment))
        self.connection.sendline('key-hash ssh-rsa {} {}'.format(key, comment))
        self.expectPrompt()
        return True
        
    def uploadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        self.connection.sendline('copy tftp://{} flash:/{}'.format(localFilePath, RemoteFilePath))
        self.expectPrompt()

    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        try:
            self.connection.sendline('copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))
            
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
            
            # Consume prompt response
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

    
    def write(self):
        self.connection.sendline('write')
        self.expectPrompt()

    def expectPrompt(self):
        return super(SwitchCisco, self).expectPrompt()
    
    def login(self, login, password):
        return super(SwitchCisco, self).login(login, password)
        
    def logout(self):
        return super(SwitchCisco, self).logout()
        
    def save_conf_TFTP(self, TFTP_IP):
        return self.downloadFileTFTP(TFTP_IP, 'system:running-config', '{}_{:%Y%m%d-%H%M%S}.cnfg'.format(self.hostname, datetime.datetime.today()))

        