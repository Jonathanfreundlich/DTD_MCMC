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

class struct_grain_temp:
    pass
#! end class

class struct_grain_temp1:
    pass
#! end class

class struct_grain_temp2:
    pass
#! end class

class struct_grain_temp3:
    pass
#! end class

#!======================================================================
  
def read_grain_temp(file_name):

    #! Beware: Python lists start at index 0 whereas, by default,
    #! Fortran arrays start at index 1.
    
    data = struct_grain_temp()
    
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
        data.region[i_region] = struct_grain_temp1()
        row = unit.readline().strip().replace('" ', '" , ').split(' , ')
        data.region[i_region].id = miu.clean_string(row[0])
        row = row[1].split()
        dim_species = int(row[0])
        data.region[i_region].stoch_heating = miu.boolean(row[1])
        data.region[i_region].dim_species = dim_species
        data.region[i_region].species = np.empty(dim_species, dtype="object")
        for i_species in range(dim_species):
            data.region[i_region].species[i_species] = struct_grain_temp2()
            data.region[i_region].species[i_species].id \
                = miu.get_single_string(unit)
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
                        data.region[i_region].species[i_species] \
                            .state = np.empty((dim_age_grains, dim_radius), \
                                              dtype="object")
                        pass
                    #! end if
                    for i_radius in range(dim_radius):
                        if data.region[i_region].stoch_heating:
                            row = unit.readline().split()
                            data.region[i_region].species[i_species] \
                                .radius[i_radius] = float(row[0])
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius] = struct_grain_temp3()
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].temp_eq = float(row[1])
                            dim_temp = int(row[2])
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].dim_temp = dim_temp
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].temp \
                                = np.empty(dim_temp, dtype="float")
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].prob \
                                = np.empty(dim_temp, dtype="float")
                            for i_temp in range(dim_temp):
                                row = unit.readline().split()
                                data.region[i_region].species[i_species] \
                                    .state[i_age, i_radius].temp[i_temp] \
                                    = float(row[0])
                                data.region[i_region].species[i_species] \
                                    .state[i_age, i_radius].prob[i_temp] \
                                    = float(row[1])
                                pass
                            #! end for
                            pass
                        #! 
                        else:
                            row = unit.readline().split()
                            data.region[i_region].species[i_species] \
                                .radius[i_radius] = float(row[0])
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius] = struct_grain_temp3()
                            data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].temp_eq = float(row[1])
                            pass
                        #! end if
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
