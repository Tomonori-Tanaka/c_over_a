"""
This script extract jij values.
"""
import argparse
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
            #jij_strage = np.append(jij_strage, jij_portion)
            jij_strage = np.vstack((jij_strage, jij_portion))

    return jij_strage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract jij values from AkaiKKR output (unit of Jij is meV).')

    phelp = "input filename (output file of AkaiKKR)"
    parser.add_argument('input_file', type=str, help=phelp)

    phelp = "number of nearest-neighbor pairs which you want."
    parser.add_argument('NN', type=int, help=phelp)

    args = parser.parse_args()

    input_file = args.input_file
    jij_ndarray = jij_extraction(input_file)

    print(jij_ndarray)
