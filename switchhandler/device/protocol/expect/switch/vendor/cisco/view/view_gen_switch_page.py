# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import datetime

from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_CISCO, registered_name='gen_switch_page')
class ViewGenSwitchPage(CommandBase):
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

    def do_run(self):
        interfaces = self.switch.get_fact('int')
        if interfaces is None:
            self.switch.logger.error(
                'Switch report error: Could not get interfaces')
            return False

        # for value in interfaces.values():
        #    print(value.name)
        #    print(value.portspeed)
        #    print(value.portnumber)
        #    print(value.description)
        #    print(value.trunkingmode)
        #    print(value.vlanaccess)
        #    print(value.vlantagged)
        #    print(value.speed)
        #    print(value.duplex)

        # try:
        #    if not os.path.exists(self.folder):
        #        os.makedirs(self.folder)
        #
        #    with open(self._build_filepath(self.folder, self.add_timestamp), 'w') as f:
        #        f.write(conf['sanitized'])
        #
        #    self.switch.logger.info('Backup complete')
        #    return True
        # except FileNotFoundError as e:
        #    self.switch.logger.error('Backup error {}'.format(e))
        #    return False
