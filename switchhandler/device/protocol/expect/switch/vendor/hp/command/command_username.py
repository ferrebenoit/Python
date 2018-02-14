# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.command.command_base import CommandBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="username")
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
        pass

    def do_run(self):
        # maybe use this command to rename and change passord of user operator and manager
        self.switch.log_info('Command Username : Nothing to do in HP switchs')
        return True
