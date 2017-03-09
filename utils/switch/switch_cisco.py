'''
Created on 23 nov. 2016

@author: FERREB
'''

from utils.switch.switch_base import SwitchBase, ConfigMode, Exec
from pexpect.exceptions import TIMEOUT, EOF
import datetime

class SwitchCisco(SwitchBase):

    def __init__(self, IP, dryrun=False):
        super(SwitchCisco, self).__init__(IP, dryrun)
        
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
        self.end()
        self.conft()
        
        self.sendline('ip ssh pubkey-chain')
        self.expectPrompt()

        self.sendline('username {}'.format(username))
        self.expectPrompt()
        
        self.sendline('key-hash ssh-rsa {} {}'.format(key, comment))
        self.expectPrompt()
        
        self.write()
        return True
        
    def uploadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        self.sendline('copy tftp://{} flash:/{}'.format(localFilePath, RemoteFilePath))
        self.expectPrompt()

    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        try:
            self.sendline('copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))
            
            #host confirmation
            self.expect('Address or name of remote host \[.*\]\?')
            self.sendline()
            
                   
            #check if host is correct and filename confirmation
            match = self.expect(['Destination filename \[.*\]\?', 'Invalid host address or name'])
            if(match == 1):
                print('Hote inconnu')
                return False
            
            self.sendline()
            
            # check if all good
            match = self.expect(['[0-9]* bytes copied in .*\r\n', '%Error opening tftp.*\r\n'], timeout=60 )
            
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

    def create_ACL(self, name, acl_entries, acl_replace=None):
        self.end()
        self.conft()

        self.ACL(name)

        for row in acl_entries:
            self.ACL_add_row(name, row, acl_replace)

        self.write()

    def ACL(self, name):
        self.sendline('ip access-list extended {}'.format(name))
        self.expectPrompt()

    def ACL_add_row(self, name, row, acl_replace=None):
        if acl_replace != None:
            for k in row.keys():
                if(k in acl_replace): 
                    row[k] = row[k].format(**acl_replace[k]) 
        
        self.ACL_add_entry(name, row['index'], row['action'], row['protocol'], row['src1'], row['src2'], row['src_port_operator'], row['src_port'], row['dst1'], row['dst2'], row['dst_port_operator'], row['dst_port'], row['log'])

    def ACL_add_entry(self, name, index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log):
        self.sendline('{} {} {} {} {} {} {} {} {} {} {} {}'.format(index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log))
        self.expectPrompt()

    def add_ospf_router(self, network, ospfwildcard, CIDR):
        self.end()
        self.conft()
        
        self.sendline('router ospf 1')
        self.expectPrompt()
        
        self.sendline('network {} {} area 0'.format(network, ospfwildcard))
        self.expectPrompt()
        
        self.write()        
     
    def create_vlan(self, ID, name, IP=-1, mask=-1, CIDR=-1, IP_helper=-1):
        '''        
            If IP mask and CIDR are provided add an IP to the vlan 
        '''
        self.end()
        self.conft()
        
        self.vlan(ID, name)
        
        self.exit()

        # If IP mask and CIDR are provided add an IP to the vlan 
        if IP != -1 and mask != -1:
            self.int_vlan(ID, name)
            self.ip_address(IP, mask, CIDR)
        
            if (IP_helper != -1):
                self.ip_helper(IP_helper)
        
        self.write()
    
    def vlan(self, ID, name=None):
        self.sendline('vlan {}'.format(ID))
        self.expectPrompt()
        if name != None:
            self.sendline('name {}'.format(name))
            self.expectPrompt()

    def int_vlan(self, ID, name=None):
        self.sendline('interface vlan{}'.format(ID))
        self.expectPrompt()
        if name != None:
            self.sendline('description {}'.format(name))
            self.expectPrompt()

    def ip_address(self, IP, mask, CIDR):
        self.sendline('ip address {} {}'.format(IP, mask))
        self.expectPrompt()

    def ip_helper(self, IP):
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
        self.end()
        self.sendline('write')
        self.expectPrompt()

    def expectPrompt(self):
        return super(SwitchCisco, self).expectPrompt()
    
    def login(self, login, password):
        return super(SwitchCisco, self).login(login, password)
        
    def logout(self):
        return super(SwitchCisco, self).logout()
        
    def save_conf_TFTP(self, TFTP_IP):
        self.end()
        result = self.downloadFileTFTP(TFTP_IP, 'system:running-config', '{}_{:%Y%m%d-%H%M%S}.cnfg'.format(self.hostname, datetime.datetime.today()))
        if result :
            self.logger.info('Backup complete')
        else:
            self.error('Backup error')
        return result 

        