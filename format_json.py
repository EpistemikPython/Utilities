
# format a JSON file with proper new lines and indents

import sys
import json

if len(sys.argv) < 3:
	print("usage: python {} <JSON file> <indent>".format(sys.argv[0]))
	sys.exit()

# read the file
with open(sys.argv[1]) as file:
	content = json.loads( file.read() )

# dump output to nicely formatted JSON
print( json.dumps( content, indent=int(sys.argv[2]) ) )
