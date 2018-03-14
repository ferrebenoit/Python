'''
Created on 4 fÃ©vr. 2018

@author: ferre
'''
from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.cisco import CATEGORY_CISCO
from switchhandler.utils.decorator.class_register import registered_class

import re


@registered_class(category=CATEGORY_CISCO, registered_name="fact_conf")
class FactConf(FactBase):
    '''
    retourne un dict avec deux entrées :
        {'raw': 'raw configuration', 'sanitized': 'sanitized configuration'}    
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def define_argument(self):
        pass

    def sanitize(self, confStr):
        confStr = re.sub(r'show running-config.*\s*\n',
                         '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'Building configuration...\s*\n',
                         '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'Current configuration .*\s*\n',
                         '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'! Last configuration change at .*\s*\n',
                         '', confStr, flags=re.MULTILINE)
        confStr = re.sub(r'! NVRAM config last updated at .*\s*\n',
                         '', confStr, flags=re.MULTILINE)
        confStr = re.sub(
            r'! No configuration change since last restart\s*\n', '', confStr, flags=re.MULTILINE)

        confStr = re.sub(
            r'ntp clock-period [0-9]*\s*\n', '', confStr, flags=re.MULTILINE)

        return confStr

    def do_run(self):
        self.switch.execute('end')

        self.switch.send_line('terminal length 0')
        self.switch.expect_prompt()

        # self.switch.send_line('show running-config view full')
        self.switch.send_line('show running-config')
        self.switch.expect_prompt()

        return {'raw': self.switch.before(), 'sanitized': self.sanitize(self.switch.before())}
