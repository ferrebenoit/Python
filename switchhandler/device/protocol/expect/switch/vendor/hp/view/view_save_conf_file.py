# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import datetime
import os

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="save_conf_file")
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
        return "\n".join(confStr.split('\n')[5:-1])

    def do_run(self):
        # self.switch.execute('conft')
        # self.switch.sendline('console local-terminal vt100')
        # self.switch.expect_prompt()
        # print('/', self.switch.connection.before.decode('UTF-8'), '/')

        self.switch.execute('end')

        self.switch.send_line('terminal length 1000')
        self.switch.expect_prompt()
        self.switch.send_line('show running-config')

        self.switch.expect_prompt()

        confStr = self.sanitize(self.switch.before())
        if len(confStr) == 0:
            self.switch.log_warning('Sauvegarde 0 octet')
            return False

        try:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            with open(self._build_filepath(self.folder, self.add_timestamp), 'w') as f:
                f.write(confStr)

            self.switch.logger.info('Backup complete')
            return True
        except FileNotFoundError as e:
            self.switch.logger.error('Backup error {}'.format(e))
            return False
