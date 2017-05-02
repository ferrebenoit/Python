# coding: utf-8
'''
Created on 23 nov. 2016

@author: FERREB
'''

import re

from pexpect.exceptions import TIMEOUT, EOF

from utils.network.net_tools import convert_to_netmask, \
    convert_to_wildcard, convert_mac_cisco
from utils.switch.switch_base import SwitchBase, ConfigMode, Exec


# from utils.switch import switchCiscoCommands
class SwitchCisco(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchCisco, self).__init__(IP, 'cisco', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([$#])'

    def getExecLevel(self):
        if self.exec == '$':
            return Exec.USER
        elif self.exec == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        if self.configMode is None:
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
        self.sendline(
            'copy tftp://{} flash:/{}'.format(localFilePath, RemoteFilePath))
        self.expectPrompt()

    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        try:
            self.sendline(
                'copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))

            # host confirmation
            self.expect('Address or name of remote host \[.*\]\?')
            self.sendline()

            # check if host is correct and filename confirmation
            match = self.expect(
                ['Destination filename \[.*\]\?', 'Invalid host address or name'])
            if(match == 1):
                print('Hote inconnu')
                return False

            self.sendline()

            # check if all good
            match = self.expect(
                ['[0-9]* bytes copied in .*\r\n', '%Error opening tftp.*\r\n'], timeout=60)

            if(match == 0):
                return True
            elif(match == 1):
                print('sauvegarde Echouee')
                print(self.connection.before)
                return False

            # Consume prompt response
            self.expectPrompt()
        except TIMEOUT:
            print("Sauvegarde echouee a cause d'un timeout")
            print(self.connection.before)
        except EOF:
            print("Sauvegarde echouee a cause d'une deconnexion")
            print(self.connection.before)
        except Exception:
            print('exception')
            # print(e)
            print(self.connection.before)
            print(self.connection.after)

    def delete_acl(self, name):
        self.sendline('no ip access-list extended {}'.format(name))
        self.expectPrompt()

    def create_ACL(self, name, acl_entries, acl_replace=None, inverse_src_and_dst=False):
        self.end()
        self.conft()

        self.delete_acl(name)

        self.ACL(name)

        for row in acl_entries:
            self.ACL_add_row(name, row, acl_replace, inverse_src_and_dst)

        self.write()

    def ACL(self, name):
        self.sendline('ip access-list extended {}'.format(name))
        self.expectPrompt()

    def ACL_add_entry(self, name, index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log, inverse_src_and_dst=False):
        # TODO: if protocol is ICMP and not inverse_src_and_dst assign echo_reply to  src_port_operator
        # if protocol is ICMP and inverse_src_and_dst assign echo to
        # dst_port_operator

        # if we ask icmp add icmp type at the end of request
        if (protocol.lower() == 'icmp'):
            if inverse_src_and_dst:
                src_port_operator = "echo"
            else:
                dst_port_operator = "echo-reply"

        if (src1.lower() != 'host'):
            src2 = convert_to_wildcard(src2)

        if (dst1.lower() != 'host'):
            dst2 = convert_to_wildcard(dst2)

        if inverse_src_and_dst:
            self.sendline('{} {} {} {} {} {} {} {} {} {} {} {}'.format(
                index, action, protocol, dst1, dst2, dst_port_operator, dst_port, src1, src2, src_port_operator, src_port, log))
        else:
            self.sendline('{} {} {} {} {} {} {} {} {} {} {} {}'.format(
                index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log))
        self.expectPrompt()

    def add_acl_to_interface(self, acl_name, interface_name, inbound=True):
        self.end()
        self.conft()

        self.sendline('interface {}'.format(interface_name))
        self.expectPrompt()

        if inbound:
            self.sendline('ip access-group {} in'.format(acl_name))
        else:
            self.sendline('ip access-group {} out'.format(acl_name))
        self.expectPrompt()

        self.write()

    def add_ospf_router(self, network, networkID):
        self.end()
        self.conft()

        self.sendline('router ospf 1')
        self.expectPrompt()

        self.sendline('network {} {} area 0'.format(
            network, convert_to_wildcard(networkID)))
        self.expectPrompt()

        self.write()

    def create_vlan(self, ID, name, IP=-1, network=-1, IP_helper=-1):
        '''If IP mask and CIDR are provided add an IP to the vlan
        '''
        self.end()
        self.conft()

        self.vlan(ID, name)

        self.exit()

        # If IP mask and CIDR are provided add an IP to the vlan
        if IP != -1 and network != -1:
            self.int_vlan(ID, name)
            self.ip_address(IP, network)

            if (IP_helper != -1):
                self.ip_helper(IP_helper)

        self.write()

    def vlan(self, ID, name=None):
        self.sendline('vlan {}'.format(ID))
        self.expectPrompt()
        if name is not None:
            self.sendline('name {}'.format(name))
            self.expectPrompt()

    def int_vlan(self, ID, name=None):
        self.sendline('interface vlan{}'.format(ID))
        self.expectPrompt()
        if name is not None:
            self.sendline('description {}'.format(name))
            self.expectPrompt()

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
        pass

    def find_port_from_mac(self, mac, ip=None):
        self.end()

        mac = convert_mac_cisco(mac)

        if ip is not None:
            self.ping(ip, 3)
            self.expectPrompt()

        self.sendline("show mac address-table | include {}".format(mac))
        self.expectPrompt()

        match = re.search(
            '^[ ]*([0-9][0-9]*)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^ ^\n]*)$', self.before(), re.MULTILINE)

        if match:
            return match.group(4)
        else:
            return ""

    def ping(self, ip, repeat=5):
        self.sendline("ping {} repeat {}".format(ip, repeat))

    def ip_address(self, IP, network):
        self.sendline(
            'ip address {} {}'.format(IP, convert_to_netmask(network)))
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
        if not self.getConfigMode() == ConfigMode.GLOBAL:
            self.sendline('end')
            self.expectPrompt()

    def write(self):
        self.end()
        self.sendline('write')
        self.expectPrompt()

    def expectPrompt(self):
        return super(SwitchCisco, self).expectPrompt()

    def login(self, login, password):
        if super(SwitchCisco, self).login(login, password):
            return True
        else:
            return False

    def logout(self):
        return super(SwitchCisco, self).logout()

    def save_conf_TFTP(self, TFTP_IP, folder=None, add_timestamp=False):
        self.end()

        result = self.downloadFileTFTP(
            TFTP_IP, 'system:running-config', self._build_tftp_filepath(folder, add_timestamp))
        if result:
            self.logger.info('Backup complete')
        else:
            self.logger.error('Backup error')
        return result
