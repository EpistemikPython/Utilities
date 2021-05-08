##############################################################################################################################
# coding=utf-8
#
# parse_args.py -- use ArgumentParser for command line variables
#
# Copyright (c) 2019-21 Mark Sattolo <epistemik@gmail.com>
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = '3.6+'
__created__ = '2019-08-30'
__updated__ = '2021-05-08'

from argparse import ArgumentParser

def test_args():
    found_args = ArgumentParser(description="xxx")
    # required arguments
    found_args.add_argument('filename', action='store', help='xxx')
    found_args.add_argument('runmode', action='store', help='prod OR test')
    return found_args

def main():
    args = test_args().parse_args()
    fname = args.filename
    mode = args.runmode.upper()
    print(F"filename = {fname}; mode = {mode}")


if __name__ == "__main__":
    main()
    exit()
