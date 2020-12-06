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

import mod_read_spectra_output as mrso
import mod_interp as mi
import mod_input_util as miu
import mod_directories as md
    
#!======================================================================
#! Objects of class `struct_plot` contain 2 fields used to plot emission lines:
#! -- `y_line_bottom[i_time, i_line]`: bottom of the `i_line`-th emission line 
#!     at the `i_time`-th age;
#! -- `y_line_top[i_time, i_line]`: top of the same line.

class struct_plot:
    pass
#! end class

#!======================================================================
#! Read file names:

file_name = list()

print("Enter the names of the files of spectra, one per line \
(followed by the <RETURN>/<ENTER> key).\n\
When done, press <RETURN> on a blank line to proceed.\n\n\
To specify a path relative to the current directory, \
start the file name with \"" + md.current_dir_id + "\".\n\
You may also provide an absolute path starting with \"" \
+ md.root_dir_id + "\" (root directory)\n\
or with \"" + md.home_dir_id + "\" (home directory).\n\
In all other cases, the path is relative to \"" + md.spectra_dir + "\".\n\
(See variables `root_dir_id`, `home_dir_id`, `home_dir` \
and `spectra_dir`\n\
in file \"mod_directories.py\".)")

while(True):
    row = miu.clean_string(input())
    if row == "":
        break
    else:
        file_name.append(md.path_file(md.spectra_dir, row))
        pass
    #! end if
    pass
#! end while

dim_file = len(file_name)

#!======================================================================
#! Read input data:

data = list()
for i_file in range(dim_file):
    data.append(mrso.read_spectra_output(file_name[i_file]))
    pass
#! end for

#!======================================================================
#! For the plot, emission lines are assumed to have a Gaussian profile 
#! with standard deviation `sigma` (in angstroems). Only the peak of lines 
#! is plotted.
#! Default full width at half-maximum, in km/s, from Mocz et al. (2012; 
#! MNRAS 425, 296):
FWHM_v_def = 10**2.2
#! Speed of light in km/s:
c_km = 2.99792458e5

print("\nFull width at half-maximum, in km/s, used to \
represent emission lines?")
print("Default:", FWHM_v_def, "km/s.")
print("Either press <RETURN> to select the default \
value, or provide a number.")
FWHM_v = input()
if FWHM_v == "":
    FWHM_v = FWHM_v_def
else:
    FWHM_v = float(FWHM_v)
    pass
#! end if

#!======================================================================
#! Emission lines are plotted as spikes with an height computed assuming
#! a Gaussian profile for velocities, with a full width at half maximum
#! given by `FWHM_v`.
#! Compute bottom and top values for each emission line:

pos_line = int()
plotted = list()
for i_file in range(dim_file):
    plotted.append(struct_plot())
    plotted[i_file].y_line_bottom = np.empty((data[i_file].dim_output_age, 
                                        data[i_file].dim_line), dtype="float")
    plotted[i_file].y_line_top = np.empty((data[i_file].dim_output_age, 
                                        data[i_file].dim_line), dtype="float")
    for i_line in range(data[i_file].dim_line):
        pos_line = mi.bracket(data[i_file].dim_cont, data[i_file].lambda_cont, 
                           data[i_file].lambda_line[i_line])
        sigma = data[i_file].lambda_line[i_line]*FWHM_v \
                /(2*np.sqrt(2*np.log(2.)))/c_km
        for i_time in range(data[i_file].dim_output_age):
            plotted[i_file].y_line_bottom[i_time, i_line] \
                = mi.interp_log_log(data[i_file].lambda_cont[pos_line], \
                                 data[i_file].lambda_cont[pos_line+1], \
                                 data[i_file].lambda_cont[pos_line] \
                                 * data[i_file].lum_cont[i_time, pos_line], \
                                 data[i_file].lambda_cont[pos_line+1] \
                                 * data[i_file].lum_cont[i_time, pos_line+1], \
                                 data[i_file].lambda_line[i_line])
            plotted[i_file].y_line_top[i_time, i_line] \
                = plotted[i_file].y_line_bottom[i_time, i_line] \
                + data[i_file].lambda_line[i_line] \
                * data[i_file].L_line[i_time, i_line] / (np.sqrt(2*np.pi)*sigma)
            pass
        #! end for
        pass
    #! end for
    pass
