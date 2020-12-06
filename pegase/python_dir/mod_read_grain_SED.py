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

import mod_input_util as miu

#!======================================================================

class struct_grain_SED:
    pass
#! end class

class struct_grain_SED1:
    pass
#! end class

class struct_grain_SED2:
    pass
#! end class

#!======================================================================
  
def read_grain_SED(file_name):

    #! Beware: Python lists start at index 0 whereas, by default,
    #! Fortran arrays start at index 1.
    #! Field named "lambda" in Fortran renamed "lambda_gr" in Python
    #! because Python's `lambda` is used to create anonymous functions
    #! (see Alonzo Church's "lambda calculus").
    
    data = struct_grain_SED()
    
    unit = open(file_name)

    data.version_id = miu.get_single_string(unit)

    data.version_date = miu.get_single_string(unit)

    row = miu.next_non_comment_line(unit).split()
    dim_age_grains = int(row[0])
    dim_region = int(row[1])
    data.dim_age_grains = dim_age_grains
    data.dim_region = dim_region
    
    data.age_grains = np.empty(dim_age_grains, dtype="float")
    data.region = np.empty(dim_region, dtype="object")

    for i_region in range(dim_region):
        data.region[i_region] = struct_grain_SED1()
        row = unit.readline().strip().replace('" ', '" , ').split(' , ')
        data.region[i_region].id = miu.clean_string(row[0])
        row = row[1].split()
        dim_species = int(row[0])
        data.region[i_region].stoch_heating = miu.boolean(row[1])
        data.region[i_region].dim_species = dim_species
        data.region[i_region].species = np.empty(dim_species, dtype="object")
        for i_species in range(dim_species):
            data.region[i_region].species[i_species] = struct_grain_SED2()
            row = unit.readline().strip().replace('" ', '" , ').split(' , ')
            data.region[i_region].species[i_species].id = miu.clean_string(row[0])
            dim_lambda = int(row[1])
            data.region[i_region].species[i_species].dim_lambda = dim_lambda
            data.region[i_region].species[i_species].lambda_gr \
                = np.empty(dim_lambda, dtype="float")
            i_lambda = 0
            while True:
                row = unit.readline().split()
                for i_col in range(len(row)):
                    data.region[i_region].species[i_species] \
                        .lambda_gr[i_lambda] = float(row[i_col])
                    i_lambda = i_lambda+1
                    pass
                #! end for
                if i_lambda == dim_lambda: break
                pass
            #! end while
            pass
        #! end for
        pass
    #! end for

    for i_age in range(dim_age_grains):
        for i_region in range(dim_region):
            data.age_grains[i_age] = miu.get_single_float(unit)
            eff_dim_species = miu.get_single_int(unit)
            if eff_dim_species > 0:
                for i_species in range(data.region[i_region].dim_species):
                    dim_radius = miu.get_single_int(unit)
                    data.region[i_region].species[i_species].dim_radius \
                        = dim_radius
                    if i_age == 0:
                        data.region[i_region].species[i_species] \
                            .radius = np.empty(dim_radius, dtype="float")
                        dim_lambda = data.region[i_region].species[i_species] \
                                     .dim_lambda
                        if data.region[i_region].stoch_heating:
                            data.region[i_region].species[i_species].lum_stoch \
                                = np.empty((dim_age_grains, dim_radius, \
                                            dim_lambda), dtype="float")
                            pass
                        #! end if
                        data.region[i_region].species[i_species].lum_eq \
                            = np.empty((dim_age_grains, dim_radius, \
                                        dim_lambda), dtype="float")

                        pass
                    #! end if
                    for i_radius in range(dim_radius):
                        data.region[i_region].species[i_species] \
                            .radius[i_radius] = miu.get_single_float(unit)
                        if data.region[i_region].stoch_heating:
                           i_lambda = 0
                           while True:
                               row = unit.readline().split()
                               for i_col in range(len(row)):
                                   data.region[i_region].species[i_species] \
                                       .lum_stoch[i_age, i_radius, i_lambda] \
                                       = float(row[i_col])
                                   i_lambda = i_lambda+1
                                   pass
                               #! end for
                               if i_lambda == dim_lambda: break
                               pass
                           #! end while
                           pass
                        #! end if
                        i_lambda = 0
                        while True:
                            row = unit.readline().split()
                            for i_col in range(len(row)):
                                data.region[i_region].species[i_species] \
                                    .lum_eq[i_age, i_radius, i_lambda] \
                                    = float(row[i_col])
                                i_lambda = i_lambda+1
                                pass
                            #! end for
                            if i_lambda == dim_lambda: break
                            pass
                        #! end while
                        pass
                    #! end do
                    pass
                #! end do
            else:
                pass
            #! end if
            pass
        #! end do
        pass
    #! end do

    unit.close()

    return data

#! end def
