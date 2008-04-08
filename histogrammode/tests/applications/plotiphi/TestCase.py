#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                     California Institute of Technology
#                   (C) Copyright 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os

import unittest

class Tests(unittest.TestCase):

    def __init__(self, *args, **kwds):
        unittest.TestCase.__init__(self, *args, **kwds)
        from lrmecs_testutils import checkDataFiles
        checkDataFiles()

        from pharos_testutils import getDataFiles
        getDataFiles()
        return
    

    def test1(self):
        "plotiphi - lrmecs"
        cmd = '''plotiphi.py -instrument=lrmecs -lrmecs.filename="../../ins-data/Lrmecs/4849" '''
        self._test(cmd)
        return


    def test2(self):
        "plotiphi - pharos"
        cmd ='plotiphi.py -instrument=pharos -pharos.instrument-definition-filename=../../ins-data/Pharos/PharosDefinitions.txt -pharos.data-filename=../../ins-data/Pharos/Pharos_342.nx.h5'
        self._test(cmd)
        return

    def test3(self):
        "plotiphi - pharos 3322"
        cmd ='plotiphi.py -instrument=pharos -pharos.instrument-definition-filename=../../ins-data/Pharos/PharosDefinitions.txt -pharos.data-filename=../../ins-data/Pharos/Pharos_3322.nx.h5'
        self._test(cmd)
        return

    def _test(self, cmd):
        import os
        if os.system( cmd ): raise "Failed to execute %s" % cmd
        return

    pass 
        

def pysuite():
    suite1 = unittest.makeSuite(Tests)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id: PharosReductionLight.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
