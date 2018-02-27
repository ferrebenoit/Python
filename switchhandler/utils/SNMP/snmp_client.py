'''
Created on 27 févr. 2018

@author: ferre
'''
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.auth import CommunityData
from pysnmp.hlapi.context import ContextData
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.hlapi.asyncore.sync.cmdgen import nextCmd, getCmd
from pysnmp.hlapi.asyncore.transport import UdpTransportTarget
from pysnmp.smi.view import MibViewController


class SNMPVariable(object):
    pass


class SNMPClient(object):
    '''
    classdocs
    '''

    def __init__(self, ip, community_public, community_private, snmp_version=2):
        '''
        Constructor
        '''
        self.ip = ip
        self.snmp_version = snmp_version
        self.community_public = community_public
        self.community_private = community_private

        self.__udp_transport()
        self.__community_data()

    def __community_data(self):
        self.community_data_public = CommunityData(
            self.community_public, mpModel=0)
        self.community_data_private = CommunityData(
            self.community_private, mpModel=0)

    def __udp_transport(self):
        self.udp_transport = UdpTransportTarget((self.ip, 161))

    def login(self, login, password):
        pass

    def get_value(self, **kwargs):
        result = {}
        data = (
            ObjectType(ObjectIdentity(kwargs['mib'], kwargs['value'], 0)),
            # ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        )

        g = getCmd(SnmpEngine(), self.community_data_public,
                   self.udp_transport, ContextData(), *data)

        errorIndication, errorStatus, errorIndex, varBinds = next(g)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )

            )
        else:
            for varBind in varBinds:
                print(varBind)
                result[varBind[0].prettyPrint()] = varBind[1].prettyPrint()

            return result

    def set_value(self, **kwargs):
        pass

    def get_table(self, **kwargs):
        pass


snmp = SNMPClient('demo.snmplabs.com', 'public', 'public')
print(snmp.get_value(mib='SNMPv2-MIB', value='sysLocation'))
