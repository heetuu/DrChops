#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.pyre.preprocessors.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as Solver

from pyre.applications.Script import Script


import unittest


from unittestX import TestCase
class IncidentEnergySolver_UseMonitors_TestCase(TestCase):

    def test(self):
        """
        """
        testFacility = self

        from TestRun_for_IncidentEnergySolverUsingMonitors import Run, ei

        #create a pyre script to run the test
        class Test(Script):

            class Inventory(Script.Inventory):
                import pyre.inventory as inv
                eiSolver = inv.facility("eiSolver", factory = Solver)
                pass # end of Inventory

            def main(self):
                run = Run()
                es = self.eiSolver
                es.setInput('run', run)
                eiSolved = es.getOutput('Ei')
                #print eiSolved, ei
                testFacility.assertAlmostEqual( ei*meV/ eiSolved, 1)
                return

            def _defaults(self):
                eiSolver = self.inventory.eiSolver
                eiSolver.inventory.monitor1Id = 1
                #eiSolver.inventory.monitor1FitGuess = [210., 4., 1000., 0.0]
                eiSolver.inventory.monitor2Id = 2
                #eiSolver.inventory.monitor2FitGuess = [410., 4., 1000., 0.0]
                return
            
            def _configure(self):
                si = self.inventory
                self.eiSolver = si.eiSolver
                return

            pass # end of Test
        t = Test('t')
        t.run()
        return
    

    pass # end of IncidentEnergySolver_UseMonitors_TestCase


from pyre.units.energy import meV
    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_UseMonitors_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: IncidentEnergySolver_UseMonitors_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
