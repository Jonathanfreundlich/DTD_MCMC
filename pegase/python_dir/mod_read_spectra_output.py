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

import sys

import mod_input_util as miu

#!======================================================================

class struct_spectra_output:
    pass
#! end class

#!======================================================================

def read_spectra_output(file_name):

    #! Beware: Python lists start at index 0 whereas, by default,
    #! Fortran arrays start at index 1.

    data = struct_spectra_output()

    unit = open(file_name)

    data.version_id = miu.get_single_string(unit)

    data.version_date = miu.get_single_string(unit)

    row = miu.next_non_comment_line(unit)
    
    data.spectra_output = miu.clean_string(row.strip().replace('" ', '" , ').split(' , ')[0])
    
    if data.spectra_output == "detailed":
        data.RF_output = miu.get_single_boolean(unit)
        data.sublim_output = miu.get_single_boolean(unit)
    else:
        data.RF_output = False
        data.sublim_output = False
        pass
    #! end if
            
    data.time_step = miu.get_single_float(unit)
            
    dim_output_age = miu.get_single_int(unit)
    data.dim_output_age = dim_output_age

    data.dim_elem = miu.get_single_int(unit)
            
    data.elem_id = np.empty(data.dim_elem, dtype="object")
    row = unit.readline().strip().replace('" ', '" , ').split(' , ')
    for i_col in range(data.dim_elem):
        data.elem_id[i_col] = miu.clean_string(row[i_col])
        pass
    #! end for

    row = unit.readline()
    dim_species_SFC = int(row.split()[0])
    data.dim_species_SFC = dim_species_SFC
    dim_species_DISM = int(row.split()[1])
    data.dim_species_DISM = dim_species_DISM
            
    data.species_id_SFC = np.empty(dim_species_SFC, dtype="object")
    row = unit.readline().strip().replace('" ', '" , ').split(' , ')
    for i_col in range(dim_species_SFC):
        data.species_id_SFC[i_col] = miu.clean_string(row[i_col])
        pass
    #! end for

    data.species_id_DISM = np.empty(dim_species_DISM, dtype="object")
    row = unit.readline().strip().replace('" ', '" , ').split(' , ')
    for i_col in range(dim_species_DISM):
        data.species_id_DISM[i_col] = miu.clean_string(row[i_col])
        pass
    #! end for
            
    dim_cont = miu.get_single_int(unit)
    data.dim_cont = dim_cont

    dim_line = miu.get_single_int(unit)
    data.dim_line = dim_line

    miu.skip_row(unit)
    data.lambda_cont = np.empty(dim_cont, dtype="float")
    i_cont = 0
    while True:
        row = unit.readline().split()
        for i_col in range(len(row)):
            data.lambda_cont[i_cont] = float(row[i_col])
            i_cont = i_cont+1
            pass
        #! end for
        if i_cont == dim_cont: break
        pass
    #! end while
    
    miu.skip_row(unit)
    data.line_id = np.empty(dim_line, dtype="object")
    data.lambda_line = np.empty(dim_line, dtype="float")
    for i_row in range(dim_line):
        row = unit.readline().strip().replace('" ', '" , ').split(' , ')
        data.line_id[i_row] = miu.clean_string(row[0])
        data.lambda_line[i_row] = float(row[1])
        pass
    #! end for
    
    data.reserv_warn_present = miu.get_single_boolean(unit)
    data.SF_warn_present = miu.get_single_boolean(unit)

    if data.SF_warn_present:
        data.SF_warn_age = miu.get_single_float(unit)
        pass
    #! end if        

    data.dim_infall_warn = miu.get_single_int(unit)

    data.infall_warn_present = np.empty(dim_line, dtype="int") # Change name of variable???
    data.infall_warn_age = np.empty(dim_line, dtype="float")
    for i_row in range(data.dim_infall_warn):
        row = unit.readline().split()
        data.infall_warn_present[i_row] = int(row[0])
        data.infall_warn_age[i_row] = float(row[1])
        pass
    #! end for
        
    data.outflow_warn_present = miu.get_single_boolean(unit)
    if data.outflow_warn_present:
        data.outflow_warn_age = miu.get_single_float(unit)
        pass
    #! end if

    data.output_age = np.empty(dim_output_age, dtype="float")
    data.convol_time = np.empty(dim_output_age, dtype="float")
    data.cosmic_time = np.empty(dim_output_age, dtype="float")
    data.redshift = np.empty(dim_output_age, dtype="float")
    data.galaxy_mass = np.empty(dim_output_age, dtype="float")
    data.live_stars_mass = np.empty(dim_output_age, dtype="float")
    data.WD_mass = np.empty(dim_output_age, dtype="float")
    data.BHNS_mass = np.empty(dim_output_age, dtype="float")
    data.inert_mass = np.empty(dim_output_age, dtype="float")
    data.ISM_mass = np.empty(dim_output_age, dtype="float")
    data.ISM_Z = np.empty(dim_output_age, dtype="float")
    data.stel_Z_mass_avrg = np.empty(dim_output_age, dtype="float")
    data.stel_Z_bol_avrg = np.empty(dim_output_age, dtype="float")
    data.carb_abund = np.empty(dim_output_age, dtype="float")
    data.sil_abund = np.empty(dim_output_age, dtype="float")
    data.ISM_abund = np.empty((dim_output_age, data.dim_elem), dtype="float")
    data.L_bol = np.empty(dim_output_age, dtype="float")
    data.tau_V = np.empty(dim_output_age, dtype="float")
    data.L_dust = np.empty(dim_output_age, dtype="float")
    data.SF_rate = np.empty(dim_output_age, dtype="float")
    data.Lyman_cont_rate = np.empty(dim_output_age, dtype="float")
    data.CCSN_rate = np.empty(dim_output_age, dtype="float")
    data.SNIa_rate = np.empty(dim_output_age, dtype="float")
    data.stel_age_mass_avrg = np.empty(dim_output_age, dtype="float")
    data.stel_age_bol_avrg = np.empty(dim_output_age, dtype="float")
    data.Lyman_cont_gas_abs = np.empty(dim_output_age, dtype="float")
    data.Lyman_cont_dust_abs = np.empty(dim_output_age, dtype="float")
    data.ejec_rate_tot = np.empty(dim_output_age, dtype="float")
    data.infall_rate = np.empty(dim_output_age, dtype="float")
    data.outflow_rate = np.empty(dim_output_age, dtype="float")
    data.ejec_cumul_mass = np.empty(dim_output_age, dtype="float")
    data.SF_live_cumul_mass = np.empty(dim_output_age, dtype="float")
    data.infall_cumul_mass = np.empty(dim_output_age, dtype="float")
    data.outflow_cumul_mass = np.empty(dim_output_age, dtype="float")
    data.L_dust_SFC = np.empty(dim_output_age, dtype="float")
    data.L_dust_DISM = np.empty(dim_output_age, dtype="float")
    data.opt_depth_warn_present = np.empty(dim_output_age, dtype="object")
    data.opt_depth_warn_min_lambda = np.empty(dim_output_age, dtype="float")
    data.opt_depth_warn_max_lambda = np.empty(dim_output_age, dtype="float")
    data.lum_cont = np.empty((dim_output_age, dim_cont), dtype="float")
    data.L_line = np.empty((dim_output_age, dim_line), dtype="float")
    data.lum_stel_SFC_unatt \
        = np.empty((dim_output_age, dim_cont), dtype="float")
    data.lum_stel_DISM_unatt \
        = np.empty((dim_output_age, dim_cont), dtype="float")
    data.lum_neb_cont_SFC_unatt \
        = np.empty((dim_output_age, dim_cont), dtype="float")
    data.lum_neb_cont_DISM_unatt \
        = np.empty((dim_output_age, dim_cont), dtype="float")
    data.RF_cont_SFC = np.empty((dim_output_age, dim_cont), dtype="float")
    data.RF_cont_DISM = np.empty((dim_output_age, dim_cont), dtype="float")
    data.lum_species_SFC \
        = np.empty((dim_species_SFC, dim_output_age, dim_cont), dtype="float")
    data.lum_species_DISM \
        = np.empty((dim_species_SFC, dim_output_age, dim_cont), dtype="float")
    data.sublim_lum_species_SFC \
        = np.empty((dim_species_SFC, dim_output_age, dim_cont), dtype="float")
    data.sublim_lum_species_DISM \
        = np.empty((dim_species_SFC, dim_output_age, dim_cont), dtype="float")
    data.L_line_SFC_unatt = np.empty((dim_output_age, dim_line), dtype="float")
    data.L_line_DISM_unatt = np.empty((dim_output_age, dim_line), dtype="float")
    data.RF_line_SFC = np.empty((dim_output_age, dim_line), dtype="float")
    data.RF_line_DISM = np.empty((dim_output_age, dim_line), dtype="float")
    
    for i_time in range(dim_output_age):
        
        data.output_age[i_time] = miu.get_single_float(unit)

        data.convol_time[i_time] = miu.get_single_float(unit)

        data.cosmic_time[i_time] = miu.get_single_float(unit)
        
        data.redshift[i_time] = miu.get_single_float(unit)
        
        data.galaxy_mass[i_time] = miu.get_single_float(unit)

        data.live_stars_mass[i_time] = miu.get_single_float(unit)
        
        data.WD_mass[i_time] = miu.get_single_float(unit)
        
        data.BHNS_mass[i_time] = miu.get_single_float(unit)
        
        data.inert_mass[i_time] = miu.get_single_float(unit)
        
        data.ISM_mass[i_time] = miu.get_single_float(unit)
        
        data.ISM_Z[i_time] = miu.get_single_float(unit)
        
        data.stel_Z_mass_avrg[i_time] = miu.get_single_float(unit)
        
        data.stel_Z_bol_avrg[i_time] = miu.get_single_float(unit)
        
        data.carb_abund[i_time] = miu.get_single_float(unit)
        
        data.sil_abund[i_time] = miu.get_single_float(unit)
        
        row = unit.readline().split()
        for i_col in range(data.dim_elem):
            data.ISM_abund[i_time, i_col] = float(row[i_col])
            pass
        #! end for
 
        data.L_bol[i_time] = miu.get_single_float(unit)

        data.tau_V[i_time] = miu.get_single_float(unit)
        
        data.L_dust[i_time] = miu.get_single_float(unit)
        
        data.SF_rate[i_time] = miu.get_single_float(unit)
        
        data.Lyman_cont_rate[i_time] = miu.get_single_float(unit)
        
        data.CCSN_rate[i_time] = miu.get_single_float(unit)
        
        data.SNIa_rate[i_time] = miu.get_single_float(unit)
        
        data.stel_age_mass_avrg[i_time] = miu.get_single_float(unit)
        
        data.stel_age_bol_avrg[i_time] = miu.get_single_float(unit)
        
        data.Lyman_cont_gas_abs[i_time] = miu.get_single_float(unit)
        
        data.Lyman_cont_dust_abs[i_time] = miu.get_single_float(unit)
        
        data.ejec_rate_tot[i_time] = miu.get_single_float(unit)
        
        data.infall_rate[i_time] = miu.get_single_float(unit)
        
        data.outflow_rate[i_time] = miu.get_single_float(unit)
        
        data.ejec_cumul_mass[i_time] = miu.get_single_float(unit)
        
        data.SF_live_cumul_mass[i_time] = miu.get_single_float(unit)
        
        data.infall_cumul_mass[i_time] = miu.get_single_float(unit)
        
        data.outflow_cumul_mass[i_time] = miu.get_single_float(unit)
        
        data.L_dust_SFC[i_time] = miu.get_single_float(unit)
        
        data.L_dust_DISM[i_time] = miu.get_single_float(unit)
        
        data.opt_depth_warn_present[i_time] \
            = miu.get_single_boolean(unit)
        if data.opt_depth_warn_present[i_time]:
            data.opt_depth_warn_min_lambda[i_time] = miu.get_single_float(unit)
            data.opt_depth_warn_max_lambda[i_time] = miu.get_single_float(unit)
            pass
        #! end if

        if data.spectra_output == "detailed":
            miu.skip_row(unit)
            
            for i_cont in range(dim_cont):
                if data.RF_output:
                    row = unit.readline().split()
                    data.lum_cont[i_time, i_cont] = float(row[0])
                    data.lum_stel_SFC_unatt[i_time, i_cont] = float(row[1])
                    data.lum_stel_DISM_unatt[i_time, i_cont] = float(row[2])
                    data.lum_neb_cont_SFC_unatt[i_time, i_cont] = float(row[3])
                    data.lum_neb_cont_DISM_unatt[i_time, i_cont] = float(row[4])
                    data.RF_cont_SFC[i_time, i_cont] = float(row[5])
                    data.RF_cont_DISM[i_time, i_cont] = float(row[6])
                else:
                    row = unit.readline().split()
                    data.lum_cont[i_time, i_cont] = float(row[0])
                    data.lum_stel_SFC_unatt[i_time, i_cont] = float(row[1])
                    data.lum_stel_DISM_unatt[i_time, i_cont] = float(row[2])
                    data.lum_neb_cont_SFC_unatt[i_time, i_cont] = float(row[3])
                    data.lum_neb_cont_DISM_unatt[i_time, i_cont] = float(row[4])
                    pass
                #! end if
                pass
            #! end for

            miu.skip_row(unit)
            for i_cont in range(dim_cont):
                row = unit.readline().split()
                for i_col in range(dim_species_SFC):
                    data.lum_species_SFC[i_col, i_time, i_cont] \
                        = float(row[i_col])
                    pass
                #! end for
                for i_col in range(dim_species_DISM):
                    data.lum_species_DISM[i_col, i_time, i_cont] \
                        = float(row[dim_species_SFC+i_col])
                    pass
                #! end for
                pass
            #! end for

            if data.sublim_output:
                miu.skip_row(unit)
                for i_cont in range(dim_cont):
                    row = unit.readline().split()
                    for i_col in range(dim_species_SFC):
                        data.sublim_lum_species_SFC[i_col, i_time, i_cont] \
                            = float(row[i_col])
                        pass
                    #! end for
                    for i_col in range(dim_species_DISM):
                        data.sublim_lum_species_DISM[i_col, i_time, i_cont] \
                            = float(row[dim_species_SFC+i_col])
                        pass
                    #! end for
                    pass
                #! end for
                pass
            #! end if

            miu.skip_row(unit)
            for i_line in range(dim_line):
                if data.RF_output:
                    row = unit.readline().split()
                    data.L_line[i_time, i_line] = float(row[0])
                    data.L_line_SFC_unatt[i_time, i_line] = float(row[1])
                    data.L_line_DISM_unatt[i_time, i_line] = float(row[2])
                    data.RF_line_SFC[i_time, i_line] = float(row[3])
                    data.RF_line_DISM[i_time, i_line] = float(row[4])
                else:
                    row = unit.readline().split()
                    data.L_line[i_time, i_line] = float(row[0])
                    data.L_line_SFC_unatt[i_time, i_line] = float(row[1])
                    data.L_line_DISM_unatt[i_time, i_line] = float(row[2])
                    pass
                #! end if
                pass
            #! end for
        elif data.spectra_output == "basic":
            miu.skip_row(unit)
            i_cont = 0
            while True:
                row = unit.readline().split()
                for i_col in range(len(row)):
                    data.lum_cont[i_time, i_cont] = float(row[i_col])
                    i_cont = i_cont+1
                    pass
                #! end for
                if i_cont == dim_cont: break
                pass
            #! end for

            miu.skip_row(unit)
            i_line = 0
            while True:
                row = unit.readline().split()
                for i_col in range(len(row)):
                    data.L_line[i_time, i_line] = float(row[i_col])
                    i_line = i_line+1
                    pass
                #! end for
                if i_line == dim_line: break
                pass
            #! end while
        else:
            print("Wrong value for `spectra_output`. Stopped.")
            sys.exit()
            pass
        #! end if
        pass
    #! end for

    unit.close()

    return data

#! end def
