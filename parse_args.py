
from argparse import ArgumentParser

def test_args():
	found_args = ArgumentParser(description="xxx")
	# required arguments
	found_args.add_argument('filename', action=store, help='xxx')
	found_args.add_argument('runmode', action=store, help='prod OR test')
	return found_args

def main():
	args = test_args().parse_args()
	
	fname = args.filename
	
	mode = args.runmode.upper()
