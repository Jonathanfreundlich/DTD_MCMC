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

#! To run the code with either Python2 or Python3:

from __future__ import print_function

try:
    input = raw_input
except NameError:
    pass

#!======================================================================
#! External modules for maths and graphs:

import numpy as np
import matplotlib.pyplot as plt

#!======================================================================
#! Pégase.3 modules:

import mod_read_grain_SED as mrgs
import mod_input_util as miu
import mod_directories as md

#!======================================================================
#! Read file names:

print("Enter the name of the file of grain SEDs \
(followed by the <RETURN>/<ENTER> key).\n\n\
To specify a path relative to the current directory, \
start the file name with \"" + md.current_dir_id + "\".\n\
You may also provide an absolute path starting with \"" \
+ md.root_dir_id + "\" (root directory)\n\
or with \"" + md.home_dir_id + "\" (home directory).\n\
In all other cases, the path is relative to \"" + md.grain_SED_dir + "\".\n\
(See variables `root_dir_id`, `home_dir_id`, `home_dir` \
and `grain_SED_dir`\n\
in file \"mod_directories.py\".)")

row = miu.clean_string(input())

file_name = md.path_file(md.grain_SED_dir, row)

#!======================================================================
#! Read input data:

data = mrgs.read_grain_SED(file_name)

#!======================================================================
#! Plot of grain emission spectra.

plt.ion()
for i_age in range(data.dim_age_grains):
    print("age/(1 Myr) =", data.age_grains[i_age])
    for i_region in range(data.dim_region):
        print("region = \"" + str(data.region[i_region].id) + "\"")
        for i_species in range(data.region[i_region].dim_species):
            dim_lambda = data.region[i_region].species[i_species].dim_lambda
            print("species = \"" \
                  + str(data.region[i_region].species[i_species].id) + "\"")
            for i_radius in range(data.region[i_region].species[i_species] \
                                  .dim_radius):
                print("radius/(1 um) =", \
                      data.region[i_region].species[i_species].radius[i_radius])
                l10_x_min = np.log10(data.region[i_region].species[i_species] \
                                     .lambda_gr[0])
                l10_x_max = np.log10(data.region[i_region].species[i_species] \
                                     .lambda_gr[dim_lambda-1])
                y_min = min(data.region[i_region].species[i_species] \
                            .lum_eq[i_age, i_radius, :])
                y_max = max(data.region[i_region].species[i_species] \
                            .lum_eq[i_age, i_radius, :])
                if data.region[i_region].stoch_heating:
                    y_min = min(y_min, \
                                min(data.region[i_region].species[i_species] \
                                    .lum_stoch[i_age, i_radius, :]))
                    y_max = max(y_max, \
                                max(data.region[i_region].species[i_species] \
                                    .lum_stoch[i_age, i_radius, :]))
                    pass
                #! end if
                y_min = max(y_min, y_max/1.e10)
                delta_l10_x = l10_x_max - l10_x_min
                l10_x_min = l10_x_min - 0.1*delta_l10_x
                l10_x_max = l10_x_max + 0.1*delta_l10_x
                l10_y_min = np.log10(y_min)
                l10_y_max = np.log10(y_max)
                l10_y_max = l10_y_max + 0.1*(l10_y_max - l10_y_min)
                x_min = 10**l10_x_min
                x_max = 10**l10_x_max
                y_min = 10**l10_y_min
                y_max = 10**l10_y_max
                plt.xlim(x_min, x_max)
                plt.ylim(y_min, y_max)
                plt.xlabel("$\lambda/(1\,\mathrm{\AA})$")
                plt.ylabel("$\lambda\,L_\lambda$")
                plt.title("Grain emission spectrum")
                plt.text(10**(l10_x_min+0.05*(l10_x_max-l10_x_min)), \
                         10**(l10_y_max-0.05*(l10_y_max-l10_y_min)), \
                         "Without stochastic heating.", color="green")
                plt.loglog(data.region[i_region].species[i_species] \
                           .lambda_gr, \
                           data.region[i_region].species[i_species] \
                           .lum_eq[i_age, i_radius, :], \
                           "green")
                if data.region[i_region].stoch_heating:
                    plt.text(10**(l10_x_min+0.05*(l10_x_max-l10_x_min)), \
                             10**(l10_y_max-0.1*(l10_y_max-l10_y_min)), \
                             "With stochastic heating.", color="red")
                    plt.loglog(data.region[i_region].species[i_species] \
                               .lambda_gr, \
                               data.region[i_region].species[i_species] \
                               .lum_stoch[i_age, i_radius, :], \
                               "red")
                    pass
                #! end if
                plt.pause(0.001) #! Needed to show the plot in some cases \
                    #! for some reason.
                print("Press the <RETURN>/<ENTER> key to proceed.")
                input()
                plt.clf()
                pass
            #! end for
            pass
        #! end for
        pass
    #! end for
    pass
#! end for