#! end for

#!======================================================================
#! Determine default bounds for the plots.

x_min = np.finfo(float).max
x_max = 0
y_min = np.finfo(float).max
y_max = 0
for i_file in range(dim_file):
    x_min = min(x_min, data[i_file].lambda_cont[0])
    x_max = max(x_max, data[i_file].lambda_cont[data[i_file].dim_cont-1])
    for i_time in range(data[i_file].dim_output_age):
        for i_cont in range(data[i_file].dim_cont):
            if data[i_file].lum_cont[i_time, i_cont] > 0:
                y_min = min(y_min, data[i_file].lambda_cont[i_cont] 
                            * data[i_file].lum_cont[i_time, i_cont])
                y_max = max(y_max, data[i_file].lambda_cont[i_cont]
                            * data[i_file].lum_cont[i_time, i_cont])
                pass
            #! end if
            pass
        #! end for
        for i_line in range(data[i_file].dim_line):
            y_max = max(y_max, plotted[i_file].y_line_top[i_time, i_line])
            pass
        #! end for
        pass
    #! end for
    pass
#! end for

l10_x_min = np.log10(x_min)
l10_x_max = np.log10(x_max)
l10_y_min = np.log10(y_min)
l10_y_max = np.log10(y_max)

print("\nx-axis: log_10(lambda/angstroem).")
print("y-axis: log_10(lambda L_lambda/[erg s^-1/M_sys]).")
print("Default values of `x_min`, `x_max`, `y_min`, `y_max`:")
print(l10_x_min, l10_x_max, l10_y_min, l10_y_max)
print("Enter modified values separated by commas. An empty value is unchanged.")
print("Press <RETURN> after the last modified value \
to keep the remaining ones unchanged.")
row = input().split(",")
dim_col = len(row)
if dim_col > 0:
    if row[0] != "": 
        l10_x_min = float(row[0])
        pass
    #! end if
    if dim_col > 1:
        if row[1] != "": 
            l10_x_max = float(row[1])
            pass
        #! end if
        if dim_col > 2:
            if row[2] != "": 
                l10_y_min = float(row[2])
                pass
            #! end if
            if dim_col > 3:
                if row[3] != "": 
                    l10_y_max = float(row[3])
                    pass
                #! end if
                pass
            #! end if
            pass
        #! end if
        pass
    #! end if
    pass
#! end if

bottom_margin = 0
top_margin = 0.1
l10_y_min, l10_y_max \
    = (1.+bottom_margin)*l10_y_min - bottom_margin*l10_y_max, \
    -top_margin*l10_y_min + (1.+top_margin)*l10_y_max
x_min = 10**l10_x_min
x_max = 10**l10_x_max
y_min = 10**l10_y_min
y_max = 10**l10_y_max

#!======================================================================
#! Log-log plot of SEDs as a function of age for each file of spectra.

#! Colors used to plot SEDs, with cycling when `dim_file` > `dim_color`:
line_color = ["black", "red", "green", "blue"] #! Modify and complete 
#! this list as you want.
dim_color = len(line_color)

plt.ion()
for i_time in range(data[0].dim_output_age):
    print(data[0].output_age[i_time])
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel("$\lambda/\mathrm{\AA}$")
    plt.ylabel("$\lambda\,L_\lambda/(\mathrm{erg\,s^{-1}}/M_\mathrm{sys})$")
    for i_file in range(dim_file):
        #! Plot continuum:     
        plt.loglog(data[i_file].lambda_cont, \
                   data[i_file].lambda_cont*data[i_file].lum_cont[i_time,:],
                   line_color[i_file % dim_color])
        #! Plot emission lines:
        for i_line in range(data[i_file].dim_line):
            plt.loglog((data[i_file].lambda_line[i_line], \
                        data[i_file].lambda_line[i_line]), \
                       (plotted[i_file].y_line_bottom[i_time, i_line], \
                        plotted[i_file].y_line_top[i_time, i_line]),
                       line_color[i_file % dim_color])
            pass
        #! end for
        pass
    #! end for
    plt.pause(0.001) #! Needed to show the plot in some cases for some reason.
    print("Press the <RETURN>/<ENTER> key to jump to the next time.")
    input()
    plt.clf()
    pass
#! end for
