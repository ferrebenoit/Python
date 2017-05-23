# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from pexpect.exceptions import EOF, TIMEOUT

from switchhandler.switch.command_base import CommandBase


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

    def do_run(self):
        # copy running-config tftp://192.168.0.1/
        try:
            self.switch.sendline(
                'copy {} tftp {} {}'.format(
                    self.localFilePath,
                    self.TFTP_IP,
                    self.RemoteFilePath
                ))

            match = self.switch.connection.expect([self._PROMPT, '00000K Peer unreachable.', 'Invalid input:'])
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
