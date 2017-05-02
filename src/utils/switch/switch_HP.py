import re

from pexpect.exceptions import TIMEOUT, EOF

from utils.network.net_tools import convert_to_netmask, convert_to_wildcard,\
    convert_mac_HP
from utils.switch.switch_base import SwitchBase, ConfigMode, Exec


class SwitchHP(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchHP, self).__init__(IP, 'hp', site, dryrun)

        # prompt rexex
        self._PROMPT = '([A-Za-z0-9\-]*)(\((.*)\))*([>#])'

    @property
    def hostname(self):
        ''' strip the initial '1H' from the host name
        '''
        hostname = super(SwitchHP, self).hostname
        if not super(SwitchHP, self).hostname == 'None':
            hostname = hostname[2:]

        return hostname

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

    def auth_PublicKey(self, username, key, comment, TFTP_IP=''):
        self.end()

        self.sendline('copy tftp pub-key-file {} {} manager append'.format(TFTP_IP, key))
        self.expectPrompt()

        self.conft()

        self.sendline('aaa authentication ssh login public-key')
        self.expectPrompt()

        self.write()
        return True

    def uploadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        self.sendline('copy tftp flash {} {}'.format(TFTP_IP, localFilePath, RemoteFilePath))
        self.expectPrompt()

        return True

    def downloadFileTFTP(self, TFTP_IP, localFilePath, RemoteFilePath):
        # copy running-config tftp://192.168.0.1/
        try:
            self.sendline('copy {} tftp {} {}'.format(localFilePath, TFTP_IP, RemoteFilePath))

            match = self.connection.expect([self._PROMPT, '00000K Peer unreachable.', 'Invalid input:'])
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

    def create_vlan(self, ID, name, IP=-1, network=-1, IP_helper=-1):
        self.end()
        self.enable()
        self.conft()

        self.vlan(ID, name)

        # If IP mask and CIDR are provided add an IP to the vlan
        if IP != -1 and network != -1:
            self.ip_address(IP, network)
            self.ip_helper(IP_helper)

        self.write()

    def create_ACL(self, name, acl_entries, acl_replace=None, inverse_src_and_dst=False):
        self.end()
        self.conft()

        self.ACL(name)

        for row in acl_entries:
            self.ACL_add_row(name, row, acl_replace, inverse_src_and_dst)

        self.write()

    def ACL(self, name):
        self.sendline('ip access-list extended "{}"'.format(name))
        self.expectPrompt()

    def ACL_add_entry(self, name, index, action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port, log, inverse_src_and_dst=False):
        # if protocol is icmp discard the entry as HP does not deny/accept ICMP
        if (protocol.lower() == 'icmp'):
            return

        if (src1.lower() != 'host'):
            src2 = convert_to_wildcard(src2)

        if (dst1.lower() != 'host'):
            dst2 = convert_to_wildcard(dst2)

        if inverse_src_and_dst:
            self.sendline('{} {} {} {} {} {} {} {} {} {}'.format(action, protocol, dst1, dst2, dst_port_operator, dst_port, src1, src2, src_port_operator, src_port))
        else:
            self.sendline('{} {} {} {} {} {} {} {} {} {}'.format(action, protocol, src1, src2, src_port_operator, src_port, dst1, dst2, dst_port_operator, dst_port))
        self.expectPrompt()

    def delete_acl(self, name):
        pass

    def add_acl_to_interface(self, acl_name, interface_name, inbound=True):
        pass

    def add_ospf_router(self, network, networkID):
        pass

    def vlan(self, ID, name=None):
        self.sendline('vlan {}'.format(ID))
        self.expectPrompt()

        if name is not None:
            self.sendline('name "{}"'.format(name))
            self.expectPrompt()

    def int_vlan(self, ID, name=None):
        self.vlan(ID, name)

    def ip_address(self, IP, network):
        self.sendline('ip address {} {}'.format(IP, convert_to_netmask(network)))
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
        self.sendline('write memory')
        self.expectPrompt()

    def save_conf_TFTP(self, TFTP_IP, folder=None, add_timestamp=False):
        self.end()

        result = self.downloadFileTFTP(TFTP_IP, 'running-config', self._build_tftp_filepath(folder, add_timestamp))

        if result:
            self.logger.info('Backup complete')
        else:
            self.error('Backup error')
        return result

    def ping(self, ip, repeat=5):
        self.sendline("ping {} repetitions {}".format(ip, repeat))

    def find_port_from_mac(self, mac, ip=None):
        self.end()
        mac = convert_mac_HP(mac)

        if ip is not None:
            self.ping(ip, 3)
            self.expectPrompt()

        self.sendline("show mac-address {}".format(mac))
        self.expectPrompt()

        match = re.search('Located on Port : ([A-Z][0-9]+)', self.before(), re.MULTILINE)
        if match:
            return match.group(1)
        else:
            return ""

    def add_tagged_vlan_to_port(self, vlan_id, port, description=None):
        self.sendline('vlan {}'.format(vlan_id))
        self.expectPrompt()

        self.sendline('tagged {}'.format(port))
        self.expectPrompt()

        if description is not None:
            self.sendline('interface {}'.format(port))
            self.expectPrompt()
            self.sendline('name {}'.format(description))
            self.expectPrompt()

    def expectPrompt(self):
        return super(SwitchHP, self).expectPrompt()

    def login(self, login, password):
        try:
            if self.dryrun:
                self.logger.info("Login ok as user {}".format(login))
                return True

            self.connect()
            self.connection._spawn("ssh {}@{} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".format(login, self.IP))

            self.connection.expect('password:')
            self.connection.sendline(password)

            self.sendline()
            self._loadPromptState()

            self.expectPrompt()

            self.logger.info("Login ok as user {}".format(login))
            return True
        except:
            self.logger.critical(self.connection.before)
            self.logger.critical(self.connection.after)
            self.logger.error("Connection error")
            return False

        return False

    def logout(self):
        if super(SwitchHP, self).logout():
            self.expect('[y/n]?')
            self.send('y')
            return True
        else:
            return False
