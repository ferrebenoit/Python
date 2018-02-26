'''
Created on 23 févr. 2018

@author: ferre
'''
#from pysnmp.hlapi import *
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.auth import CommunityData
from pysnmp.hlapi.context import ContextData
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.hlapi.asyncore.sync.cmdgen import nextCmd, getCmd
from pysnmp.hlapi.asyncore.transport import UdpTransportTarget
from pysnmp.smi.view import MibViewController


def t1():

    se = SnmpEngine()
    mvc = se.getUserContext('mibViewController')
    if not mvc:
        mvc = MibViewController(se.getMibBuilder())
    #
    # # 1.3.6.1.2.1.2.2 ('iso', 'org', 'dod', 'internet', 'mgmt', 'mib-2', 'interfaces', 'ifTable')
    oid_iftable = ObjectIdentity('IF-MIB', 'ifTable')
    oid_iftable.resolveWithMib(mvc)

    print("Root oid")
    print(oid_iftable.getOid())
    print(oid_iftable.getLabel())
    print(oid_iftable.getMibNode())
    print(oid_iftable.getMibSymbol())

    g = nextCmd(SnmpEngine(), CommunityData('public', mpModel=1), UdpTransportTarget(
        ('demo.snmplabs.com', 161)), ContextData(), ObjectType(ObjectIdentity('IF-MIB', 'ifTable')), lexicographicMode=False)

    print("\nWalking table")
    data = []
    dIndex = {}

    for errorIndication, errorStatus, errorIndex, varBinds in g:

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

                oid = varBind[0]
                value = varBind[1]

                label = oid.getLabel()
                print("Label:", label)
                print("Mib Symbol:", oid.getMibSymbol())
                key = str(oid.getMibSymbol()[-1][0])

                if not key in dIndex:
                    dIndex[key] = {}
                    data.append(dIndex[key])

                dIndex[key][label[-1]] = str(value.prettyPrint())

    print("\nPrinting items")
    for ind, item in enumerate(data):
        print("Item %s" % (str(ind + 1), ))
        for key, value in item.items():
            print(" %s: %s" % (key, value))


def table():
    item = 0
    for errorIndication, \
        errorStatus, \
        errorIndex, \
        varBinds in nextCmd(SnmpEngine(),
                            CommunityData('public', mpModel=0),
                            UdpTransportTarget(('demo.snmplabs.com', 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifType')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifMtu')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifType')),
                            ObjectType(ObjectIdentity(
                                'IF-MIB', 'ifPhysAddress')),
                            lexicographicMode=False):

        print("Item ", item)
        item += 1

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )
            )
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))


def snmpwalk():
    # g = nextCmd(SnmpEngine(), CommunityData('public', mpModel=1), UdpTransportTarget(
    #    ('demo.snmplabs.com', 161)), ContextData(), ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID', 0)))
    g = nextCmd(SnmpEngine(), CommunityData('public', mpModel=1), UdpTransportTarget(
        ('demo.snmplabs.com', 161)), ContextData(), ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2')))

    for errorIndication, errorStatus, errorIndex, varBinds in g:

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
                print(' = '.join([x.prettyPrint() for x in varBind]))


def get():
    data = (
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    g = getCmd(SnmpEngine(), CommunityData('public', mpModel=0), UdpTransportTarget(
        ('demo.snmplabs.com', 161)), ContextData(), *data)

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
            print(' = '.join([x.prettyPrint() for x in varBind]))


t1()
