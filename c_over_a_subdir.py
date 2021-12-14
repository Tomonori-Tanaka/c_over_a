import argparse
import os
import re
import shutil

import numpy as np


def calc_lat_constant(volume, c_over_a):
    return round((volume / c_over_a) ** (1 / 3), 6)

parser = argparse.ArgumentParser(description='automation program for c/a from bcc to fcc')

phelp = 'initial value of c/a'
parser.add_argument('initial_c_a', type=float, help=phelp)

phelp = 'end value of c/a'
parser.add_argument('end_c_a', type=float, help=phelp)

phelp = 'division number'
parser.add_argument('division_num', type=int, help=phelp)

phelp = 'input kkr file'
parser.add_argument('input_file', help=phelp)

phelp = 'go keyword for sub dirctory'
parser.add_argument('go_keyword', help=phelp)

args = parser.parse_args()

c_over_a_ndarray = np.linspace(args.initial_c_a, args.end_c_a, args.division_num, endpoint=True)
# dirctory representation is "/**/**/**" .
current_path = os.getcwd()
for c_over_a in c_over_a_ndarray:
    c_over_a = round(c_over_a, 6)
    str_c_over_a = "{0:.6f}".format(c_over_a)
    file_path = current_path + "/" + str_c_over_a + "/" + args.input_file
    with open(file_path, encoding='utf-8') as f:
        body = f.read()
        body = re.sub('go', args.go_keyword, body)
    subdir_path = current_path + "/" + str_c_over_a + "/" + args.go_keyword
    try:
        os.mkdir(subdir_path)
    except:
        print('{0} directory already exists. We skip it.'.format(subdir_path))
        continue
    newfile_path = subdir_path + "/" + args.input_file
    with open(newfile_path, mode='w', encoding='utf-8') as f:
        f.write(body)
    shutil.copy('./job.sh', subdir_path)
    shutil.copy(subdir_path + "/../potential.data", subdir_path)

