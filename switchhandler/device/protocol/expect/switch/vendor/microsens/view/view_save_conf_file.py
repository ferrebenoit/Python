# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import datetime
import os

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.microsens.utils import parse_vlan


class ViewSaveConfFile(CommandBase):
    '''Charger un fichier sur le switch


    :param folder:
    :type  folder:
    :param add_timestamp:
    :type  add_timestamp:

    :default add_timestamp:False
    :default folder:None:

    Commandes exécutées::

      ViewSaveConfFile(path='localPath', add_timestamp=false)

      prompt# copy tftp://10.1.1.1/remote/file flash:/local/file
      prompt#

    '''

    def arg_default(self):
        self.folder = getattr(self, 'folder', None)
        self.add_timestamp = getattr(self, 'add_timestamp', False)

    def _build_folderpath(self, folder, conf_type):
        folderpath = "Microsens/{}/export/".format(
            self.switch.IP,
        )
        if folder:
            folderpath = "{}/{}".format(folder, folderpath)

        return folderpath

    def _build_filepath(self, folder, conf_type, add_timestamp):
        filepath = "{}{}".format(
            self._build_folderpath(folder, conf_type),
            conf_type
        )

        if add_timestamp:
            filepath = "{}_{:%Y%m%d-%H%M%S}".format(
                filepath,
                datetime.datetime.today()
            )

        return filepath

    def sanitize(self, confStr):
        return "\n".join(confStr.split('\n')[1:-1])

    def analyse_conf(self, conf_type, rege):
        pass

    def backup_conf(self, conf_type, command):
        self.switch.sendline(command)
        self.switch.expectPrompt()

        confStr = self.sanitize(self.switch.before())
        try:
            directory = self._build_folderpath(self.folder, conf_type)
            file = self._build_filepath(self.folder, conf_type, self.add_timestamp)

            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file, 'w') as f:
                f.write(confStr)

            self.switch.logger.info('Backup {} complete'.format(conf_type))
            return confStr
        except FileNotFoundError as e:
            self.switch.logger.error('Backup {} error {}'.format(conf_type, e))
            return None

    def do_run(self):
        self.backup_conf('cdp', 'show cdp config')
        self.backup_conf('POE', 'show port power')
        conf = self.backup_conf('vlan', 'show vlan')
        print(parse_vlan(conf))
        return True
