# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="username")
class CommandUsername(CommandBase):
    '''Créer un nouvel utilisateur

    :param username: le nom de l'utilisateur
    :type name: str
    :param level: les droits de l'utilisateur
    :type level: int
    :param userpass: le mot de passe de l'utilisateur
    :type userpass: str


    Commandes exécutées::

      prompt# username USERNAME privilege LEVEL secret USERPASS
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def define_argument(self):
        self.add_argument(name='username', required=True)
        self.add_argument(name='level', required=True)
        self.add_argument(name='userpassword', required=True)

    def do_run(self):
        self.switch.send_line('username {} privilege {} password {}'.format(
            self.username,
            self.level,
            self.userpassword))
        self.switch.expect_prompt()
        self.switch.send_line('ssh server allow-users {}'.format(self.username))
        self.switch.expect_prompt()
        return True
