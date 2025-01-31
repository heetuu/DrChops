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
class events2IQE_TestCase(TestCase):


    def test1(self):
        'events2IQE'
        from  arcseventdata.events2IQE import  events2IQE
        import arcseventdata
        events, n = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        IQE = H.histogram(
            'I(Q, E)',
            [
            ('Q', H.arange(0,10, 0.1)),
            ('energy', H.arange(-50,50,1)),
            ],
            data_type = 'int')
        
        pixelpositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        Ei = 60
        
        events2IQE( events, n, IQE, Ei, pixelpositions )
        return
    
    pass # end of events2IQE_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2IQE_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2IQE_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
