##############################################################################################################################
# coding=utf-8
#
# mhsLogging.py -- custom logging
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2021-05-03"
__updated__ = "2021-05-11"

import logging
import logging.config as lgconf
import yaml
import shutil
import os.path as osp
from datetime import datetime as dt
import mhsUtils

FXN_TIME_STR:str  = "%H:%M:%S:%f"
CELL_TIME_STR:str = "%H:%M:%S"
CELL_DATE_STR:str = "%Y-%m-%d"
FILE_DATE_STR:str = "D%Y-%m-%d"
FILE_TIME_STR:str = "T%H-%M-%S"
FILE_DATETIME_FORMAT = FILE_DATE_STR + FILE_TIME_STR
RUN_DATETIME_FORMAT  = CELL_DATE_STR + '_' + FXN_TIME_STR

now_dt:dt   = dt.now()
run_ts:str  = now_dt.strftime(RUN_DATETIME_FORMAT)
file_ts:str = now_dt.strftime(FILE_DATETIME_FORMAT)

YAML_CONFIG_FILE   = osp.join(mhsUtils.PYTHON_UTIL_FOLDER, "logging" + osp.extsep + "yaml")

SIMPLE_FORMAT:str  = "%(levelname)-8s - %(filename)s[%(lineno)s]: %(message)s"
COMPLEX_FORMAT:str = "%(levelname)-8s | %(filename)-16s : %(funcName)-24s l.%(lineno)-4s > %(message)s"

DEFAULT_FILE_LEVEL    = logging.DEBUG
DEFAULT_CONSOLE_LEVEL = logging.WARNING

DEFAULT_LOG_LEVEL = logging.INFO
QUIET_LOG_LEVEL   = logging.CRITICAL

saved_log_info = list()


def get_simple_logger(filename:str, level:str=DEFAULT_LOG_LEVEL, file_time:str=file_ts) -> logging.Logger:
    basename = mhsUtils.get_base_filename(filename)
    lgr = logging.getLogger(basename)
    # default for logger: all messages DEBUG or higher
    lgr.setLevel(logging.DEBUG)

    fh = logging.FileHandler("logs/" + basename + '_' + file_time + ".log")
    # default for file handler: all messages DEBUG or higher
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler() # console handler
    # log to console at the level requested on the command line
    try:
        ch.setLevel(level)
    except ValueError:
        ch.setLevel(DEFAULT_LOG_LEVEL)

    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(levelname)s - %(asctime)s | %(funcName)s > %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add handlers to the logger
    lgr.addHandler(ch)
    lgr.addHandler(fh)
    return lgr


class MhsLogger:
    saved_log_info = list()

    class MhsLogFilter(logging.Filter):
        """Save a copy of log messages."""
        def filter(self, record):
            MhsLogger.saved_log_info.append(str(record.msg) + '\n')
            return True

    def __init__( self, basename:str, con_level=DEFAULT_CONSOLE_LEVEL, file_level=DEFAULT_FILE_LEVEL,
                  folder="logs", suffix="log" ):

        self.mhs_logger = logging.getLogger(basename)
        # default for logger: all messages DEBUG or higher
        self.mhs_logger.setLevel(logging.DEBUG)

        self.con_hdlr  = logging.StreamHandler()  # console handler
        self.file_hdlr = logging.FileHandler(folder + osp.sep + basename + '_' + file_ts + osp.extsep + suffix)

        try:
            self.con_hdlr.setLevel(con_level)
            self.file_hdlr.addFilter( self.MhsLogFilter() )
            self.file_hdlr.setLevel(file_level)
        except ValueError:
            self.con_hdlr.setLevel(DEFAULT_CONSOLE_LEVEL)
            self.file_hdlr.setLevel(DEFAULT_FILE_LEVEL)

        # create formatters and add to the handlers
        con_formatter  = logging.Formatter(SIMPLE_FORMAT)
        file_formatter = logging.Formatter(COMPLEX_FORMAT)
        self.con_hdlr.setFormatter(con_formatter)
        self.file_hdlr.setFormatter(file_formatter)

        # add handlers to the logger
        self.mhs_logger.addHandler(self.con_hdlr)
        self.mhs_logger.addHandler(self.file_hdlr)

    def get_logger(self):
        return self.mhs_logger

    def append(self, msg:str):
        self.saved_log_info.append( msg + '\n' )

    def get_saved_info(self):
        return self.saved_log_info

    def send_saved_info(self):
        self.log_list(self.saved_log_info)

    def log_list(self, items:list, newl=''):
        for item in items:
            self.mhs_logger.log( self.file_hdlr.level, newl + str(item) )

    def show(self, msg:str, level=logging.INFO, endl='\n'):
        """ print and log """
        print(msg, end = endl)
        if self.mhs_logger:
            self.mhs_logger.log(level, msg)

    def debug(self, msg:str):
        if self.mhs_logger:
            self.mhs_logger.debug(msg)

# END class MhsLogger


class SpecialFilter(logging.Filter):
    """SAVE A COPY OF LOG MESSAGES"""
    def filter(self, record):
        saved_log_info.append(str(record.msg) + '\n')
        return True


# load the logging config
with open(YAML_CONFIG_FILE, 'r') as fp:
    LOG_CONFIG = yaml.safe_load(fp.read())
# print(json.dumps(LOG_CONFIG, indent=4))


def get_special_logger(logger_name:str) -> logging.Logger:
    lgconf.dictConfig(LOG_CONFIG)
    print(F"requested logger = {logger_name}")
    return logging.getLogger(logger_name)


def get_spec_lgr_filename(logger_name:str, posn:int=1) -> str:
    print(F"requested logger name = {logger_name}")
    handler = LOG_CONFIG.get("loggers").get(logger_name).get("handlers")[posn]
    print(F"handler = {handler}")
    return LOG_CONFIG.get("handlers").get(handler).get("filename")


def finish_special_logging(logger_name:str, custom_log_name:str=None, timestamp:str=file_ts, sfx:str="log"):
    """copy the standard log file to a customized named & time-stamped file to save each execution separately"""
    run_log_name = get_spec_lgr_filename(logger_name)
    custom_name = custom_log_name if custom_log_name else run_log_name
    final_log_name = custom_name + '_' + timestamp + osp.extsep + sfx
    print(F"finish logging to {run_log_name}")
    logging.shutdown() # need this to ensure get a NEW log file with next call of get_logger() from SAME file
    shutil.move(run_log_name, final_log_name)
    print(F"move {run_log_name} to {final_log_name}")
