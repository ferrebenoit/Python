'''
Created on 4 févr. 2018

@author: ferre
'''
import re

from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="fact_mac_licence")
class FactConfig(FactBase):
    '''
    retourne l'adresse mac pour la licence :
        "MYKONOS-ABIS-19156#show system mac license

        MAC address for licensing:

        0000.cd29.ed4d"

        "0000.cd29.ed4d"

    '''

    __REGEX = r"([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})"

    def parse(self, conf):
        match_obj = re.search(self.__REGEX, conf, re.MULTILINE)
        if match_obj is not None:
            return match_obj.group(0)
        else:
            return None

    def define_argument(self):
        pass

    def sanitize(self, confStr):
        confStr = re.sub(r'\r',
                         '', confStr, flags=re.MULTILINE)

        confStr = "\n".join(confStr.split('\n')[1:])

        return confStr

    def do_run(self):
        # change to sh mac addresstable | inc CPU
        self.switch.send_line('show system mac license')
        self.switch.expect_prompt()

        return self.parse(self.switch.before())
