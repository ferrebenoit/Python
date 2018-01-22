#!/usr/bin/env python3
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class CreateAcl(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--aclname', help='The acl Name')
        self._arg_parser.add_argument('--intname', help='the interface')
        #self._arg_parser.add_argument('--inbound', help='the interface', choices=['yes', 'no'], default='yes')

        self._add_mandatory_arg('aclname', 'intname', 'inbound')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de s''authentifier')
        else:
            switch.execute('add_acl_to_interface',
                           acl_name=args['aclname'] + 'IN',
                           interface_name=args['intname'],
                           inbound=True
                           )
            switch.execute('add_acl_to_interface',
                           acl_name=args['aclname'] + 'OUT',
                           interface_name=args['intname'],
                           inbound=False
                           )

            switch.logout()


create_acl = CreateAcl('Assign access list to interface', sys.argv[1:])
create_acl.process()


# class CreateAclWorker(BaseWorker):
#
#    def __init__(self, **args):
#        pass
#
#    def run(self):
#        pass
#
#
# class CreateAcl(SwitchScripter):
#
#    def __init__(self, description, args, future_funtion):
#        super().__init__(description, args)
#
