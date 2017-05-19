# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
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
        try:
            self.switch.sendline(
                'copy {} tftp://{}/{}'.format(self.local_file_path, self.tftp_ip, self.remote_file_path))

            # host confirmation
            self.switch.expect('Address or name of remote host \[.*\]\?')
            self.switch.sendline()

            # check if host is correct and filename confirmation
            match = self.switch.expect(
                ['Destination filename \[.*\]\?', 'Invalid host address or name'])
            if(match == 1):
                print('Hote inconnu')
                return False

            self.switch.sendline()

            # check if all good
            match = self.switch.expect(
                ['[0-9]* bytes copied in .*\r\n', '%Error opening tftp.*\r\n'], timeout=60)

            if(match == 0):
                return True
            elif(match == 1):
                print('sauvegarde Echouee')
                print(self.switch.connection.before)
                return False

            # Consume prompt response
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
