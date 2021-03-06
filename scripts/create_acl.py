#!/usr/bin/env python3
from _csv import reader
import csv
import os
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class CreateAcl(SwitchScripter):

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--aclname', help='The acl Name')
        self._arg_parser.add_argument('--vlanid', help='the vlan id')
        #self._arg_parser.add_argument('--siteid', help='the site id')
        self._arg_parser.add_argument('--secondaryserver', help='the secondary server')
        self._arg_parser.add_argument('--csvaclentries', help='The csv file that holds the contents')

        self._arg_parser.add_argument('--vlan1', help='the vlan1')
        self._arg_parser.add_argument('--vlan30', help='the vlan1')
        self._arg_parser.add_argument('--vlan252', help='the vlan1')
        self._arg_parser.add_argument('--vlan262', help='the vlan1')
        self._arg_parser.add_argument('--vlan1cidr', help='the vlan1')
        self._arg_parser.add_argument('--vlan30cidr', help='the vlan1')
        self._arg_parser.add_argument('--vlan252cidr', help='the vlan1')
        self._arg_parser.add_argument('--vlan262cidr', help='the vlan1')

        self._add_mandatory_arg('aclname',
                                'csvaclentries',
                                'vlanid',
                                'siteid',
                                'secondaryserver',
                                )

    def _common_actions(self, switch, args):
        self._create_acl(switch, args, "In", False)

        self._create_acl(switch, args, "Out", True)

    def _create_acl(self, switch, args, acl_suffix, inverse_src_and_dst):
        if not os.path.isfile(args['csvaclentries']):
            print('fichier de l acl non trouve')
            exit

        if not switch.login(args['login'], args['password']):
            print('impossible de s''authentifier')
        else:
            # build replace dict
            aclreplace = {}
            aclreplace['src1'] = {
                'vlanid': args['vlanid'],
                'siteid': args['siteid'],
                'vlan1': args.get('vlan1', ''),
                'vlan30': args.get('vlan30', ''),
                'vlan252': args.get('vlan252', ''),
                'vlan262': args.get('vlan262', ''),
            }
            aclreplace['src2'] = {
                'vlan1cidr': args.get('vlan1cidr', ''),
                'vlan30cidr': args.get('vlan30cidr', ''),
                'vlan252cidr': args.get('vlan252cidr', ''),
                'vlan262cidr': args.get('vlan262cidr', ''),
            }
            aclreplace['dst1'] = {'vlanid': args['vlanid'], 'siteid': args['siteid']}
            aclreplace['dst2'] = {'secondaryserver': args['secondaryserver']}

            # build condition dict
            acl_conditions = {}
            acl_conditions['vendor'] = switch.vendor

            with open(args['csvaclentries']) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
                # switch.create_ACL(args['aclname'] + acl_suffix, reader, ['wyse={}'.format(args['wyse'])], aclreplace, inverse_src_and_dst)
                switch.execute('create_acl',
                               name=args['aclname'] + acl_suffix,
                               acl_entries=reader,
                               acl_replace=aclreplace,
                               acl_conditions=acl_conditions,
                               inverse_src_and_dst=inverse_src_and_dst
                               )

            switch.logout()


create_acl = CreateAcl('Add access list', sys.argv[1:])
create_acl.process()
