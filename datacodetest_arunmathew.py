#
# Script based on README.md
# Author: Arun Mathew
#

import json
import random
import string
import struct
import sys
import csv

def gen_fw_file(spec_file, fw_file, row_count):
    with open(spec_file) as f:
        spec = json.load(f)

    columns = spec['ColumnNames']
    f_widths = list(map(int,spec['Offsets']))
    letters = string.ascii_lowercase

    # open file in write mode 
    fw =  open(fw_file, 'w', encoding=spec['FixedWidthEncoding'])

    # write header row to file
    if spec['IncludeHeader'] == 'True':
        # generate header row
        fw_row = ''.join("%*s" % j for j in zip(f_widths, columns)) + '\n'
        fw.write(fw_row)

    # loop through to generate fixed width data rows
    for i in range(row_count):
        field_val_arr = []

        # generate fixed with columns and concatenate to form the full row
        for k in  range(len(columns)):
            field_str = 'R' + str(i) + 'C' + str(k)
            field_str = field_str + ''.join(random.choice(letters) for l in range(f_widths[k]))
            field_val_arr.append(field_str[0:f_widths[k]])

        fw_row = ""
        fw_row = fw_row.join("%*s" % j for j in zip(f_widths, field_val_arr)) +  '\n'

        # append to fixed width row to file
        fw.write(fw_row)

    fw.close()


def gen_csv_from_fw(spec_file, fw_file, csv_file):
    with open(spec_file) as f:
        spec = json.load(f)

    f_widths = list(map(int,spec['Offsets']))

    fw_data = open(fw_file, 'r', encoding=spec['FixedWidthEncoding'])

    # open csv file
    csv_data = open(csv_file, 'w', newline='', encoding=spec['DelimitedEncoding'])
    csv_writer = csv.writer(csv_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # create field mapping
    fmtstring = ' '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's')
        for fw in f_widths)
    fieldstruct = struct.Struct(fmtstring)

    # loop through  fixed width file
    for line in fw_data:
        if sys.version_info[0] < 3:
            parse = fieldstruct.unpack_from
        else:
            # converts unicode input to byte string and results back to unicode string
            unpack = fieldstruct.unpack_from
            parse = lambda line: tuple(s.decode() for s in unpack(line.encode()))

        fields = parse(line)

        # remove spaces
        fields = [x.strip(' ') for x in fields]
        #print('fields: {}'.format(fields))

        # write to csv file
        csv_writer.writerow(fields)

    csv_data.close()
    fw_data.close()
    
def main():
    spec_file = 'spec.json'
    fw_file = 'fw_data.txt'
    csv_file =  'csv_data.csv'
    row_count  =  10
    # read spec file and generate fixed width file
    gen_fw_file(spec_file, fw_file, row_count)
    # parse fixed width file and generate to csv file
    gen_csv_from_fw(spec_file, fw_file, csv_file)

if __name__ == "__main__":
    main()