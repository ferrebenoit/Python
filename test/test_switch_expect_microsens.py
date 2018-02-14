'''
Created on 1 févr. 2018

@author: FERREB
'''
import pytest


from switchhandler.device.device_exception import CommandParameterNotFoundException
from switchhandler.device.protocol.expect.switch.vendor.microsens.switch_microsens import SwitchMicrosens


@pytest.fixture(autouse=True, scope="module")
def switch():
    return SwitchMicrosens('127.0.0.1', dryrun=True)


def test_write(switch):
    assert switch.execute('write')


@pytest.mark.xfail(raises=CommandParameterNotFoundException)
def test_create_vlan_exception(switch):
    assert switch.execute('create_vlan')
