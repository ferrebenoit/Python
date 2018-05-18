'''
Created on 4 févr. 2018

@author: ferre
'''
import re

from switchhandler.device.executable.fact.fact_base import FactBase
from switchhandler.device.protocol.expect.switch.vendor.allied import CATEGORY_ALLIED
from switchhandler.utils.decorator.class_register import registered_class


@registered_class(category=CATEGORY_ALLIED, registered_name="fact_version")
class FactConfig(FactBase):
    '''
    retourne l'adresse mac pour la licence :
        "MYKONOS-ABIS-19156#show system mac license

        MAC address for licensing:

        0000.cd29.ed4d"

        "0000.cd29.ed4d"

    '''

    __REGEX = r"(^(Current software   : (?P<software>.*))|^(Software version   : (?P<softwareversion>.*))|^(Build date         : (?P<builddate>.*))|^((Base|Chassis)\s*\d*\s*(?P<model>.*?\s{2})))"

    def parse(self, conf):
        return re.finditer(self.__REGEX, conf, re.MULTILINE)

    def define_argument(self):
        pass

    def sanitize(self, confStr):
        confStr = re.sub(r'\r',
                         '', confStr, flags=re.MULTILINE)

        confStr = "\n".join(confStr.split('\n')[1:])

        return confStr

    def do_run(self):
        result = {}

        conf = self.switch.get_fact('system')

        res_system = self.parse(conf['sanitized'])
        for res in res_system:
            tmp = res.groupdict().get('software')
            if tmp is not None:
                result['software'] = tmp
            tmp = res.groupdict().get('softwareversion')
            if tmp is not None:
                result['softwareversion'] = tmp
            tmp = res.groupdict().get('builddate')
            if tmp is not None:
                result['builddate'] = tmp
            tmp = res.groupdict().get('model')
            if tmp is not None:
                result['model'] = tmp

        return result
