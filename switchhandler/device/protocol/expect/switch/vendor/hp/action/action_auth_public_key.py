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

<<<<<<< HEAD
    def define_argument(self):
        self.add_argument(name='username', required=True)
        self.add_argument(name='key', required=True)
        self.add_argument(name='comment', required=True)
        self.add_argument(name='tftp_ip', default=None)

    def arg_default(self):
        # self.tftp_ip = getattr(self, 'tftp_ip', None)
        pass

    def do_run(self):
        self.switch.execute('end')
=======
    def arg_default(self):
        self.tftp_ip = getattr(self, 'tftp_ip', None)

    def do_run(self):
        self.switch.end()
>>>>>>> refs/remotes/origin/master

        self.switch.sendline('copy tftp pub-key-file {} {} manager append'.format(
            self.tftp_ip,
            self.key
        ))
        self.switch.expectPrompt()

        self.execute('conft')

        self.switch.sendline('aaa authentication ssh login public-key')
        self.switch.expectPrompt()

        self.switch.execute('write')
        return True
