// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_ARCSEVENTDATA_EVENT2QE
#define H_ARCSEVENTDATA_EVENT2QE

#include "Event2Quantity.h"

namespace ARCS_EventData{

  // Event -> pixelID, energy transfer
  class Event2QE: public Event2Quantity2<double, double>
  {
  public:
    // meta methods
    /// ctor.
    /// Constructor. 
    /// Ei: neutron incident energy. meV
    /// pixelPositions: mapping of pixelID --> position 
    ///     pixelPositions[pixelID*3, pixelID*3+1, pixelID*3+2] is the position vector
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    /// mod2sample: distance from moderator to sample. unit: meter
    /// tofset: shutter tof offset
    Event2QE
    ( double Ei,
      const double * pixelPositions, 
      unsigned int ntotpixels = (1+115)*8*128,
      double tofUnit=1e-7, double mod2sample=13.5,
      double toffset = 0.0
      );

    // methods
    unsigned int operator() ( const Event & e, double &Q, double & E ) const ;


  private:

    //data
    double m_Ei, m_vi, m_ki;
    const double * m_pixelPositions;
    double m_tofUnit;
    double m_mod2sample;
    double m_ntotpixels;
    double m_toffset;
  };
  
}


#endif // H_ARCSEVENTDATA_EVENT2QE


// version
// $Id$

// End of file 
  
