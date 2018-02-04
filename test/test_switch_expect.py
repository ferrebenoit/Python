'''
Created on 1 févr. 2018

@author: FERREB
'''
import pytest


from switchhandler.device.device_exception import CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.vendor.cisco.switch_cisco import SwitchCisco


@pytest.fixture(autouse=True, scope="module")
def switch_cisco():
    return SwitchCisco('127.0.0.1', dryrun=True)


def test_write(switch_cisco):
    assert switch_cisco.execute('write')


def test_int_vlan(switch_cisco):
    assert switch_cisco.execute('int_vlan', id='80')


@pytest.mark.xfail(raises=CommandParameterNotFoundException)
def test_int_vlan_exception(switch_cisco):
    assert switch_cisco.execute('int_vlan')
