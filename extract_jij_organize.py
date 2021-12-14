"""
This script extract jij values.
"""
import argparse
import os
from itertools import islice

import numpy as np
# global variables
from numpy import ndarray

lattice_factor_keyword = "brvtyp="
jij_detect_keyword_begin = "index   site    comp"
jij_detect_keyword_end = "Tc (in mean field approximation)"
bohr2ang = 0.5291772109


def jij_extraction(filepath):
    with open(filepath, mode='r', encoding='utf-8') as f:
        linecount = 0
        for line in f:
            # extract lattice factor (a in angstrom)
            if lattice_factor_keyword in line:
                lattice_factor = float(line.split()[2]) * bohr2ang

            # extract jij values and store them to jij_dict
            if jij_detect_keyword_begin in line:
                jij_start_line = linecount + 1
            if jij_detect_keyword_end in line:
                jij_end_line = linecount - 1
            linecount += 1
    jij_strage = np.empty((0, 4))
    with open(filepath, mode='r', encoding='utf-8') as f:
        for line in islice(f, jij_start_line, jij_end_line):
            distance_fractional = float(line.split()[8])
            distance_ang = float(line.split()[8]) * lattice_factor
            jij_value = float(line.split()[10])
            jij_portion: ndarray = np.array([lattice_factor, distance_fractional, distance_ang, jij_value])
            # jij_strage = np.append(jij_strage, jij_portion)
            jij_strage = np.vstack((jij_strage, jij_portion))

    return jij_strage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract jij values from AkaiKKR output (unit of Jij is meV).')

    phelp = "input filename (output file of AkaiKKR)"
    parser.add_argument('input_file', type=str, help=phelp)

    phelp = "nearest-neighbor pair which you want."
    parser.add_argument('NN', type=int, help=phelp)

    args = parser.parse_args()

    # get current directory "/**/**/**"
    current_dir = os.getcwd()
    # get the list of the directories in the current directory.
    files = os.listdir(current_dir)
    # remove hidden directories from the directory list
    files_dir = [f for f in files if os.path.isdir(os.path.join(current_dir, f))]
    files_dir.sort()

    for dir in files_dir:
        path_jij_dir = current_dir + "/" + dir + "/j"
        if os.path.exists(path_jij_dir):
            path_jij_file = path_jij_dir + "/" + args.input_file
            jij_ndarray = jij_extraction(path_jij_file)
            print(dir,
                  "\t", round(float(jij_ndarray[args.NN - 1][2]), 6),
                  "\t", round(float(jij_ndarray[args.NN - 1][3]), 6))
        else:
            continue
