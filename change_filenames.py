##############################################################################################################################
# coding=utf-8
#
# change_filenames.py
#   -- replace a selected string in file names with a new string
#
# Source - https://stackoverflow.com/a/24954254
# Posted by nicholas
# Retrieved 2026-09-18, License - CC BY-SA 3.0
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2026-09-18"
__updated__ = "2026-09-30"

import os
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_OLD_TERM = "results"
DEFAULT_NEW_TERM = "statistics"
DEFAULT_FOLDER = "."
TERM_MIN_LENGTH = 1
TERM_MAX_LENGTH = 13

def run():
    """Replace a selected string in file names with a new string."""
    ct = 0
    for root, dirnames, filenames in os.walk(target_folder):
        lgr.info(f"root: {root}; dirnames: {dirnames}")
        if dirnames:
            for subdir in dirnames:
                # DO NOT go into subdirs
                dirnames.remove(subdir)
        for oldname in filenames:
            lgr.debug(f"current file = '{oldname}'")
            if old_term in oldname:
                # OLD_TERM will be replaced by NEW_TERM in the filenames in the target folder
                newname = oldname.replace(old_term, new_term)
                if newname != oldname:
                    ct += 1
                    if test_run:
                        lgr.info(f"change '{oldname}' to '{newname}'")
                    else:
                        os.rename(osp.join(root,oldname), osp.join(root,newname))
                        lgr.info(f"renamed '{oldname}' to '{newname}'")
    lgr.info(f"Found {ct} matching filenames.")

def set_args():
    arg_parser = ArgumentParser(description = "replace a selected string in file names with a new string",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-t', '--test', action = "store_true", default = False,
                            help = "display the old and new filenames WITHOUT performing the change")
    arg_parser.add_argument('-f', '--folder', type = str, default = DEFAULT_FOLDER,
                            help = f"path to the folder to search for filenames to change; DEFAULT = '{DEFAULT_FOLDER}'")
    arg_parser.add_argument('-o', '--oldterm', type = str, default = DEFAULT_OLD_TERM,
                            help = f"string TO BE REPLACED in the target filenames; DEFAULT = '{DEFAULT_OLD_TERM}'")
    arg_parser.add_argument('-n', '--newterm', type = str, default = DEFAULT_NEW_TERM,
                            help = f"NEW STRING (can be empty) to put in the target filenames; DEFAULT = '{DEFAULT_NEW_TERM}'")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    targfolder = args.folder if osp.isdir(args.folder) else DEFAULT_FOLDER
    lgr.info(f"target folder = '{targfolder}'")
    # need at least one character to search and replace
    oldt = args.oldterm if TERM_MIN_LENGTH <= len(args.oldterm) <= TERM_MAX_LENGTH else DEFAULT_OLD_TERM
    lgr.info(f"old string = '{oldt}'")
    # can just eliminate existing strings by using '' as the replacement term
    newt = args.newterm if len(args.newterm) <= TERM_MAX_LENGTH else DEFAULT_NEW_TERM
    lgr.info(f"new string = '{newt}'")
    if newt == oldt:
        lgr.info(f">> New term '{newt}' is THE SAME as old term '{oldt}' !!??")
    return args.test, targfolder, oldt, newt


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        test_run, target_folder, old_term, new_term = get_args(argv[1:])
        run()
    except KeyboardInterrupt as mki:
        lgr.exception(mki)
        code = 13
    except ValueError as mve:
        lgr.exception(mve)
        code = 27
    except Exception as mex:
        lgr.exception(mex)
        code = 66
    lgr.info(f"Elapsed time = {(time.perf_counter() - start)*1000000} microseconds")
    exit(code)
