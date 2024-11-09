##############################################################################################################################
# coding=utf-8
#
# format_json.py
#   -- format a JSON file with proper new lines and indents
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>
#
__author__         = 'Mark Sattolo'
__author_email__   = 'epistemik@gmail.com'
__python_version__ = '3.6+'
__created__ = '2019-02-25'
__updated__ = '2024-11-09'

from sys import argv
import json
from mhsUtils import osp, save_to_json, get_base_filename, JSON_LABEL

DEFAULT_INDENT = 4
MAX_INDENT = 16
USAGE = f"Usage: python3 {get_base_filename(argv[0])} 'path to input {JSON_LABEL} file' <indent, DEFAULT = {DEFAULT_INDENT}>"

def run():
    print(f"argv = {argv}")
    if len(argv) < 2:
        print(USAGE)
        raise Exception("NO file name.")
    elif argv[1] == "-h":
        print(USAGE)
        return
    elif osp.isfile(argv[1]):
        filename = argv[1]
    else:
        print(USAGE)
        raise Exception("BAD file name.")

    jndent = DEFAULT_INDENT
    if len(argv) > 2:
        ix = int(argv[2])
        if 1 <= ix <= MAX_INDENT: jndent = ix

    # read the file
    with open(filename) as jfile:
        content = json.loads( jfile.read() )

    # dump output to newly formatted JSON file
    print(f"new {JSON_LABEL} file = {save_to_json(get_base_filename(filename), content, indt = jndent)}" )


if __name__ == "__main__":
    code = 0
    try:
        run()
    except KeyboardInterrupt as mki:
        print( repr(mki) )
        code = 13
    except ValueError as mve:
        print( repr(mve) )
        code = 27
    except Exception as mex:
        print( repr(mex) )
        code = 66
    print("Program finished.")
    exit(code)
