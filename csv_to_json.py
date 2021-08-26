##############################################################################################################################
# coding=utf-8
#
# csv_to_json.py -- convert a CSV file to a JSON file with proper new lines and indents
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = '3.6+'
__created__ = '2021-08-26'
__updated__ = '2021-08-26'

import sys
import csv
import json

def main_csv_to_json(csv_file:str, json_file:str, p_json_idt:str):
    try:
        json_indent = int(p_json_idt)
    except ValueError:
        print(F"bad json indent = {p_json_idt}; Using default value = 4.")
        json_indent = 4

    try:
        # read the CSV file
        with open(csv_file) as fc:
            reader = csv.DictReader(fc)
            rows = list(reader)

        # dump output to nicely formatted JSON
        with open(json_file, 'x') as fj:
            json.dump(rows, fj, indent = json_indent)

    except FileNotFoundError as fnfe:
        raise fnfe


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(F"usage: python3 {sys.argv[0]} <CSV file> <JSON file> <indent>")
    else:
        main_csv_to_json( sys.argv[1], sys.argv[2], sys.argv[3] )
        print("Program finished.")
    exit()
