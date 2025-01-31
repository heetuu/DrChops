#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

'''
To run this test in parallel, you can run

 $ mpirun -n 8 `which mpipython.exe` ReduceVanadiumData_TestCase.py

'''


try:
    import mpi
    mpiRank = mpi.world().rank
    
except ImportError:
    mpiRank = 0


import unittest

from unittestX import TestCase as base
class TestCase(base):

    def test(self):
        indir = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_297' 
        calibration_constants_output = 'calibration.h5'
        mask_output = 'mask.h5'
        outputs = [
            calibration_constants_output,
            mask_output,
            ]
        
        import os
        assert os.path.exists( indir  )
        for output in outputs:
            if os.path.exists( output ): os.remove( output )
            continue
        
        from reduction.core.ARCS.ReduceVanadiumData import reduce
        reduced = reduce(
            indir,
            Ei = 98.58,
            emission_time = 0,
            E_params = (-65,65,1.)
            )
        
        if mpiRank !=0: return

        calibration = reduced['calibration']
        mask = reduced['mask']
        
        from histogram.hdf import dump
        dump( calibration, calibration_constants_output, '/', 'c' )
        dump( mask, mask_output, '/', 'c' )

        import arcseventdata as aed
        v = aed.detectorview( calibration )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( v, min = 0, max = 100 )
        return

    pass # end of TestCase


import reduction.units as units


import unittest

def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    #journal.debug('reduction.core.getPixelInfo' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
