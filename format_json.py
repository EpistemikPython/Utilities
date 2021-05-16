##############################################################################################################################
# coding=utf-8
#
# format_json.py -- format a JSON file with proper new lines and indents
#
# Copyright (c) 2019-21 Mark Sattolo <epistemik@gmail.com>
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = '3.6+'
__created__ = '2019-02-25'
__updated__ = '2021-05-15'

import sys
import json

if len(sys.argv) < 3:
    print(F"usage: python3 {sys.argv[0]} <JSON file> <indent>")
    exit()

# read the file
with open(sys.argv[1]) as file:
    content = json.loads( file.read() )

# dump output to nicely formatted JSON
print( json.dumps( content, indent = int(sys.argv[2]) ) )
