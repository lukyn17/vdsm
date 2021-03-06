#
# Copyright 2012 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
#
# Refer to the README and COPYING files for full details of the license
#

import os
from testrunner import VdsmTestCase as TestCaseBase

from vdsm import netinfo
from monkeypatch import MonkeyPatch

# speeds defined in ethtool
ETHTOOL_SPEEDS = set([10, 100, 1000, 2500, 10000])


class TestNetinfo(TestCaseBase):

    def testNetmaskConversions(self):
        path = os.path.join(os.path.dirname(__file__), "netmaskconversions")
        with open(path) as netmaskFile:
            for line in netmaskFile:
                if line.startswith('#'):
                    continue
                bitmask, address = [value.strip() for value in line.split()]
                self.assertEqual(netinfo.prefix2netmask(int(bitmask)),
                                 address)
        self.assertRaises(ValueError, netinfo.prefix2netmask, -1)
        self.assertRaises(ValueError, netinfo.prefix2netmask, 33)

    def testSpeedInvalidNic(self):
        nicName = 'DUMMYNICDEVNAME'
        self.assertTrue(nicName not in netinfo.nics())
        s = netinfo.speed(nicName)
        self.assertEqual(s, 0)

    def testSpeedInRange(self):
        for d in netinfo.nics():
            s = netinfo.speed(d)
            self.assertFalse(s < 0)
            self.assertTrue(s in ETHTOOL_SPEEDS or s == 0)

    def testIntToAddress(self):
        num = [0, 1, 16777344, 16777408, 4294967295]
        ip = ["0.0.0.0", "1.0.0.0", "128.0.0.1",
              "192.0.0.1", "255.255.255.255"]
        for n, addr in zip(num, ip):
            self.assertEqual(addr, netinfo.intToAddress(n))

    def testIPv6StrToAddress(self):
        inputs = [
            '00000000000000000000000000000000',
            '00000000000000000000000000000001',
            '20010db8000000000001000000000002',
            '20010db8aaaabbbbccccddddeeeeffff',
            'fe80000000000000be305bbffec58446']
        ip = [
            '::',
            '::1',
            '2001:db8::1:0:0:2',
            '2001:db8:aaaa:bbbb:cccc:dddd:eeee:ffff',
            'fe80::be30:5bbf:fec5:8446']
        for s, addr in zip(inputs, ip):
            self.assertEqual(addr, netinfo.ipv6StrToAddress(s))

    @MonkeyPatch(netinfo, 'networks', lambda: {'fake': {'bridged': True}})
    def testGetNonExistantBridgeInfo(self):
        # Getting info of non existing bridge should not raise an exception,
        # just log a traceback. If it raises an exception the test will fail as
        # it should.
        netinfo.get()

    def testMatchNicName(self):
        self.assertTrue(netinfo._match_nic_name('test1', ['test0', 'test1']))
