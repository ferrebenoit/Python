'''
Created on 4 févr. 2018

@author: ferre
'''
import re

from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="fact_system")
class FactConfig(FactBase):
    '''
    show system
    retourne un dict avec deux entrées :
        {'raw': 'raw configuration', 'sanitized': 'sanitized configuration'}
    '''

    def define_argument(self):
        pass

    def sanitize(self, confStr):
        confStr = re.sub(r'\r',
                         '', confStr, flags=re.MULTILINE)

        confStr = "\n".join(confStr.split('\n')[1:])

        return confStr

    def do_run(self):
        self.switch.send_line('terminal length 0')
        self.switch.expect_prompt()

        self.switch.send_line('show system')
        self.switch.expect_prompt()

        return {'raw': self.switch.before(), 'sanitized': self.sanitize(self.switch.before())}
