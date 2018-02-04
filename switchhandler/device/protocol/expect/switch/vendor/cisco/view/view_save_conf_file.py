# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import datetime
import re

from switchhandler.device.executable.command.command_base import CommandBase


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

    def define_argument(self):
        self.add_argument(name='folder', default=None)
        self.add_argument(name='add_timestamp', default=False)

    def arg_default(self):
        # self.folder = getattr(self, 'folder', None)
        # self.add_timestamp = getattr(self, 'add_timestamp', False)
        pass

    def _build_filepath(self, folder, add_timestamp):
        filepath = "{}_{}_{}".format(
            self.switch.IP,
            self.switch.hostname,
            self.switch.vendor
        )

        if folder:
            filepath = "{}/{}".format(folder, filepath)

        if add_timestamp:
            filepath = "{}_{:%Y%m%d-%H%M%S}".format(
                filepath,
                datetime.datetime.today()
            )

        return filepath

    def sanitize(self, confStr):
        confStr = re.sub(r'show running-config\s*\n', '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'Building configuration...\s*\n', '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'Current configuration .*\s*\n', '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'! Last configuration change at .*\s*\n', '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'! NVRAM config last updated at .*\s*\n', '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'! No configuration change since last restart\s*\n', '', confStr, flags=re.MULTILINE)

        confStr = re.sub(r'ntp clock-period [0-9]*\s*\n', '', confStr, flags=re.MULTILINE)

        return confStr

    def do_run(self):
        self.switch.execute('end')

        self.switch.sendline('terminal length 0')
        self.switch.expectPrompt()

        self.switch.sendline('show running-config')
        self.switch.expectPrompt()

        confStr = self.sanitize(self.switch.before())
        try:
            with open(self._build_filepath(self.folder, self.add_timestamp), 'w') as f:
                f.write(confStr)

            self.switch.logger.info('Backup complete')
            return True
        except FileNotFoundError as e:
            self.switch.logger.error('Backup error {}'.format(e))
            return False
