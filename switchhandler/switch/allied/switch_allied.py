import re

from pexpect.exceptions import TIMEOUT, EOF

from switchhandler.network.net_tools import convert_to_cidr, convert_mac_allied
from switchhandler.switch.switch_base import SwitchBase, ConfigMode, Exec
from switchhandler.switch.allied import switchAlliedCommands


class SwitchAllied(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchAllied, self).__init__(IP, 'allied', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

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
        elif self.configMode == 'config-vlan':  # vlan database
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
        self.sendline('copy tftp://{} flash:/{}'.format(
            TFTP_IP,
            localFilePath,
            RemoteFilePath
        ))
        self.expectPrompt()

    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        # copy running-config tftp://192.168.0.1/
        try:
            self.sendline('copy {} tftp://{}/{}'.format(localFilePath, TFTP_IP, RemoteFilePath))

            match = self.connection.expect(['Successful operation', '% Network is unreachable', '% Invalid tftp destination'])
            if match > 0:
                print('Sauvegarde echouee ')
                return False
            elif match == 0:
                return True

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

    def create_ACL(self, name, acl_entries, acl_replace=None, inverse_src_and_dst=False):
        self.end()
        self.enable()
        self.conft()

        self.ACL(name)

        for row in acl_entries:
            self.ACL_add_row(name, row, acl_replace, inverse_src_and_dst)

        self.write()

    def delete_acl(self, name):
        pass

    def ACL(self, name):
        self.sendline('access-list extended {}'.format(name))
        self.expectPrompt()

    def ACL_add_entry(self, name, index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log, inverse_src_and_dst=False):
        # TODO: if protocol is ICMP and not inverse_src_and_dst assign icmp-type 0 to  src_port_operator
        # if protocol is ICMP and inverse_src_and_dst assign icmp-type 8 to  dst_port_operator

        # if we ask icmp add icmp type at the end of request
        if (protocol.lower() == 'icmp'):
            if inverse_src_and_dst:
                src_port_operator = "8"
            else:
                dst_port_operator = "0"

        if (src1.lower() != 'host'):
            src2 = convert_to_cidr(src2)

        if (dst1.lower() != 'host'):
            dst2 = convert_to_cidr(dst2)

        if (src1.lower() == 'host'):
            src1 = src2
            src2 = '0'

        if (dst1.lower() == 'host'):
            dst1 = dst2
            dst2 = '0'

        if src2 != '':
            src2 = '/{}'.format(src2)

        if dst2 != '':
            dst2 = '/{}'.format(dst2)

        if inverse_src_and_dst:
            self.sendline('{} {} {}{} {} {} {}{} {} {} {}'.format(action, protocol, dst1, dst2, dst_port_operator, dst_port, src1, src2, src_port_operator, src_port, log))
        else:
            self.sendline('{} {} {}{} {} {} {}{} {} {} {}'.format(action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log))
        self.expectPrompt()

    def add_acl_to_interface(self, acl_name, interface_name, inbound=True):
        pass

    def add_ospf_router(self, network, networkID):
        self.end()
        self.enable()
        self.conft()

        self.sendline('router ospf 1')
        self.expectPrompt()

        self.sendline('network {}/{} area 0'.format(network, convert_to_cidr(networkID)))
        self.expectPrompt()

        self.write()

    def create_vlan(self, ID, name, IP=-1, network=-1, IP_helper=-1):
        self.end()
        self.enable()
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
        self.sendline('vlan database')
        self.expectPrompt()

        if name is not None:
            self.sendline('vlan {} name {}'.format(ID, name))
            self.expectPrompt()

    def int_vlan(self, ID, name=None):
        self.sendline('interface vlan{}'.format(ID))
        self.expectPrompt()

        if name is not None:
            self.sendline('description {}'.format(name))
            self.expectPrompt()

    def ip_address(self, IP, network):
        self.sendline('ip address {}/{}'.format(IP, convert_to_cidr(network)))
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

    def save_conf_TFTP(self, TFTP_IP, folder=None, add_timestamp=False):
        self.end()
        self.enable()
        result = self.downloadFileTFTP(
            TFTP_IP,
            'running-config',
            self._build_tftp_filepath(folder, add_timestamp))

        if result:
            self.logger.info('Backup complete')
        else:
            self.logger.error('Backup error')
        return result

    def ping(self, ip, repeat=5):
        self.sendline("ping {} repeat {}".format(ip, repeat))

    def find_port_from_mac(self, mac, ip=None):
        self.end()
        self.enable()

        mac = convert_mac_allied(mac)

        if ip is not None:
            self.ping(ip, 3)
            self.expectPrompt()

        self.sendline("show mac address-table | include {}".format(mac))
        self.expectPrompt()

        match = re.search('^([0-9][0-9]*)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^ ]*)$', self.before(), re.MULTILINE)
        if match:
            return match.group(2)
        else:
            return ""

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
        self.sendline('int {}'.format(port))
        self.expectPrompt()

        if description is not None:
            self.sendline('description {}'.format(description))
            self.expectPrompt()

        self.sendline('switchport trunk allowed vlan add {}'.format(vlan_id))
        self.expectPrompt()

    def add_vlan_to_portlist(self, vlan_id, port_list, description=None):
        self.end()
        self.enable()
        self.conft()

        for port in port_list:
            self.add_vlan_to_port(vlan_id, port, description)

        self.write()

    def expectPrompt(self):
        return super(SwitchAllied, self).expectPrompt()

    def login(self, login, password):
        if super(SwitchAllied, self).login(login, password):
            self.expectPrompt()
            return True
        else:
            return False

    def logout(self):
        return super(SwitchAllied, self).logout()

    def getSwitchCommands(self):
        return switchAlliedCommands
