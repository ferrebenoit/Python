'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase


class ActionAuthPublicKey(ActionBase):
    '''Ajouter un Vlan avec son Id, nom, IP, netmask, ip helper


    def auth_PublicKey(self, username, key, comment, TFTP_IP=''):
    :param username: Le nom d'utilisateur à associer à la clé
    :type  username: str
    :param key: La clé
    :type  key: str
    :param comment: Commentaire
    :type  comment: str
    :param tftp_ip: ip du tftp
    :type  tftp_ip: str
    :default  tftp_ip: None

    Commandes exécutées::

      prompt#
      prompt#
    '''

    def define_argument(self):
        # operator is neverused so ignore keyuser in this commad
        # self.add_argument(name='keyuser', required=True)
        self.add_argument(name='keypath', required=True)
        self.add_argument(name='tftpip', required=True)

    def arg_default(self):
        # self.tftp_ip = getattr(self, 'tftp_ip', None)
        pass

    def do_run(self):
        self.switch.execute('end')

        self.switch.send_line('copy tftp pub-key-file {} {} manager append'.format(
            self.tftpip,
            self.keypath
        ))
        self.switch.expect_prompt()

        self.switch.execute('conft')

        self.switch.send_line('aaa authentication ssh login public-key')
        self.switch.expect_prompt()

        self.switch.execute('write')
        return True
