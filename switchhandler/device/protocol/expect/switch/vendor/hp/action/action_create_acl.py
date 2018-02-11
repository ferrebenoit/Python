'''
Created on 9 mai 2017

@author: ferreb
'''
from switchhandler.device.executable.action.action_base import ActionBase
from switchhandler.device.protocol.expect.switch.vendor.hp import CATEGORY_HP
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_HP, registered_name="create_acl")
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

    def define_argument(self):
        self.add_argument(name='name', required=True)
        self.add_argument(name='acl_entries', required=True)
        self.add_argument(name='acl_replace', default=None)
        self.add_argument(name='inverse_src_and_dst', default=False)
        self.add_argument(name='acl_conditions', default=None)

    def do_run(self):
        self.switch.execute('end')
        self.switch.execute('conft')

        self.switch.execute('no_acl', name=self.name)

        self.switch.execute('acl', name=self.name)

        for item in self.acl_entries:
            self.switch.execute('acl_add_row',
                                name=self.name,
                                row=item,
                                acl_replace=self.acl_replace,
                                acl_conditions=self.acl_conditions,
                                inverse_src_and_dst=self.inverse_src_and_dst
                                )

        self.switch.execute('write')
