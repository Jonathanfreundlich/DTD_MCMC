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

import mod_read_grain_temp as mrgt
import mod_input_util as miu
import mod_directories as md

#!======================================================================
#! Read file names:

print("Enter the name of the file of grain temperatures \
(followed by the <RETURN>/<ENTER> key).\n\n\
To specify a path relative to the current directory, \
start the file name with \"" + md.current_dir_id + "\".\n\
You may also provide an absolute path starting with \"" \
+ md.root_dir_id + "\" (root directory)\n\
or with \"" + md.home_dir_id + "\" (home directory).\n\
In all other cases, the path is relative to \"" + md.grain_temp_dir + "\".\n\
(See variables `root_dir_id`, `home_dir_id`, `home_dir` \
and `grain_temp_dir`\n\
in file \"mod_directories.py\".)")

row = miu.clean_string(input())

file_name = md.path_file(md.grain_temp_dir, row)

#!======================================================================
#! Read input data:

data = mrgt.read_grain_temp(file_name)

#!======================================================================
#! Plot of grain temperatures.

plt.ion()
for i_age in range(data.dim_age_grains):
    print("age/(1 Myr) =", data.age_grains[i_age])
    for i_region in range(data.dim_region):
        print("region = \"" + str(data.region[i_region].id) + "\"")
        if data.region[i_region].stoch_heating:
            for i_species in range(data.region[i_region].dim_species):
                print("species = \"" \
                      + str(data.region[i_region].species[i_species].id) + "\"")
                for i_radius in \
                    range(data.region[i_region].species[i_species].dim_radius):
                    print("radius/(1 um) =", data.region[i_region] \
                          .species[i_species].radius[i_radius])
                    dim_temp = data.region[i_region].species[i_species] \
                                   .state[i_age, i_radius].dim_temp
                    l10_x_min = np.log10(data.region[i_region] \
                                         .species[i_species] \
                                         .state[i_age, i_radius].temp[0])
                    l10_x_max = np.log10(data.region[i_region] \
                                         .species[i_species] \
                                         .state[i_age, i_radius] \
                                         .temp[dim_temp-1])
                    y_min = min(data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].prob[:])
                    y_max = max(data.region[i_region].species[i_species] \
                                .state[i_age, i_radius].prob[:])
                    delta_l10_x = l10_x_max - l10_x_min
                    (l10_x_min, l10_x_max) = (l10_x_min-0.1*delta_l10_x, \
                                              l10_x_max+0.1*delta_l10_x)
                    x_min = 10**l10_x_min
                    x_max = 10**l10_x_max
                    y_max = y_max + 0.1*(y_max-y_min)
                    plt.xlim(x_min, x_max)
                    plt.ylim(y_min, y_max)
                    plt.xlabel("$T/(1\,\mathrm{K})$")
                    plt.ylabel("$\mathrm{d}P/\mathrm{d}(\log_{10}T)$")
                    plt.title("Grain temperature probability")
                    plt.semilogx(data.region[i_region].species[i_species] \
                                 .state[i_age, i_radius].temp[:], \
                                 data.region[i_region].species[i_species] \
                                 .state[i_age, i_radius].prob[:], \
                                 "red")
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
        #! end if
        pass
    #! end for
    pass
#! end for
    
