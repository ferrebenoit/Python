# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from pexpect.exceptions import EOF, TIMEOUT

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="download_file_tftp")
class ViewDownloadFileTFTP(CommandBase):
    '''télécharger un fichier depuis le switch


    :param tftp_ip,
    :type  tftp_ip,
    :param local_file_path,
    :type  local_file_path,
    :param remote_file_path
    :type  remote_file_path

    Commandes exécutées::

      ViewDownloadFileTFTP(tftp_ip='10.1.1.1', local_file_path='local/file', remote_file_path='remote/file')

      prompt# copy local/file tftp://10.1.1.1/remote/file
      prompt#

    '''

    def define_argument(self):
        self.add_argument(name='tftp_ip', required=True)
        self.add_argument(name='local_file_path', required=True)
        self.add_argument(name='remote_file_path', required=True)

    def do_run(self):
        # copy running-config tftp://192.168.0.1/
        try:
            self.switch.sendline(
                'copy {} tftp {} {}'.format(
                    self.local_file_path,
                    self.tftp_ip,
                    self.remote_file_path
                ))

            match = self.switch.connection.expect([self.switch.prompt, '00000K Peer unreachable.', 'Invalid input:'])
            if match > 0:
                print('Sauvegarde echouee ')
                return False
            elif match == 0:
                return True

            self.switch.expect_prompt()
        except TIMEOUT:
            print("Sauvegarde echouee a cause d'un timeout")
            print(self.switch.connection.before)
        except EOF:
            print("Sauvegarde echouee a cause d'une deconnexion")
            print(self.switch.connection.before)
        except Exception as e:
            print('exception {}'.format(e))
            # print(e)
            print(self.switch.connection.before)
            print(self.switch.connection.after)
