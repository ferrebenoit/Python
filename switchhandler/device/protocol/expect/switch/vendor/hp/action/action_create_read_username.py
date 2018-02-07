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
        pass

    def arg_default(self):
        # self.tftp_ip = getattr(self, 'tftp_ip', None)
        pass

    def do_run(self):
        # maybe use this command to change operator and manager accounts
        self.switch.log_info('Create read Username: Nothing to do in HP switchs')
        return True
