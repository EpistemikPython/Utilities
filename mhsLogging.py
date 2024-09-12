##############################################################################################################################
# coding=utf-8
#
# mhsLogging.py -- custom logging
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2021-05-03"
__updated__ = "2024-09-12"

import logging
import logging.config
import yaml
import shutil
from mhsUtils import osp, PYTHON_UTIL_FOLDER, get_base_filename, dt, FILE_DATETIME_FORMAT

CONSOLE_FORMAT = "%(levelname)-8s | %(filename)s[%(lineno)s]: %(message)s"
FILE_FORMAT    = "%(levelname)-8s | %(filename)-24s : %(funcName)-24s < %(lineno)-4s > %(message)s"
SIMPLE_FORMAT  = "%(levelname)-8s @ %(asctime)s | %(funcName)s > %(message)s"

DEFAULT_LOG_LEVEL = logging.INFO
QUIET_LOG_LEVEL   = logging.CRITICAL
DEFAULT_FILE_LEVEL    = logging.DEBUG
DEFAULT_CONSOLE_LEVEL = logging.WARNING
DEFAULT_LOG_SUFFIX = "log"
DEFAULT_LOG_FOLDER = "logs"


class MhsLogger:
    saved_log_info = []

    # internal class
    class MhsLogFilter(logging.Filter):
        """Save a copy of log messages."""
        def filter(self, record):
            MhsLogger.saved_log_info.append( str(record.msg) + '\n' )
            return True

    def __init__(self, logger_name:str, con_level:logging = DEFAULT_CONSOLE_LEVEL, file_level:logging = DEFAULT_FILE_LEVEL,
                 folder:str = DEFAULT_LOG_FOLDER, file_time:str = dt.now().strftime(FILE_DATETIME_FORMAT),
                 suffix:str = DEFAULT_LOG_SUFFIX):
        basename = get_base_filename(logger_name)

        try:
            self.mhs_logger = logging.getLogger(basename)
            # default for logger: all messages DEBUG or higher
            self.mhs_logger.setLevel(logging.DEBUG)
            self.con_hdlr  = logging.StreamHandler() # console handler
            self.file_hdlr = logging.FileHandler(osp.join(folder, basename + '_' + file_time + osp.extsep + suffix))
            self.file_hdlr.addFilter( self.MhsLogFilter() )
        except Exception as iex:
            print(f"Problem during setup: {repr(iex)}")
            raise iex

        try:
            self.con_hdlr.setLevel(con_level)
            self.file_hdlr.setLevel(file_level)
        except ValueError:
            self.con_hdlr.setLevel(DEFAULT_CONSOLE_LEVEL)
            self.file_hdlr.setLevel(DEFAULT_FILE_LEVEL)
        except Exception as ilx:
            print(f"Problem setting Levels: {repr(ilx)}")

        try:
            # create formatters and add to the handlers
            con_formatter  = logging.Formatter(CONSOLE_FORMAT)
            file_formatter = logging.Formatter(FILE_FORMAT)
            self.con_hdlr.setFormatter(con_formatter)
            self.file_hdlr.setFormatter(file_formatter)

            # add handlers to the logger
            self.mhs_logger.addHandler(self.con_hdlr)
            self.mhs_logger.addHandler(self.file_hdlr)
        except Exception as fex:
            print(f"Problem setting Formatters or adding Handlers: {repr(fex)}")
            raise fex

        self.mhs_logger.info(f"FINISHED {self.__class__.__name__} init.")

    def get_logger(self):
        return self.mhs_logger

    def append(self, msg:str):
        self.saved_log_info.append( msg + '\n' )

    def get_saved_info(self):
        return self.saved_log_info

    def send_saved_info(self):
        self.log_list(self.saved_log_info)

    def log_list(self, items:list, newl = ''):
        for item in items:
            self.mhs_logger.log( self.file_hdlr.level, newl + str(item) )

    def error(self, msg):
        self.mhs_logger.error(msg)

    def exception(self, msg):
        self.mhs_logger.exception(msg)

    def warning(self, msg):
        self.mhs_logger.warning(msg)

    def info(self, msg):
        self.mhs_logger.info(msg)

    def debug(self, msg):
        self.mhs_logger.debug(msg)

    def logl(self, msg, level = DEFAULT_LOG_LEVEL):
        self.mhs_logger.log(level, msg)

    def show(self, msg, level = DEFAULT_LOG_LEVEL, endl = '\n'):
        """print and log."""
        print(msg, end = endl)
        self.mhs_logger.log(level, msg)
# END class MhsLogger


#
#  Simple logger
########################################
def get_simple_logger(logger_name:str, level = DEFAULT_LOG_LEVEL,
                      file_time:str = dt.now().strftime(FILE_DATETIME_FORMAT)) -> logging.Logger:
    basename = get_base_filename(logger_name)
    lgr = logging.getLogger(basename)
    # default for logger: all messages DEBUG or higher
    lgr.setLevel(logging.DEBUG)

    fh = logging.FileHandler( osp.join(DEFAULT_LOG_FOLDER, basename + '_' + file_time + osp.extsep + DEFAULT_LOG_SUFFIX) )
    # default for file handler: all messages DEBUG or higher
    fh.setLevel(DEFAULT_FILE_LEVEL)

    ch = logging.StreamHandler() # console handler
    # log to console at the level requested on the command line
    try:
        ch.setLevel(level)
    except ValueError:
        ch.setLevel(DEFAULT_LOG_LEVEL)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(SIMPLE_FORMAT)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add handlers to the logger
    lgr.addHandler(ch)
    lgr.addHandler(fh)
    return lgr


#
#  Special logger
########################################
YAML_CONFIG_FILE:str = osp.join( PYTHON_UTIL_FOLDER, "logging" + osp.extsep + "yaml" )
special_log_info = []
log_config = None


class SpecialFilter(logging.Filter):
    """SAVE A COPY OF LOG MESSAGES"""
    def filter(self, record):
        special_log_info.append(str(record.msg) + '\n')
        return True


def get_special_logger(logger_name:str) -> logging.Logger:
    # load the logging config
    global log_config
    with open(YAML_CONFIG_FILE) as fp:
        log_config = yaml.safe_load(fp.read())
    logging.config.dictConfig(log_config)
    print(f"requested logger = {logger_name}")
    return logging.getLogger(logger_name)

# noinspection PyUnresolvedReferences
def get_spec_lgr_filename(logger_name:str, posn:int = 1) -> str:
    print(f"requested logger name = {logger_name}")
    if log_config:
        handler = log_config.get("loggers").get(logger_name).get("handlers")[posn]
        print(f"handler = {handler}")
        return log_config.get("handlers").get(handler).get("filename")
    print("log_config not available yet?!")
    return ""

def finish_special_logging(logger_name:str, custom_log_name:str = None,
                           timestamp:str = dt.now().strftime(FILE_DATETIME_FORMAT), sfx:str = DEFAULT_LOG_SUFFIX):
    """copy the standard log file to a customized named & time-stamped file to save each execution separately"""
    run_log_name = get_spec_lgr_filename(logger_name)
    custom_name = custom_log_name if custom_log_name else run_log_name
    final_log_name = custom_name + '_' + timestamp + osp.extsep + sfx
    print(f"finish logging to {run_log_name}")
    logging.shutdown() # need this to ensure get a NEW log file with next call of get_special_logger() from SAME file
    shutil.move(run_log_name, final_log_name)
    print(f"move {run_log_name} to {final_log_name}")
