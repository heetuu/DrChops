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


## obtain histograms about pixel h(pack, tube, pixel)
##   - phi. scattering angle
##   - psi. azimuthal angle
##   - dist. distance from sample to pixel.


import numpy as N
import histogram
#from numpy import sqrt, sum, arccos, arctan2, array, pi


def getpixelinfo(
    positions, detaxes, instrument):

    npacks, ndetsperpack, npixelsperdet = [axis.size() for axis in detaxes]

    save = positions.shape
    positions.shape = npacks, ndetsperpack, npixelsperdet, 3

    from getpixelsizes import getpixelsizes
    radii, heights = getpixelsizes(
        instrument, npacks, ndetsperpack, npixelsperdet)
    
    dists, phis, psis, solidangles, dphis, dpsis = \
           calcpixelinfo(positions, radii, heights)

    positions.shape = save

    # scattering angles
    phi_p = histogram.histogram('phi_pdp', detaxes )
    phi_p.I[:] = phis
    
    psi_p = histogram.histogram('psi_pdp', detaxes )
    psi_p.I[:] = psis
    
    # distances
    dist_p = histogram.histogram('dist_pdp', detaxes )
    dist_p.I[:] = dists

    # quantities related to the sizes of pixels
    # solid angles
    solidangle_p = histogram.histogram('solidangle_pdp', detaxes)
    solidangle_p.I[:] = solidangles

    # dphi
    dphi_p = histogram.histogram('dphi_pdp', detaxes )
    dphi_p.I[:] = dphis

    # dpsi
    dpsi_p = histogram.histogram('dpsi_pdp', detaxes )
    dpsi_p.I[:] = dpsis
    
    return phi_p, psi_p, dist_p, solidangle_p, dphi_p, dpsi_p



def calcpixelinfo(positions, radii, heights):
    xs = positions[:,:,:,0]; ys = positions[:,:,:,1]; zs = positions[:,:,:,2]
    dists = N.sqrt(xs**2+ys**2+zs**2)

    # scattering angles
    phis = phi(xs, dists) * (180/N.pi)
    psis = psi(zs, ys) * (180/N.pi)
    
    # quantities related to the sizes of pixels
    # solid angles
    solidangles = solidangle2(xs,ys,zs,radii,heights)

    # dphi
    dphis = dphi(xs, ys, zs, dists, radii, heights) * (180/N.pi)

    # dpsi
    dpsis = dpsi(xs, ys, zs, dists, radii, heights) * (180/N.pi)
    
    return dists, phis, psis, solidangles, dphis, dpsis



# calculators

#phi is the angle between the scattered neutron and the incident beam
# note: assuming we use "Instrument scientist" coord system
# z: up (opposite of gravity)
# x: neutron beam downstream
def phi(x, dist):
    return N.arccos(x/dist)


def psi(z, y):
    return N.arctan2(z,y)


def solidangle2(x,y,z,radius,height):
    '''solid angle of a pixel at position(x,y,z)
    tube is assumed to be vertical.
    radius: radius of tube
    height: height of pixel
    '''
    r2 = x*x + y*y + z*z
    cost = (1 - z*z/r2)**0.5
    area = 2*radius*height*cost
    return solidangle1(area, r2)


def solidangle1(area, radius_square):
    '''basic formula to calculate solid angle
    sa = area/radius**2
    '''
    return area/radius_square



def dphi(x,y,z,r, radius, height):
    # the vector along the direction of dphi
    p1 = r**2/x -x
    p2 = -y
    p3 = -z
    
    xis0 = x<0.01
    p1[xis0]=1
    p2[xis0]=0
    p3[xis0]=0

    #normalize
    tmp = N.sqrt(p1**2 + p2**2 + p3**2)
    p1/=tmp; p2/=tmp; p3/=tmp
    del tmp

    # horizontal span of pixel
    rxy = N.sqrt(x**2+y**2)
    h1 = -2*radius*y/rxy
    h2 = 2*radius*x/rxy
    h3 = 0

    # vertical span of pixel
    v1=v2=0
    v3 = height

    # dot products. ignore zeros
    dphi1 = N.abs(p1*h1+p2*h2)
    dphi2 = N.abs(p3*v3)

    return (dphi1+dphi2)/r


def dpsi(x,y,z,r, radius, height):
    # the vector along the direction of dpsi
    p1 = 0
    p2 = z
    p3 = -y
    
    #normalize
    tmp = N.sqrt(p2**2 + p3**2)
    p2/=tmp; p3/=tmp
    iszero = tmp<0.01
    p2[iszero] = 1; p3[iszero] = 0
    del tmp

    # horizontal span of pixel
    rxy = N.sqrt(x**2+y**2)
    #h1 = -2*radius*y/rxy
    h2 = 2*radius*x/rxy
    h3 = 0

    # vertical span of pixel
    v1=v2=0
    v3 = height

    # dot products. ignore zeros
    dpsi1 = N.abs(p2*h2)
    dpsi2 = N.abs(p3*v3)

    ret = (dpsi1+dpsi2)/r
    ret[iszero] = maxdpsi
    ret[ret>maxdpsi] = maxdpsi
    return ret


def dphi_impl1(z, r, radius, height):
    cost = N.sqrt(1-z*z/r**2)
    dphi1 = height * cost / r
    dphi2 = 2*radius / r
    dphi = N.sqrt(dphi1**2 + dphi2**2)
    return dphi


maxdpsi = N.pi/2 # quite random
def dpsi_impl2(y, z, radius, height):
    r2 = y**2 + z**2
    smallr2 = r2 < 1.e-2
    r2[smallr2] = 1.
    d2 = (2*radius)**2 + height**2
    dpsi = N.sqrt(d2/r2)
    dpsi[dpsi>maxdpsi] = maxdpsi
    dpsi[smallr2] = maxdpsi
    return dpsi




#tests
def test_dphi():
    n = 5
    x=y=z = N.ones(5) * 1.
    r = N.ones(5) * 3.
    radius = N.ones(5) * 0.02
    height = N.ones(5) * 0.01
    print dphi(x,y,z,r,radius,height)

def test_dpsi():
    n = 5
    x = y = z = N.ones(5) * 1.
    r = N.ones(5) * 3.
    radius = N.ones(5) * 0.02
    height = N.ones(5) * 0.01
    print dpsi(x,y,z,r, radius,height)


def test_dphi_impl1():
    n = 5
    z = N.ones(5) * 1.
    r = N.ones(5) * 3.
    radius = N.ones(5) * 0.02
    height = N.ones(5) * 0.01
    print dphi_impl1(z,r,radius,height)

def test_dpsi_impl1():
    n = 5
    y = z = N.ones(5) * 1.
    radius = N.ones(5) * 0.02
    height = N.ones(5) * 0.01
    print dpsi_impl1(y,z,radius,height)


def main():
    test_dphi()
    test_dpsi()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

#  End of file 
