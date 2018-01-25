# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase


class ViewUploadFileTFTP(CommandBase):
    '''Charger un fichier sur le switch


    :param tftp_ip,
    :type  tftp_ip,
    :param local_file_path,
    :type  local_file_path,
    :param remote_file_path
    :type  remote_file_path

    Commandes exécutées::

      ViewUploadFileTFTP(tftp_ip='10.1.1.1', local_file_path='local/file', remote_file_path='remote/file')

      prompt# copy tftp://10.1.1.1/remote/file flash:/local/file
      prompt#

    '''

    def do_run(self):
        self.switch.sendline(
            'copy tftp://{}/{} flash:/{}'.format(self.tftp_ip, self.local_file_path, self.remote_file_path))
        self.switch.expectPrompt()
