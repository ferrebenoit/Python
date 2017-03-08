from utils.switch.switch_base import SwitchBase, ConfigMode, Exec
from pexpect.exceptions import TIMEOUT, EOF
import datetime

class SwitchAllied(SwitchBase):

    def __init__(self, IP, dryrun=False):
        super(SwitchAllied, self).__init__(IP, dryrun)
        
        #prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>#])'
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
        self.end()
        self.enable()
        self.conft()
        
        self.sendline('crypto key pubkey-chain userkey {}'.format(username))
        self.connection.expect('Tself.sendnish:')
        self.sendline(key)
        self.sendcontrol('d')
        
        self.expectPrompt()
        
        self.write()
        return True
        
    def uploadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        self.sendline('copy tftp://{} flash:/{}'.format(TFTP_IP, localFilePath, RemoteFilePath))
        self.expectPrompt()
            
    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        # copy running-config tftp://192.168.0.1/
        try:
            self.sendline('copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))
            
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
    
    def add_ospf_router(self, network, ospfwildcard, CIDR):
        self.end()
        self.enable()
        self.conft()
        
        self.sendline('router ospf 1')
        self.expectPrompt()

        self.sendline('network {}/{} area 0'.format(network, CIDR))
        self.expectPrompt()
        
        self.write()
    
    def create_vlan(self, ID, name, IP=-1, mask=-1, CIDR=-1, IP_helper=-1):
        self.end()
        self.enable()
        self.conft()
        
        self.vlan(ID, name)
        
        self.exit()
        
        # If IP mask and CIDR are provided add an IP to the vlan 
        if IP != -1 and CIDR != -1:
            self.int_vlan(ID, name)
            self.ip_address(IP, mask, CIDR)
        
            if (IP_helper != -1):
                self.ip_helper(IP_helper)
        
        self.write()
    
    def vlan(self, ID, name=None):
        self.connection.sendline('vlan database')
        self.expectPrompt()
        
        if name != None:
            self.sendline('vlan {} name {}'.format(ID, name))
            self.expectPrompt()
        

    def int_vlan(self, ID, name=None):
        self.sendline('interface vlan{}'.format(ID))
        self.expectPrompt()
        
        if name != None:
            self.sendline('description {}'.format(name))
            self.expectPrompt()


    def ip_address(self, IP, mask, CIDR):
        self.sendline('ip address {}/{}'.format(IP, CIDR))
        self.expectPrompt()

    def ip_helper(self, IP):
        self.sendline('ip dhcp-relay server-address {}'.format(IP))
        self.expectPrompt()
        self.sendline('ip helper-address {}'.format(IP))
        self.expectPrompt()
                    
    def enable(self):
        self.sendline('enable')
        self.expectPrompt()
    
    def conft(self):
        self.sendline('configure terminal')
        self.expectPrompt()
    
    def exit(self):
        self.sendline('exit')
        self.expectPrompt()
            
    def end(self):
        self.sendline('end')
        self.expectPrompt()

    def write(self):
        self.sendline('write')
        self.expectPrompt()

    def save_conf_TFTP(self, TFTP_IP):
        self.end()
        self.enable()
        result = self.downloadFileTFTP(TFTP_IP, 'running-config', '{}_{:%Y%m%d-%H%M%S}.cnfg'.format(self.hostname, datetime.datetime.today()))
        
        if result :
            self.logger.info('Backup complete')
        else:
            self.error('Backup error')
        return result 
    
    def expectPrompt(self):
        return super(SwitchAllied, self).expectPrompt()
             
    def login(self, login, password):

        return super(SwitchAllied, self).login(login, password)
            
    def logout(self):
        return super(SwitchAllied, self).logout()
        
        
        