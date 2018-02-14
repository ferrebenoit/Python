'''
Created on 1 févr. 2018

@author: FERREB
'''
import pytest


from switchhandler.device.device_exception import CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.vendor.allied.switch_allied import SwitchAllied


@pytest.fixture(autouse=True, scope="module")
def switch():
    return SwitchAllied('127.0.0.1', dryrun=True)


def test_write(switch):
    assert switch.execute('write')


def test_int_vlan(switch):
    assert switch.execute('int_vlan', id='80')


@pytest.mark.xfail(raises=CommandParameterNotFoundException)
def test_int_vlan_exception(switch):
    assert switch.execute('int_vlan')


@pytest.mark.xfail(raises=CommandParameterNotFoundException)
def test_acl_add_row(switch):
    assert switch.execute('acl_add_row')
