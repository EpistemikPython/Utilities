##############################################################################################################################
# coding=utf-8
#
# mhsLogging.py -- custom logging
#
# Copyright (c) 2025 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2021-05-03"
__updated__ = "2025-08-06"

import logging
import logging.config
import yaml
import shutil
from mhsUtils import osp, PYTHON_UTIL_FOLDER, get_base_filename, dt, FILE_DATETIME_FORMAT

CONSOLE_FORMAT = "%(levelname)-8s | %(funcName)s[%(lineno)s]: %(message)s"
FILE_FORMAT    = "%(levelname)-8s | %(filename)-24s : %(funcName)-24s < %(lineno)-4s > %(message)s"
SIMPLE_FORMAT  = "%(levelname)-8s @ %(asctime)s | %(funcName)s # %(message)s"

# CRITICAL = 50
# ERROR    = 40
# WARNING  = 30
# INFO     = 20
# DEBUG    = 10
# NOTSET   = 0

DEFAULT_LOG_LEVEL:int     = logging.INFO
QUIET_LOG_LEVEL:int       = logging.CRITICAL
DEFAULT_FILE_LEVEL:int    = logging.DEBUG
DEFAULT_CONSOLE_LEVEL:int = logging.WARNING
DEFAULT_LOG_SUFFIX:str = "log"
DEFAULT_LOG_FOLDER:str = DEFAULT_LOG_SUFFIX + 's'

def get_level(levname:str):
    loglev = logging.getLevelName( levname.upper() )
    return loglev if isinstance(loglev, int) else None

class MhsLogger:
    saved_log_info = []

    # internal class
    class MhsLogFilter(logging.Filter):
        """Save a copy of log messages."""
        def filter(self, record):
            MhsLogger.saved_log_info.append( str(record.msg) + '\n' )
            return True

    def __init__(self, logger_name:str, con_level:int = DEFAULT_CONSOLE_LEVEL, file_level:int = DEFAULT_FILE_LEVEL,
                 folder:str = DEFAULT_LOG_FOLDER, file_time:str = dt.now().strftime(FILE_DATETIME_FORMAT),
                 suffix:str = DEFAULT_LOG_SUFFIX):
        basename = get_base_filename(logger_name)

        try:
            self.mhs_logger = logging.getLogger(basename)
            self.mhs_logger.setLevel(logging.DEBUG)
            self.console_hdlr = logging.StreamHandler()
            self.file_hdlr = logging.FileHandler(osp.join(folder, basename + '_' + file_time + osp.extsep + suffix))
            self.file_hdlr.addFilter( self.MhsLogFilter() )
        except Exception as iex:
            print(f"Problem during setup: {repr(iex)}")
            raise iex

        try:
            self.console_hdlr.setLevel(con_level)
            self.file_hdlr.setLevel(file_level)
        except ValueError as lve:
            print(f"Problem setting requested Levels: {repr(lve)}")
            self.console_hdlr.setLevel(DEFAULT_CONSOLE_LEVEL)
            self.file_hdlr.setLevel(DEFAULT_FILE_LEVEL)
        except Exception as ilx:
            print(f"Problem setting default Levels: {repr(ilx)}")
            raise ilx

        try:
            # create formatters and add to the handlers
            con_formatter  = logging.Formatter(CONSOLE_FORMAT)
            file_formatter = logging.Formatter(FILE_FORMAT)
            self.console_hdlr.setFormatter(con_formatter)
            self.file_hdlr.setFormatter(file_formatter)

            # add handlers to the logger
            self.mhs_logger.addHandler(self.console_hdlr)
            self.mhs_logger.addHandler(self.file_hdlr)
        except Exception as fex:
            print(f"Problem setting Formatters or adding Handlers: {repr(fex)}")
            raise fex

        self.mhs_logger.log(file_level, f"FINISHED {self.__class__.__name__} init.")

    def get_logger(self):
        return self.mhs_logger

    def get_saved_info(self):
        return self.saved_log_info

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

    def logl(self, level, msg):
        self.mhs_logger.log(level, msg)

    def log_list(self, items:list, level:int, newl = ''):
        for item in items:
            self.mhs_logger.log( level = level, msg = newl + str(item) )

    def show(self, msg, level = DEFAULT_LOG_LEVEL, endl = '\n'):
        """print and log."""
        print(msg, end = endl)
        self.mhs_logger.log(level, msg)
# END class MhsLogger


#
#  Simple logger
########################################
def get_simple_logger(logger_name:str, level = DEFAULT_LOG_LEVEL, file_handling = True,
                      file_time:str = dt.now().strftime(FILE_DATETIME_FORMAT)) -> logging.Logger:
    basename = get_base_filename(logger_name)
    lgr = logging.getLogger(basename)
    # default for logger: all messages DEBUG or higher
    lgr.setLevel(logging.DEBUG)

    ch = logging.StreamHandler() # console handler
    try:
        ch.setLevel(level) # try to log to console at the level requested on the command line
    except ValueError:
        ch.setLevel(DEFAULT_LOG_LEVEL)
    formatter = logging.Formatter(SIMPLE_FORMAT)
    ch.setFormatter(formatter)
    lgr.addHandler(ch)

    if file_handling:
        fh = logging.FileHandler( osp.join(DEFAULT_LOG_FOLDER, basename + '_' + file_time + osp.extsep + DEFAULT_LOG_SUFFIX) )
        fh.setLevel(DEFAULT_FILE_LEVEL)
        fh.setFormatter(formatter)
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
