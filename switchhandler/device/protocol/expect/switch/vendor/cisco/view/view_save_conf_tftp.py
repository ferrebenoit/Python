# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import datetime

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name="save_conf_tftp")
class ViewSaveConfTFTP(CommandBase):
    '''Charger un fichier sur le switch


    :param tftp_ip:
    :type  tftp_ip:
    :param folder:
    :type  folder:
    :param add_timestamp:
    :type  add_timestamp:

    :default add_timestamp:False
    :default folder:None:

    Commandes exécutées::

      ViewSaveConfTFTP(tftp_ip='10.1.1.1', folder='folder', add_timestamp=True)

      prompt# copy tftp://10.1.1.1/remote/file flash:/local/file
      prompt#

    '''

    def define_argument(self):
        self.add_argument(name='tftp_ip', required=True)
        self.add_argument(name='folder', required=True, default=None)
        self.add_argument(name='add_timestamp', required=True, default=False)

    def _build_tftp_filepath(self, folder, add_timestamp):
        filepath = "{}_{}_{}".format(self.switch.IP, self.switch.hostname, self.switch.vendor)

        if folder:
            filepath = "{}/{}".format(folder, filepath)

        if add_timestamp:
            filepath = "{}_{:%Y%m%d-%H%M%S}".format(filepath, datetime.datetime.today())

        return filepath

    def do_run(self):
        self.switch.execute('end')

        result = self.switch.execute(
            'download_file_tftp',
            tftp_ip=self.tftp_ip,
            local_file_path='system:running-config',
            remote_file_path=self._build_tftp_filepath(self.folder, self.add_timestamp))
        if result:
            self.switch.logger.info('Backup complete')
        else:
            self.switch.logger.error('Backup error')
        return result
