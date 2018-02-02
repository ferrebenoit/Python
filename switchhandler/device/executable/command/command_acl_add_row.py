# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
import json
import re

from switchhandler.device.executable.command.command_base import CommandBase


class CommandACLAddRow(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    :param name: le nom de l'acl
    :type  name: str
    :param row: Les entrées de la ligne d'acl
    :type  row: dict
    :param acl_replace: les variables de remplacements ***default : *** None
    :type  acl_replace: dict
    :default acl_replace: None
    :param acl_conditions: Les condition pour affecter les entrées de l'acl au switch ***default : *** None
    :type acl_conditions: dict
    :default acl_conditions: None
    :param inverse_src_and_dst: inverse source et destination
    :type  inverse_src_and_dst: bool
    :default inverse_src_and_dst: False




    Commandes exécutées::

      prompt#
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

<<<<<<< HEAD
    def define_argument(self):
        self.add_argument(name='name', required=True)
        self.add_argument(name='row', required=True)
        self.add_argument(name='acl_replace', default=None)
        self.add_argument(name='acl_conditions', default=False)
        self.add_argument(name='inverse_src_and_dst', default=None)

    def arg_default(self):
        # self.acl_replace = getattr(self, 'acl_replace', None)
        # self.inverse_src_and_dst = getattr(self, 'inverse_src_and_dst', False)
        # self.acl_conditions = getattr(self, 'acl_conditions', None)
        pass

    def do_run(self):
        if self.acl_replace is not None:
            for k in self.row.keys():
                if(k in self.acl_replace):
                    self.row[k] = self.row[k].format(**self.acl_replace[k])

        condition_str = getattr(self.row, 'condition', '')

        if condition_str == '':
            condition_str = '{}'
        conditions = json.loads(condition_str)

        for k in self.acl_conditions.keys():
            if re.search(conditions.get(k, '.*'), self.acl_conditions[k], re.IGNORECASE):
                #:
=======
    def arg_default(self):
        self.acl_replace = getattr(self, 'acl_replace', None)
        self.inverse_src_and_dst = getattr(self, 'inverse_src_and_dst', False)
        self.acl_conditions = getattr(self, 'acl_conditions', None)

    def do_run(self):
        if self.acl_replace is not None:
            for k in self.row.keys():
                if(k in self.acl_replace):
                    self.row[k] = self.row[k].format(**self.acl_replace[k])

        condition_str = self.row['condition']
        if condition_str == '':
            condition_str = '{}'
        conditions = json.loads(condition_str)

        for k in self.acl_conditions.keys():
            if re.search(conditions.get(k, '.*'), self.acl_conditions[k], re.IGNORECASE):
                # if condition in row['condition']:
>>>>>>> refs/remotes/origin/master

                self.switch.execute('acl_add_entry',
                                    name=self.name,
                                    index=self.row['index'],
                                    action=self.row['action'],
                                    protocol=self.row['protocol'],
                                    src1=self.row['src1'],
                                    src2=self.row['src2'],
                                    src_port_operator=self.row['src_port_operator'],
                                    src_port=self.row['src_port'],
                                    dst1=self.row['dst1'],
                                    dst2=self.row['dst2'],
                                    dst_port_operator=self.row['dst_port_operator'],
                                    dst_port=self.row['dst_port'],
                                    log=self.row['log'],
                                    inverse_src_and_dst=self.inverse_src_and_dst
                                    )
