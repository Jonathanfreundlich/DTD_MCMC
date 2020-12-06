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

import sys

#!======================================================================

def skip_row(unit):
    unit.readline()
    return None
#! end def

#!======================================================================

def next_non_comment_line(unit):

    #! Skip comment lines (including blank lines) and return the first 
    #! non-comment line. 

    while True:
        row = unit.readline().strip()
        if row == "": break
        if row[0:2] != "!#": break
        pass
    #! end while

    return row

#! end def

#!======================================================================

def clean_string(input_string):
    output_string = input_string.strip().strip('"')
    return output_string
#! end def

#!======================================================================

def get_single_string(unit):
    string = clean_string(unit.readline().strip().replace('" ', '" , ').split(' , ')[0])
    return string
#! end def

#!======================================================================

def get_single_int(unit):
    return int(unit.readline().split()[0])
#! end def

#!======================================================================

def get_single_float(unit):
    return float(unit.readline().split()[0])
#! end def

#!======================================================================

def boolean(value):

    boolean = value.strip(".").upper()
    if boolean[0] == "T":
        boolean = True
    elif boolean[0] == "F":
        boolean = False
    else:
        print("`" + value + "` is not a boolean. Stopped.")
        sys.exit()
        pass
    #! end if
    return boolean

#! end def

#!======================================================================

def get_single_boolean(unit):

    value = boolean(unit.readline().split()[0])
    return value

#! end def
