#!/usr/bin/env python3
import sys

from switchhandler.switch.switch_scripter import SwitchScripter


class CreateAcl(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--aclname', help='The acl Name')
        self._arg_parser.add_argument('--intname', help='the interface')
        self._arg_parser.add_argument('--inbound', help='the interface', choices=['yes', 'no'], default='yes')

        self._add_mandatory_arg('aclname', 'intname', 'inbound')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de s''authentifier')
        else:
            switch.execute('add_acl_to_interface',
                           args['aclname'] + 'IN',
                           args['intname'],
                           True
                           )
            switch.execute('add_acl_to_interface',
                           args['aclname'] + 'OUT',
                           args['intname'],
                           False
                           )

            switch.logout()

create_acl = CreateAcl('Add access list', sys.argv[1:])
create_acl.process()
