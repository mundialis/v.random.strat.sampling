"""
Name:       v.random.strat.sampling test
Purpose:    Tests v.random.strat.sampling input parsing.
            Uses NC Basic data set.

Author:     Markus Neteler
Copyright:  (C) 2020 Markus Neteler, mundialis, and the GRASS Development Team
Licence:    This program is free software under the GNU General Public
            License (>=v2). Read the file COPYING that comes with GRASS
            for details.
"""

import os

from grass.gunittest.case import TestCase
from grass.gunittest.main import test

class Testdivide(TestCase):
    invect = 'zipcodes'
    outtrain = 'training'

    @classmethod
    def setUpClass(cls):
        """Ensures expected computational region and generated data"""
        cls.use_temp_region()
        cls.runModule('g.region', vector=cls.invect)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary region and generated data"""
        cls.del_temp_region()

    def test_points(self):
        """Test divide points"""
        # note: numeric ZIPNUM column works
        self.assertModule('v.random.strat.sampling', input=self.invect, column='NAME',
                          output=self.outtrain, npoints=2)
        self.assertVectorExists(self.outtrain)
        # there are 19 names in the table: 19 * unclear = 78
        topology = dict(points=78)
        self.assertVectorFitsTopoInfo(self.outtrain, topology)

if __name__ == '__main__':
    test()
