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

#include <sstream>
#include <iostream>

#include "numpy_support.h"
#include "wrap_events2EvenlySpacedIxxxx.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIxxxx.h"

#include "arcseventdata/Event2QQQE.h"
#include "arcseventdata/Event2hklE.h"


#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace wrap_arcseventdata
{

  namespace wrap_events2EvenlySpacedIxxxx_Impl {
    const char jrnltag[] = "events2EvenlySpacedIxxxx";
  }
  
  using namespace ARCS_EventData;
  using namespace reductionmod;
  
  namespace events2EvenlySpacedIxxxx_impl {
    
    template <typename Event2XXXX, 
	      typename X1Data, typename X2Data, typename X3Data, typename X4Data,
	      typename ZData, int ZTypeCode
	      >
    PyObject * call_numpyarray
    (const Event2XXXX & e2xxxx,
     PyObject * pyevents, size_t N,
     X1Data x1_begin, X1Data x1_end, X1Data x1_step, 
     X2Data x2_begin, X2Data x2_end, X2Data x2_step, 
     X3Data x3_begin, X3Data x3_end, X3Data x3_step, 
     X4Data x4_begin, X4Data x4_end, X4Data x4_step, 
     PyObject *pyzarray)
    {
      if (checkDataType(pyzarray, "zarray", ZTypeCode)) return 0;

      std::ostringstream oss;

      const Event *events_begin = (const Event *)
	PyCObject_AsVoidPtr( pyevents );
#ifdef DEBUG
      journal::debug_t debug( wrap_events2EvenlySpacedIxxxx_Impl::jrnltag );
      debug << journal::at(__HERE__)
	    << "events_begin = " << events_begin 
	    << journal::endl;
#endif
      if (events_begin == 0) {
	oss << "first argument must be a PyCObject of a void pointer " 
	    << "pointing to an events array."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      size_t nzarrsize = PyArray_Size( pyzarray );
      
      //std::cout << x_begin << ", " << x_end << ", " << x_step << std::endl;
      size_t tmpsize =  size_t((x1_end-x1_begin)/x1_step) * size_t( (x2_end-x2_begin)/x2_step)
	* size_t((x3_end-x3_begin)/x3_step) * size_t( (x4_end-x4_begin)/x4_step);
      
      if (nzarrsize != tmpsize )  {
	oss << "Size mismatch: "
	    << "zarray: size = " << nzarrsize << "; "
	    << "x1 bin boundaries parameters = " << x1_begin << ", " << x1_end << ", " << x1_step
	    << "x2 bin boundaries parameters = " << x2_begin << ", " << x2_end << ", " << x2_step
	    << "x3 bin boundaries parameters = " << x3_begin << ", " << x3_end << ", " << x3_step
	    << "x4 bin boundaries parameters = " << x4_begin << ", " << x4_end << ", " << x4_step
	    << std::endl;
	oss << "This could be caused by python floating-point-number error."
	    << "You can try to change the step size and see if that helps."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      typedef Array1DIterator<ZData> ZIterator;
      ZIterator z_begin(pyzarray);
      
      events2EvenlySpacedIxxxx<Event2XXXX, X1Data, X2Data, X3Data, X4Data, ZData, ZIterator>
	(events_begin, N, e2xxxx, 
	 x1_begin, x1_end, x1_step, 
	 x2_begin, x2_end, x2_step, 
	 x3_begin, x3_end, x3_step, 
	 x4_begin, x4_end, x4_step, 
	 z_begin);

      return Py_None;
    }
    
  }
 
  

  // 
  char events2IQQQE_numpyarray__name__[] = "events2IQQQE_numpyarray";
  char events2IQQQE_numpyarray__doc__[] = "events2IQQQE_numpyarray\n" \
"events2IQQQE( events, N, \n"\
"            Qx_begin, Qx_end, Qx_step, \n"\
"            Qy_begin, Qy_end, Qy_step, \n"\
"            Qz_begin, Qz_end, Qz_step, \n"\
"            E_begin, E_end, E_step, \n"\
"            intensities, Ei, pixelPositions, ntotpixels, tofUnit, \n"\
"            mod2sample, toffset, intensity_npy_typecode)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // Qx_begin, Qx_end, Qx_step: Qx axis parameters
  // Qy_begin, Qy_end, Qy_step: Qy axis parameters
  // Qz_begin, Qz_end, Qz_step: Qz axis parameters
  // E_begin, E_end, E_step: E axis parameters
  // intensities: numpy array to store I(d)
  // Ei: incident neutron energy
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  // toffset: shutter time offset. unit: microsecond
  // intensity_npy_typecode: numpy typecode for the intensity array
  
  PyObject * events2IQQQE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double Qx_begin, Qx_end, Qx_step;
    double Qy_begin, Qy_end, Qy_step;
    double Qz_begin, Qz_end, Qz_step;
    double E_begin, E_end, E_step;
    double Ei;
    PyObject *pypixelPositions;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    double toffset = 0;
    int intensity_npy_typecode = NPY_INT;
    
    int ok = PyArg_ParseTuple
      (args, "OlddddddddddddOdO|ldddi", 
       &pyevents, &N, 
       &Qx_begin, &Qx_end, &Qx_step,
       &Qy_begin, &Qy_end, &Qy_step,
       &Qz_begin, &Qz_end, &Qz_step,
       &E_begin, &E_end, &E_step,
       &pyintensities,
       &Ei,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample,
       &toffset,
       &intensity_npy_typecode);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2QQQE e2QQQE( Ei, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset );
    /*
    std::cout << "pixel axis" 
	      << Q_begin << ", "
	      << Q_end << ", "
	      << Q_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << E_begin << ", "
	      << E_end << ", "
	      << E_step << ", "
	      << std::endl;
    */
    switch (intensity_npy_typecode) {

    case NPY_INT:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2QQQE,
	double, double, double, double, npy_int, NPY_INT>
	(e2QQQE,
	 pyevents, N,
	 Qx_begin, Qx_end, Qx_step, 
	 Qy_begin, Qy_end, Qy_step, 
	 Qz_begin, Qz_end, Qz_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    case NPY_LONG:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2QQQE,
	double, double, double, double, npy_long, NPY_LONG>
	(e2QQQE,
	 pyevents, N,
	 Qx_begin, Qx_end, Qx_step, 
	 Qy_begin, Qy_end, Qy_step, 
	 Qz_begin, Qz_end, Qz_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    case NPY_DOUBLE:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2QQQE,
	double, double, double, double, npy_double, NPY_DOUBLE>
	(e2QQQE,
	 pyevents, N,
	 Qx_begin, Qx_end, Qx_step, 
	 Qy_begin, Qy_end, Qy_step, 
	 Qz_begin, Qz_end, Qz_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    default:
      std::ostringstream oss;
      oss << "Not implemented yet: intensity array data type is " 
	  << intensity_npy_typecode
	  << "."
	  << "int: " << NPY_INT << ", "
	  << "long: " << NPY_LONG << ", "
	  << "double: " << NPY_DOUBLE << ", "
	  << std::endl;
      PyErr_SetString( PyExc_NotImplementedError, oss.str().c_str() );
      return 0;
      
    }
  }
  

  // 
  char events2IhklE_numpyarray__name__[] = "events2IhklE_numpyarray";
  char events2IhklE_numpyarray__doc__[] = "events2IhklE_numpyarray\n" \
"events2IhklE( events, N, \n"\
"            h_begin, h_end, h_step, \n"\
"            k_begin, k_end, k_step, \n"\
"            l_begin, l_end, l_step, \n"\
"            E_begin, E_end, E_step, \n"\
"            intensities, Ei, ub, pixelPositions, ntotpixels, tofUnit, \n"\
"            mod2sample, toffset, intensity_npy_typecode)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // h_begin, h_end, h_step: h axis parameters
  // k_begin, k_end, k_step: k axis parameters
  // l_begin, l_end, l_step: l axis parameters
  // E_begin, E_end, E_step: E axis parameters
  // intensities: numpy array to store Intensities
  // Ei: incident neutron energy
  // ub: matrix to convert Q vector to hkl
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  // toffset: shutter time offset. unit: microsecond
  // intensity_npy_typecode: numpy typecode for the intensity array
  
  PyObject * events2IhklE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double h_begin, h_end, h_step;
    double k_begin, k_end, k_step;
    double l_begin, l_end, l_step;
    double E_begin, E_end, E_step;
    double Ei;
    PyObject *pyub;
    PyObject *pypixelPositions;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    double toffset = 0;
    int intensity_npy_typecode = NPY_INT;
    
    int ok = PyArg_ParseTuple
      (args, "OlddddddddddddOdOO|ldddi", 
       &pyevents, &N, 
       &h_begin, &h_end, &h_step,
       &k_begin, &k_end, &k_step,
       &l_begin, &l_end, &l_step,
       &E_begin, &E_end, &E_step,
       &pyintensities,
       &Ei,
       &pyub,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample,
       &toffset,
       &intensity_npy_typecode);
    
    if (!ok) return 0;

    // convert ub from python object to a double array
    if (!PyTuple_Check(pyub) || PyTuple_Size(pyub)!=3 ) {
      PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple");
      return 0;
    }
    double ub[9];
    for (int i=0; i<3; i++) {
      PyObject *item = PyTuple_GetItem(pyub, i);

      if (!PyTuple_Check(item) || PyTuple_Size(item)!=3) {
	PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple of 3-tuples");
	return 0;
      }
      for (int j=0; j<3; j++) {
	PyObject *pynum = PyTuple_GetItem(item,j);
	if (!PyFloat_Check(pynum)) {
	  PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple of 3-tuples of floats");
	  return 0;
	}
	ub[3*i+j] = PyFloat_AsDouble(pynum);
      }
    }
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2hklE e2hklE( Ei, ub, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset );
    /*
    std::cout << "pixel axis" 
	      << Q_begin << ", "
	      << Q_end << ", "
	      << Q_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << E_begin << ", "
	      << E_end << ", "
	      << E_step << ", "
	      << std::endl;
    */
    switch (intensity_npy_typecode) {

    case NPY_INT:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2hklE,
	double, double, double, double, npy_int, NPY_INT>
	(e2hklE,
	 pyevents, N,
	 h_begin, h_end, h_step, 
	 k_begin, k_end, k_step, 
	 l_begin, l_end, l_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    case NPY_LONG:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2hklE,
	double, double, double, double, npy_long, NPY_LONG>
	(e2hklE,
	 pyevents, N,
	 h_begin, h_end, h_step, 
	 k_begin, k_end, k_step, 
	 l_begin, l_end, l_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    case NPY_DOUBLE:
      return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2hklE,
	double, double, double, double, npy_double, NPY_DOUBLE>
	(e2hklE,
	 pyevents, N,
	 h_begin, h_end, h_step, 
	 k_begin, k_end, k_step, 
	 l_begin, l_end, l_step, 
	 E_begin, E_end, E_step, 
	 pyintensities)
	;

    default:
      std::ostringstream oss;
      oss << "Not implemented yet: intensity array data type is " 
	  << intensity_npy_typecode
	  << "."
	  << "int: " << NPY_INT << ", "
	  << "long: " << NPY_LONG << ", "
	  << "double: " << NPY_DOUBLE << ", "
	  << std::endl;
      PyErr_SetString( PyExc_NotImplementedError, oss.str().c_str() );
      return 0;
      
    }
  }
  
} // wrap_arcseventdata:



// version
// $Id$

// End of file
