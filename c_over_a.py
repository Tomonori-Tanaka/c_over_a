import argparse
import os
import re
import shutil

import numpy as np


def calc_lat_constant(volume, c_over_a):
    return round((volume / c_over_a) ** (1 / 3), 6)

parser = argparse.ArgumentParser(description='automation program for c/a from bcc to fcc')

phelp = 'lattice constant in bcc structure'
parser.add_argument('a_bcc', type=float, help=phelp)

phelp = 'initial value of c/a'
parser.add_argument('initial_c_a', type=float, help=phelp)

phelp = 'end value of c/a'
parser.add_argument('end_c_a', type=float, help=phelp)

phelp = 'division number'
parser.add_argument('division_num', type=int, help=phelp)

phelp = 'input kkr file'
parser.add_argument('input_file', help=phelp)

args = parser.parse_args()

c_over_a_ndarray = np.linspace(args.initial_c_a, args.end_c_a, args.division_num, endpoint=True)

for c_over_a in c_over_a_ndarray:
    with open(args.input_file, encoding='utf-8') as f:
        c_over_a = round(c_over_a, 6)
        body = f.read()
        body = re.sub('XXX', str(calc_lat_constant(args.a_bcc ** 3, c_over_a)), body)
        body = re.sub('YYY', str(c_over_a), body)
    try:
        os.mkdir('{0:.6f}'.format(c_over_a))
    except:
        print('{0:.6f} directory already exists. We skip it.'.format(c_over_a))
        continue
    with open('tmp.dat', mode='w', encoding='utf-8') as f:
        f.write(body)
    shutil.move('./tmp.dat', './{0:.6f}/kkrin.dat'.format(c_over_a))
    shutil.move('./job.sh', './{0:.6f}/'.format(c_over_a))

