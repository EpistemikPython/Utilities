##############################################################################################################################
# coding=utf-8
#
# python_utilities.py -- useful classes, functions & constants
#
# some code from account_analysis.py by Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
#
# Copyright (c) 2020 Mark Sattolo <epistemik@gmail.com>
#
__author__         = 'Mark Sattolo'
__author_email__   = 'epistemik@gmail.com'
__python_version__ = '3.6.9'
__created__ = '2019-04-07'
__updated__ = '2020-04-09'

import inspect
import json
import shutil
from decimal import Decimal
from datetime import date, timedelta, datetime as dt
import logging as lg
import logging.config as lgconf
import yaml

FXN_TIME_STR:str  = "%H:%M:%S:%f"
CELL_TIME_STR:str = "%H:%M:%S"
CELL_DATE_STR:str = "%Y-%m-%d"
FILE_DATE_STR:str = "D%Y-%m-%d"
FILE_TIME_STR:str = "T%Hh%M"
FILE_DATE_FORMAT  = FILE_DATE_STR + FILE_TIME_STR
RUN_DATE_FORMAT   = CELL_DATE_STR + '_' + FXN_TIME_STR

now_dt:dt  = dt.now()
run_ts:str = now_dt.strftime(RUN_DATE_FORMAT)
print(F"{__file__}: run_ts = {run_ts}")
file_ts:str = now_dt.strftime(FILE_DATE_FORMAT)
print(F"{__file__}: file_ts = {file_ts}")

BASE_PYTHON_FOLDER = '/newdata/dev/git/Python/'
YAML_CONFIG_FILE   = BASE_PYTHON_FOLDER + 'Utilities/logging.yaml'
STD_GNC_OUT_SUFFIX = '.gncout'
saved_log_info = list()


class SpecialFilter(lg.Filter):
    """SAVE A COPY OF LOG MESSAGES"""
    def filter(self, record):
        saved_log_info.append(str(record.msg) + '\n')
        return True


# load the logging config
with open(YAML_CONFIG_FILE, 'r') as fp:
    LOG_CONFIG = yaml.safe_load(fp.read())
lgconf.dictConfig(LOG_CONFIG)
# print(json.dumps(LOG_CONFIG, indent=4))


def get_logger_filename(logger_name:str, posn:int=1) -> str:
    print(F"requested logger name = {logger_name}")
    handler = LOG_CONFIG.get('loggers').get(logger_name).get('handlers')[posn]
    print(F"handler = {handler}")
    return LOG_CONFIG.get('handlers').get(handler).get('filename')


def get_logger(logger_name:str) -> lg.Logger:
    print(F"requested logger = {logger_name}")
    return lg.getLogger(logger_name)


def finish_logging(logger_name:str, custom_log_name:str=None, timestamp:str=file_ts, sfx:str=STD_GNC_OUT_SUFFIX):
    """copy the standard log file to a customized named & time-stamped file to save each execution separately"""
    run_log_name = get_logger_filename(logger_name)
    if not custom_log_name:
        custom_log_name = run_log_name
    final_log_name = custom_log_name + '_' + timestamp + sfx
    print(F"finish logging to {run_log_name}")
    lg.shutdown() # need this to ensure get a NEW log file with next call of get_logger() to SAME logger
    shutil.move(run_log_name, final_log_name)
    print(F"move {run_log_name} to {final_log_name}")


ZERO:Decimal = Decimal(0)

# number of months
QTR_MONTHS:int = 3
YEAR_MONTHS:int = 12

ONE_DAY:timedelta = timedelta(days=1)


def get_current_time(time_indicator:str='T') -> str:
    return dt.now().strftime(CELL_DATE_STR + time_indicator + FXN_TIME_STR)


def get_base_filename(p_name:str, div1:str='/', div2:str='.') -> str:
    spl1 = p_name.split(div1)
    if spl1 and isinstance(spl1, list):
        spl2 = spl1[-1].split(div2)
        if spl2 and isinstance(spl2, list):
            return spl2[0]
    return ''


