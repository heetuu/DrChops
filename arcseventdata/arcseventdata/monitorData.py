#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


#tofunit = '0.1*microsecond'
tofunit = 'microsecond'

def readHistogram( filename ):
    s = open(filename).read()
    import numpy as N
    I = N.fromstring( s, 'u4' )
    n = len(I)
    tof = N.arange( 0.5, n+0.4, 1. )
    import histogram as H
    Itof = H.histogram(
        'I(tof)',
        [
        ('tof', tof, tofunit),
        ],
        data = I, errors = I )
    return Itof


# version
__id__ = "$Id$"

#  End of file 
