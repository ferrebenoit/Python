'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.switch.action.action_base import ActionBase


class ActionCreateACL(ActionBase):
    '''Créé une acl et y insert des entées depuis un fichier CSV
    si lacl existe déjà elle est effacée puis re-créée

    :param name: le nom de l'ACL
    :type name: str
    :param acl_entries: les entrées de l'acl
    :type acl_entries: dict
    :param acl_replace: Les variables qui seront remplacées dans acl_entries.
    :type acl_replace: dict
    :default acl_replace: None
    :param inverse_src_and_dst:
    :type inverse_src_and_dst: Bool
    :default inverse_src_and_dst: False
    '''

    def arg_default(self):
        self.acl_replace = getattr(self, 'acl_replace', None)
        self.inverse_src_and_dst = getattr(self, 'inverse_src_and_dst', False)

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.execute('delete_acl', name=self.name)

        self.switch.execute('acl', name=self.name)

        for item in self.acl_entries:
            self.switch.execute('add_acl_row',
                                row=item,
                                acl_replace=self.acl_replace,
                                inverse_src_and_dst=self.inverse_src_and_dst
                                )

        self.switch.execute('write')
