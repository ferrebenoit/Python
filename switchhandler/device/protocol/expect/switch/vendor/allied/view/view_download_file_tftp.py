# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from pexpect.exceptions import TIMEOUT, EOF

from switchhandler.device.executable.command.command_base import CommandBase


class ViewDownloadFileTFTP(CommandBase):
    '''télécharger un fichier depuis le switch


    :param tftp_ip:
    :type  tftp_ip:
    :param local_file_path:
    :type  local_file_path:
    :param remote_file_path:
    :type  remote_file_path:

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
        try:
            self.switch.sendline(
                'copy {} tftp://{}/{}'.format(
                    self.local_file_path,
                    self.tftp_ip,
                    self.remote_file_path))

            match = self.switch.connection.expect(['Successful operation', '% Network is unreachable', '% Invalid tftp destination'])
            if match > 0:
                print('Sauvegarde echouee ')
                return False
            elif match == 0:
                return True

            self.switch.expectPrompt()
        except TIMEOUT:
            print("Sauvegarde echouee a cause d'un timeout")
            print(self.switch.connection.before)
        except EOF:
            print("Sauvegarde echouee a cause d'une deconnexion")
            print(self.switch.connection.before)
        except Exception:
            print('exception')
            # print(e)
            print(self.switch.connection.before)
            print(self.switch.connection.after)
