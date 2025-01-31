// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>

#include <Python.h>

#include "exceptions.h"
#include "bindings.h"


//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL arcseventdata_ARRAY_API
#include "numpy/arrayobject.h"


char pyarcseventdata_module__doc__[] = "";

// Initialization function for the module (*must* be called initarcseventdata)
extern "C"
void
initarcseventdata()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "arcseventdata", pyarcseventdata_methods,
        pyarcseventdata_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module arcseventdata");
    }

    // install the module exceptions
    pyarcseventdata_runtimeError = PyErr_NewException("arcseventdata.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pyarcseventdata_runtimeError);

    // numpy
    import_array();
    return;
}

// version
// $Id$

// End of file