def year_span(target_year:int, base_year:int, yr_span:int, hdr_span:int, logger:lg.Logger=None) -> int:
    """
    calculate which row to update, factoring in the header row placed every so-many years
    :param target_year: year to calculate for
    :param   base_year: starting year in the sheet
    :param     yr_span: number of rows between equivalent positions in adjacent years, not including header rows
    :param    hdr_span: number of rows between header rows
    :param logger
    """
    if logger: logger.debug(F"target year = {target_year}; base year = {base_year}; year span = {yr_span}; header span = {hdr_span}")

    year_diff = int(target_year - base_year)
    hdr_adjustment = 0 if hdr_span <= 0 else (year_diff // int(hdr_span))
    return int(year_diff * yr_span) + hdr_adjustment


def get_int_year(target_year:str, base_year:int, logger:lg.Logger=None) -> int:
    """
    convert the string representation of a year to an int
    :param target_year: to convert
    :param   base_year: earliest possible year
    :param      logger
    """
    if logger: logger.debug(F"year = {target_year}; base year = {base_year}")

    if not target_year.isnumeric():
        msg = "Input MUST be the String representation of a Year, e.g. '2013'!"
        if logger:
            c_frame = inspect.currentframe().f_back
            logger.error(msg, c_frame)
        raise Exception(msg)

    int_year = int(float(target_year))
    if int_year > now_dt.year or int_year < base_year:
        msg = F"Input MUST be a Year between {now_dt.year} and {base_year}!"
        if logger:
            c_frame = inspect.currentframe().f_back
            logger.error(msg, c_frame)
        raise Exception(msg)

    return int_year


def get_int_quarter(p_qtr:str, logger:lg.Logger=None) -> int:
    """
    convert the string representation of a quarter to an int
    :param   p_qtr: to convert
    :param  logger
    """
    if logger: logger.debug(F"quarter to convert = {p_qtr}")
    msg = "Input MUST be a String of 0..4!"

    if not p_qtr.isnumeric():
        if logger:
            c_frame = inspect.currentframe().f_back
            logger.error(msg, c_frame)
        raise Exception(msg)

    int_qtr = int(float(p_qtr))
    if int_qtr > 4 or int_qtr < 0:
        if logger:
            c_frame = inspect.currentframe().f_back
            logger.error(msg, c_frame)
        raise Exception(msg)

    return int_qtr


def next_quarter_start(start_year:int, start_month:int, logger:lg.Logger=None) -> (int, int):
    """
    get the year and month that starts the FOLLOWING quarter
    :param  start_year
    :param start_month
    :param      logger
    """
    if logger: logger.debug(F"start year = {start_year}; start month = {start_month}")

    # add number of months for a Quarter
    next_month = start_month + QTR_MONTHS

    # use integer division to find out if the new end month is in a different year,
    # what year it is, and what the end month number should be changed to.
    next_year = start_year + ((next_month - 1) // YEAR_MONTHS)
    next_month = ((next_month - 1) % YEAR_MONTHS) + 1

    return next_year, next_month


def current_quarter_end(start_year:int, start_month:int, logger:lg.Logger=None) -> date:
    """
    get the date that ends the CURRENT quarter
    :param  start_year
    :param start_month
    :param      logger
    """
    if logger: logger.info(F"start year = {start_year}; start month = {start_month}")

    end_year, end_month = next_quarter_start(start_year, start_month)

    # last step, the end date is one day back from the start of the next period
    # so we get a period end like 2010-03-31 instead of 2010-04-01
    return date(end_year, end_month, 1) - ONE_DAY


def generate_quarter_boundaries(start_year:int, start_month:int, num_qtrs:int, logger:lg.Logger=None) -> (date, date):
    """
    get the start and end dates for the quarters in the submitted range
    :param  start_year
    :param start_month
    :param    num_qtrs: number of quarters to calculate
    :param      logger
    """
    if logger: logger.debug(F"start year = {start_year}; start month = {start_month}; num quarters = {num_qtrs}")

    for i in range(num_qtrs):
        yield date(start_year, start_month, 1), current_quarter_end(start_year, start_month)
        start_year, start_month = next_quarter_start(start_year, start_month)


def save_to_json(fname:str, json_data:object, ts:str=file_ts, indt:int=4, lgr:lg.Logger=None) -> str:
    """
    print json data to a file -- add a timestamp to get a unique file name each run
    :param     fname: base file name to use
    :param json_data: JSON compatible struct
    :param        ts: timestamp to use
    :param      indt: indentation amount
    :param       lgr: if desired
    :return: saved file name
    """
    out_file = 'json/' + fname + '_' + ts + '.json'
    if lgr: lgr.info(F"dump to json file: {out_file}")
    with open(out_file, 'w') as jfp:
        json.dump(json_data, jfp, indent=indt)
    return out_file
