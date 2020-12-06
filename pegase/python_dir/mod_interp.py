#! This Python file uses the following encoding: utf-8 .

#!======================================================================
#! This source file is part of code Pégase.3.0.1a (2020-01-23),
#! an adjunction to Pégase.3.0.1.
#! Copyright: Michel Fioc (Michel.Fioc@iap.fr), Sorbonne université, 
#! Institut d'astrophysique de Paris/CNRS, France.
#! 
#! Pégase.3.0.1a is governed by the CeCILL license under French law and abides 
#! by the rules of distribution of free software. You can use, modify and/or 
#! redistribute this software under the terms of the CeCILL license as circulated 
#! by CEA, CNRS and INRIA at "http://www.cecill.info". The text of this license
#! is also available in French and in English in directory "doc_dir/" of this
#! code.
#! 
#! As a counterpart to the access to the source code and to the rights to copy,
#! modify and redistribute it granted by the license, users are provided only
#! with a limited warranty, and the software's author, the holder of the
#! economic rights, and the successive licensors have only limited
#! liability. 
#! 
#! The fact that you are presently reading this means that you have had
#! knowledge of the CeCILL license and that you accept its terms.
#!====================================================================== 

import numpy as np

#!======================================================================

def bracket(n, x, t):

    i = 0
    if t < x[0]: #! Downward extrapolation.
        i_inf = 0
    elif t > x[n-1]: #! Upward extrapolation.
        i_inf = n-2
    else: #! Interpolation.
        i_inf = 0
        i_sup = n-1
        if i >= 0 and i <= n-1: #! Valid initial guess provided; \
#!                                  search first in the vicinity of `x(i)`.
            d_i = 1
            if t >= x[i]:
                i_inf = i
                i_sup = min(n-1, i+d_i)
                while t > x[i_sup]:
                    i_inf = i_sup
                    d_i = 2*d_i
                    i_sup = min(n-1, i+d_i)
                else:
                    pass
                #! end while
            else:
                i_sup = i
                i_inf = max(0, i-d_i)
                while t < x[i_inf]:
                    i_sup = i_inf
                    d_i = 2*d_i
                    i_inf = max(0, i-d_i)
                else:
                    pass
                #! end while
                pass
            #! end if
            pass
        #! end if
        #! Search by dichotomy:
        while i_inf+1 < i_sup:
            i_med = (i_inf+i_sup)//2
            if t <= x[i_med]:
                i_sup = i_med
            else:
                i_inf = i_med
                pass
            #! end if
        else:
            pass
        #! end while
        pass
    #! end if

    i = i_inf
    
    return i

#! end def

#!======================================================================

def interp_log_log(x1, x2, y1, y2, x):

    y = 10**(np.log10(y1) + (np.log10(x)-np.log10(x1)) \
             * (np.log10(y2)-np.log10(y1))
             / (np.log10(x2)-np.log10(x1)))

    return y
    
#! end def
