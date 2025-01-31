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


## This script read events from ARCS event-mode preNexus file
## and write mslice spe and phx files


from ipdpE import Application as base

class Application( base ):

    class Inventory( base.Inventory  ):

        import pyre.inventory as pinv
        mslicefileprefix = pinv.str( 'mslice-prefix', default = 'mslice' )
        mslicefileprefix.meta['tip'] = 'prefix of mslice output files'
        pass # end of Inventory


    def _defaults(self):
        base._defaults(self)
        self.inventory.h5filename = 'IpdpE.h5'
        return


    def main(self):
        prefix = self.inventory.mslicefileprefix
        spef = '%s.spe' % prefix
        phxf = '%s.phx' % prefix
        if os.path.exists( spef ) or os.path.exists( phxf ):
            raise IOError , "%r or %r already exist" % (spef, phxf)
        
        base.main(self)

        if mpiRank() == 0:
            from histogram.hdf import load
            h = load( self.inventory.h5filename, 'I(pdpE)' )

            pixel_resolution = self.inventory.pixel_step
            if pixel_resolution == 1:
                from arcseventdata import getinstrumentinfo
                infos = getinstrumentinfo(self.inventory.ARCSxml)
                phi_p = infos['phis']
                psi_p = infos['psis']
                dphi_p = infos['dphis']
                dpsi_p = infos['dpsis']
            else:
                # find out info about combined pixels
                from arcseventdata.combinepixels import combinepixels
                pixelaxis = h.axisFromName('pixelID')
                ARCSxml = self.inventory.ARCSxml
                phi_p, psi_p, dist_p, solidangle_p, dphi_p, dpsi_p \
                       = combinepixels(ARCSxml, pixelaxis, pixel_resolution)

                # pick out the requested packs
                pack_params = self.inventory.pack_params
                phi_p = phi_p[pack_params, (), ()]
                psi_p = psi_p[pack_params, (), ()]
                dphi_p = dphi_p[pack_params, (), ()]
                dpsi_p = dpsi_p[pack_params, (), ()]

            # is this still necessary?
            import numpy
            phi_p.I[:] = numpy.nan_to_num( phi_p.I )
            psi_p.I[:] = numpy.nan_to_num( psi_p.I )
            
            #convert to mslice file
            import arcseventdata
            arcseventdata.write_mslice_files( h, phi_p, psi_p, dphi_p, dpsi_p, spef, phxf )
            
        return

    pass # end of Application



def mpiRank():
    try:
        import mpi
        world = mpi.world()
        mpiRank = world.rank; mpiSize = world.size
        if mpiSize < 1:
            mpiSize = 1
            parallel = False
        else:
            parallel = True
    except:
        mpiRank = 0
        mpiSize = 1
        parallel = False
        pass
    return mpiRank


import os

def main():
    Application('events2mslicefiles').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    #journal.debug('events2mslicefiles').activate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
