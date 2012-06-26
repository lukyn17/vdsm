#
# Copyright 2012 IBM, Inc.
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

import configNetwork
from testrunner import VdsmTestCase as TestCaseBase


class TestconfigNetwork(TestCaseBase):

    def testNicSort(self):
        nics = {'nics_init': ('p33p1', 'eth1', 'lan0', 'em0', 'p331',
                              'Lan1', 'eth0', 'em1', 'p33p2', 'p33p10'),
                'nics_expected': ('Lan1', 'em0', 'em1', 'eth0', 'eth1',
                                  'lan0', 'p33p1', 'p33p10', 'p33p2', 'p331')}

        nics_res = configNetwork.nicSort(nics['nics_init'])
        self.assertEqual(nics['nics_expected'], tuple(nics_res))

    def testIsBridgeNameValid(self):
        invalidBrName = ('-abc', 'abcdefghijklmnop', 'a:b', 'a.b')
        for i in invalidBrName:
            res = configNetwork.isBridgeNameValid(i)
            self.assertEqual(0, res)