#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

from unittest import TestCase
class events2IQQQE_TestCase(TestCase):


    def test1(self):
        'events2IQQQE: default intensity type (int)'
        import arcseventdata.arcseventdata as aa
        events = aa.readevents( "events.dat", 10 )
        import numpy
        I = numpy.zeros( 20*20*20*10, 'i' )
        Ei = 60.
        
        pixelPositions = aa.readpixelpositions( 'pixelID2position.bin' )
        
        aa.events2IQQQE_numpyarray(
            events, 10,
            -10, 10, 1.,
            -10, 10, 1.,
            -10, 10, 1.,
            -50, 50, 10. ,
            I,
            Ei, pixelPositions)
        return
    

    def test2(self):
        'events2IQQQE: intensity type is "double"'
        import arcseventdata.arcseventdata as aa
        events = aa.readevents( "events.dat", 10 )
        import numpy
        I = numpy.zeros( 20*20*20*10, 'double' )
        Ei = 60.
        
        pixelPositions = aa.readpixelpositions( 'pixelID2position.bin' )
        ntotpixels = 115*8*128
        tofUnit = 1e-7
        mod2sample = 13.6
        toffset = 0
        intensity_npy_typecode = numpy.dtype('double').num
        
        aa.events2IQQQE_numpyarray(
            events, 10,
            -10, 10, 1.,
            -10, 10, 1.,
            -10, 10, 1.,
            -50, 50, 10. ,
            I,
            Ei, pixelPositions,
            ntotpixels, tofUnit,
            mod2sample, toffset, intensity_npy_typecode,
            )
        return
    
    pass # end of events2IQQQE_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2IQQQE_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
