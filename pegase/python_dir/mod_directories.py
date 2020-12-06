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

#! Separator between directories:
dir_sep = "/"
#! (Replace "/" by "\" or the appropriate character if not under Linux/Unix.)

#! Identifier for the current working directory:
current_dir_id = "." + dir_sep

#! Identifiers for the root directory and the user's home directory:
root_dir_id = "/"
home_dir_id = "~/"
#! (Change them if not under Linux.
#! Do not forget the trailing directory separator.)

#! Path from the root directory to the user's home directory:
home_dir = "/absolute/path/to/home/directory/"
#! (Adapt this if you use `home_dir_id`.
#! Do not forget the trailing directory separator.)

#! Path to the top directory of Pégase.3:
#Pegase_3_dir = ".." + dir_sep + ".." + dir_sep + "Pegase.3.0.1" + dir_sep
Pegase_3_dir="/Users/jonathanf/Desktop/COLLABORATIONS/MAOZ/Pegase.3.0.1/"
#! (The path above is given relatively to the directory referred to by variable
#! `Python_dir` below, within which Python codes should normally be executed.
#! To run these from within another directory, set `Pegase_3_dir` to the
#! absolute path to the top directory of Pégase.3.
#! Do not forget the trailing directory separator.)

Python_dir = Pegase_3_dir + "Python_dir" + dir_sep

spectra_dir = Pegase_3_dir + "spectra_dir" + dir_sep

grain_temp_dir = Pegase_3_dir + "grain_temp_dir" + dir_sep

grain_SED_dir = Pegase_3_dir + "grain_SED_dir" + dir_sep

#!======================================================================

def path_file(dir_name, file_name):
    
    if file_name[:len(root_dir_id)] == root_dir_id:
        path_file = file_name
    elif file_name[:len(home_dir_id)] == home_dir_id:
        path_file = home_dir + file_name[len(home_dir_id):]
    elif file_name[:len(current_dir_id)] == current_dir_id:
        path_file = file_name
    else:
        path_file = dir_name + file_name
        pass
    #! end if

    return path_file

#! end def
