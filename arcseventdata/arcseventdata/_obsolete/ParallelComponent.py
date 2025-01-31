#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## Supports for parallel computing


import journal
info = journal.info( 'mpi' )


class ParallelComponent(object):

    '''Base class for operators that can be parallelized.
    '''

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

    info.log( "rank %d of %d" % (mpiRank, mpiSize ) )

    def runMasterNodeOnly(self, channel, func, *args, **kwds):
        if self.parallel:
            if self.mpiRank == 0:
                ret = func( *args, **kwds )
                for i in range( 1, self.mpiSize ):
                    self.mpiSend( ret, i, channel )
                    continue
                pass
            else:
                ret = self.mpiReceive( 0, channel )
                pass
            return ret
        return func(*args, **kwds)

    
    def mpiSend( self, obj, peer, tag):
        s = pickle.dumps( obj )
        return self.mpiSendStr( s )


    def mpiReceive(self, peer, tag):
        s = self.mpiReceiveStr( peer, tag )
        obj = pickle.loads( s )
        return obj


    def mpiSendStr( self, s, peer, tag):
        world = self.world
        port = world.port(peer=peer, tag=tag)
        msg = "Machine %s: sending string of length %d to peer %s with tag %s" % (
            self.mpiRank, len(s), peer, tag) 
        port.send(s)
        msg = "Machine %s: sent string of length %d to peer %s with tag %s" % (
            self.mpiRank, len(s), peer, tag) 
        info.log( msg )
        return


    def mpiReceiveStr(self, peer, tag):
        world = self.world
        port = world.port(peer=peer, tag=tag)
        s = port.receive()
        msg = "Machine %s: received string of length %d from peer %s with tag %s" % (
            self.mpiRank, len(s), peer, tag)
        info.log( msg )
        return s

    pass # end of ParallelComponent

import cPickle as pickle
    


# version
__id__ = "$Id$"

# End of file 
