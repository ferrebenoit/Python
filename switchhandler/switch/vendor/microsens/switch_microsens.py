'''
Created on 8 juin 2017

@author: ferreb
'''
from switchhandler.switch.switch_base import SwitchBase
from switchhandler.switch.vendor.microsens import switchMicrosensCommands

vlan_table = {
    '1': '1',
    '30': '2',
    '252': '3',
    '262': '4',
    '160': '5',
    '29': '6',
    '80': '7',
    '15': '8',
    '10': '9',
    '70': '10',
    '100': '11',
}


def convert_vlan_id_to_vlan_filter(vlan_id):
    return vlan_table.get(vlan_id, 0)


class SwitchMicrosens(SwitchBase):

    def __init__(self, IP, site=None, dryrun=False):
        super(SwitchMicrosens, self).__init__(IP, 'microsens', site, dryrun)

        self._PROMPT = 'Console(?P<exec>[>#])$'

    def getExecLevel(self):
        if self.exec == '>':
            return Exec.USER
        elif self.exec == '#':
            return Exec.PRIVILEGED

    def getConfigMode(self):
        ConfigMode.GLOBAL

    def expectPrompt(self):
        return super(SwitchMicrosens, self).expectPrompt()

    def _ssh_login(self, login, password):
        self.logger.info('SSH not implemented for microsens switches')
        return False

    def _telnet_login(self, login, password):
        self.connect()
        self.connection._spawn("telnet {}".format(login, self.IP))

        # in telnet microsens switch expect only password
        self.connection.expect('password:')
        self.connection.sendline(password)

        self.sendline()

        self.expectPrompt()

        return True

    def logout(self):
        return super(SwitchAllied, self).logout()

    def getSwitchCommands(self):
        return switchMicrosensCommands
