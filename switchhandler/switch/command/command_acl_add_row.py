# -*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.command.command_base import CommandBase


class CommandACLAddRow(CommandBase):
    '''Créer/se placer dans la configuration d'une ACL

    def ACL_add_row(self, row, acl_replace=None, inverse_src_and_dst=False):
    :param row: Les entrées de la ligne d'acl
    :type  row: dict
    :param acl_replace: les variables de remplacements
    :type  acl_replace: dict
    :default acl_replace: None
    :param inverse_src_and_dst: inverse source et destination
    :type  inverse_src_and_dst: bool
    :default inverse_src_and_dst: False




    Commandes exécutées::

      prompt#
      prompt#

    '''
    # TODO: Check configMode self.getConfigMode() == ConfigMode.GLOBAL

    def do_run(self):
        if self.acl_replace is not None:
            for k in row.keys():
                if(k in self.acl_replace):
                    row[k] = row[k].format(**self.acl_replace[k])

        # if condition in row['condition']:

        self.switch.execute('acl_add_entry',
                            index=row['index'],
                            action=row['action'],
                            protocol=row['protocol'],
                            src1=row['src1'],
                            src2=row['src2'],
                            src_port_operator=row['src_port_operator'],
                            src_port=row['src_port'],
                            dst1=row['dst1'],
                            dst2=row['dst2'],
                            dst_port_operator=row['dst_port_operator'],
                            dst_port=row['dst_port'],
                            log=row['log'],
                            inverse_src_and_dst=inverse_src_and_dst
                            )
