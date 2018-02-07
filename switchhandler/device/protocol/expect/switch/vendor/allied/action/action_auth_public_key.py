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
        self.add_argument(name='keyuser', required=True)
        self.add_argument(name='keypath', required=True)
        self.add_argument(name='tftpip', required=True)

    def arg_default(self):
        # self.tftp_ip = getattr(self, 'tftp_ip', None)
        pass

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('enable')

        self.switch.execute('upload_file_tftp',
                            local_file_path='pub_key.tmp',
                            tftp_ip=self.tftpip,
                            remote_file_path=self.keypath)

        self.switch.execute('conft')

        self.switch.send_line(
            'crypto key pubkey-chain userkey {} pub_key.tmp'.format(self.keyuser))
        self.switch.expect_prompt()

        self.switch.execute('end')

        self.switch.send_line('del force pub_key.tmp')
        self.switch.expect_prompt()
        # self.switch.execute('end')
        # self.switch.execute('enable')
        # self.switch.execute('conft')

        # self.switch.send_line('crypto key pubkey-chain userkey {}'.format(self.keyuser))
        # self.switch.expect('Type CNTL/D to finish:')
        # self.switch.send_line(self.key)
        # self.switch.sendcontrol('d')

        # self.switch.expect_prompt()

        # self.switch.execute('write')
        return True
