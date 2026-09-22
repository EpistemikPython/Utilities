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
__updated__ = "2026-09-19"

import os

TARGET_FOLDER = "."
OLD_TERM = "results"
NEW_TERM = "statistics"

for _, _, filenames in os.walk(TARGET_FOLDER):
    for oldname in filenames:
        print(oldname)
        # OLD_TERM will be replaced by NEW_TERM in the filenames in the current folder
        newname = oldname.replace(OLD_TERM, NEW_TERM)
        if newname != oldname:
            print(f"changing '{oldname}' to '{newname}'.")
            os.rename(oldname, newname)
