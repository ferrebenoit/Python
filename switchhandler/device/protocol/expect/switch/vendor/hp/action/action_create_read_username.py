'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="create_read_username")
class ActionCreateReadUsername(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    Commandes exécutées::

      prompt#
      prompt#
    '''

    def define_argument(self):
        pass

    def do_run(self):
        # maybe use this command to change operator and manager accounts
        self.switch.log_info('Create read Username: Nothing to do in HP switchs')
        return True
