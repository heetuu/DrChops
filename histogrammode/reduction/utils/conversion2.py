#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from math import sqrt


neutron_mass = 1.6749286e-27;
mN = neutron_mass;

electron_charge = 1.60217733e-19;
e = electron_charge;

boltzman_constant = 1.3806504e-23;
kB = boltzman_constant;

hbar = 1.054571628e-34;

K2V = hbar/mN*1e10
V2K = 1./K2V
#V2K = 1.58801E-3 # Convert v[m/s] to k[1/AA]
SE2V = sqrt(2e-3*e/mN)
# SE2V = 437.3949	   #/* Convert sqrt(E)[meV] to v[m/s] */
VS2E = mN/(2e-3*e)
#VS2E = 5.227e-6	   #/* Convert (v[m/s])**2 to E[meV] */
def v2k(vel):
    return V2K * vel
def e2v(energy):
    from numpy import sqrt
    return sqrt(energy)*SE2V
def e2k(energy):
    return v2k( e2v( energy) )
def k2v(k):
    return K2V * k
def v2e(v):
    return v*v*VS2E
def k2e(k):
    return v2e( k2v( k) )


# version
__id__ = "$Id$"

# End of file 

