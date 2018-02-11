'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="create_read_username")
class ActionCreateReadUsername(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    Commandes exécutées::

      prompt#
      prompt#
    '''

    def define_argument(self):
        self.add_argument(name='username', required=True)
        self.add_argument(name='userpassword', required=True)

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
