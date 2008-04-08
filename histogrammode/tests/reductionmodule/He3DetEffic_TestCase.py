#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.reduction import *

import unittestX as ut


class He3DetEffic_TestCase(ut.TestCase):

    def test(self):
        "He3LPSDEffic"
        eff = He3LPSDEffic( 6, 10., 1.27, 200 )
        return
    
    def test1(self):
        "He3LPSDEffic - call with one energy value"
        eff = He3LPSDEffic( 6, 10., 1.27, 200 )
        print "pressure=10, radius=1.27, n=2000"
        e = 47.043
        print "efficiency at %s is %s" % (
            e, He3LPSDEffic_callSingle( eff, 6, e )
            )
        return
    
    def test2(self):
        "He3LPSDEffic - call with one stdVector instance"
        eff = He3LPSDEffic( 6, 10., 1.27, 200 )
        print "pressure=10, radius=1.27, n=2000"
        
        from stdVector import vector
        energies = vector( 6, range(40,60,2) )

        print "energies: %s" % ( energies.asList(), )
        efficiencies = vector( 6, 10 )
        He3LPSDEffic_callVector( eff, 6, energies.handle(), efficiencies.handle() )
        print "efficiencies: %s" % efficiencies.asList()
        return
    
    pass # end of He3DetEffic_TestCase

    
def pysuite():
    suite1 = ut.makeSuite(He3DetEffic_TestCase)
    return ut.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('reduction.Universal1DRebinner').activate()
    
    pytests = pysuite()
    alltests = ut.TestSuite( (pytests, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: He3DetEffic_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
