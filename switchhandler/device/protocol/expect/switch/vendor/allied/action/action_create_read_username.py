'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase


class ActionCreateReadUsername(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    Commandes exécutées::

      prompt#
      prompt#
    '''

    def define_argument(self):
        self.add_argument(name='username', required=True)
        self.add_argument(name='userpassword', required=True)

    def arg_default(self):
        # self.tftp_ip = getattr(self, 'tftp_ip', None)
        pass

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('enable')
        self.switch.execute('conft')

        self.switch.execute('username',
                            username=self.username,
                            level='7',
                            userpassword=self.userpassword)

        self.switch.execute('write')
        return True
