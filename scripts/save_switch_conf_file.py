#!/usr/bin/env python3
# coding: utf-8

'''
Created oén 23 nov. 2016

@author: FERREB
'''

import datetime
from pathlib import Path
import sys

from jinja2 import Template

from switchhandler.script.switch_scripter import SwitchScripter


class SaveSwitchConf(SwitchScripter):
    "Class That desactivate an wifi AP"

    complete_rewrite = False
    template_path_str = '/opt/cd60/python/resources/switchports.jinja'
    template_switch_path_str = '/opt/cd60/python/resources/switch.jinja'
    template_index_path_str = '/opt/cd60/python/resources/index.jinja'
    dst_dir = '/root/Switchs-infos/source'

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--path', help='the save path')

        self._add_mandatory_arg('path')

    def before_process(self):
        pass

    def after_process(self):
        # switchs pages
        template_switch_path = Path(self.template_switch_path_str)
        template_switch_str = template_switch_path.read_text()
        template_switch = Template(template_switch_str)

        # Site page
        template_path = Path(self.template_path_str)
        template_str = template_path.read_text()
        template = Template(template_str)

        for site_name in self._sharedResult:
            switchs = self._sharedResult[site_name]
            if self.complete_rewrite:
                rendered = template.render(datetime=str(datetime.datetime.now()), site_name=site_name, switchs=switchs)
                # print(switch['interfaces'])
                # print(self._sharedResult[site_name][0]['interfaces'])
                dest_path = Path('{}/{}.rst'.format(self.dst_dir, site_name))
                dest_path.write_text(rendered)
            for switch in switchs:
                rendered_switch = template_switch.render(datetime=str(datetime.datetime.now()), switch=switch)
                dest_path = Path('{}/{}_{}.rst'.format(self.dst_dir, site_name, switch['ip']))
                dest_path.write_text(rendered_switch)

        # render index
        if self.complete_rewrite:
            template_index_path = Path(self.template_index_path_str)
            template_index_str = template_index_path.read_text()
            template = Template(template_index_str)
            rendered_index = template.render(sites=self._sharedResult.keys())
            dest_path = Path('{}/index.rst'.format(self.dst_dir))
            dest_path.write_text(rendered_index)

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            switch.log_error('BACKUP FAILED')
            print('impossible de se connecter')
        else:
            result = switch.execute(
                'save_conf_file',
                folder="{}/{}".format(args['path'], args['site']),
                add_timestamp=False)

            # switch.execute('gen_switch_page')

            interfaces = switch.get_fact('int')
            if interfaces:
                if switch.site not in self._sharedResult:
                    self._sharedResult[switch.site] = []

                self._sharedResult[switch.site].append({'hostname': switch.hostname,
                                                        'ip': switch.IP,
                                                        'interfaces': switch.get_fact('int')})

            switch.logout()

            if not result:
                switch.log_error('BACKUP FAILED')


save_conf_File = SaveSwitchConf('Save the running config', sys.argv[1:])
save_conf_File.process()
