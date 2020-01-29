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
__updated__ = '2020-01-28'

import inspect
import json
import shutil
from decimal import Decimal
from datetime import date, timedelta, datetime as dt
import logging as lg

FXN_TIME_STR:str  = "%H:%M:%S:%f"
CELL_TIME_STR:str = "%H:%M:%S"
CELL_DATE_STR:str = "%Y-%m-%d"
FILE_DATE_STR:str = "D%Y-%m-%d"
FILE_TIME_STR:str = "T%Hh%M"
FILE_DATE_FORMAT  = FILE_DATE_STR + FILE_TIME_STR
RUN_DATE_FORMAT   = CELL_DATE_STR + '_' + FXN_TIME_STR
now_dt:dt         = dt.now()
run_ts:str        = now_dt.strftime(RUN_DATE_FORMAT)
print(F"run_ts = {run_ts}")
file_ts:str       = now_dt.strftime(FILE_DATE_FORMAT)
print(F"file_ts = {file_ts}")

BASE_PYTHON_FOLDER = '/newdata/dev/git/Python/'
YAML_CONFIG_FILE   = BASE_PYTHON_FOLDER + 'Utilities/logging.yaml'
LOG_BASENAME       = 'GnucashLog'
MONARCH_BASENAME   = 'GncTxsFromMonarch'
GOOGLE_BASENAME    = 'UpdateGoogleSheet'
STD_GNC_OUT_SUFFIX = '.gncout'

saved_log_info = list()


class SpecialFilter(lg.Filter):
    def filter(self, record):
        # SAVE A COPY OF LOG MESSAGES
        saved_log_info.append(str(record.msg) + '\n')
        return True


def finish_logging(logname:str, timestamp:str=file_ts, sfx:str=STD_GNC_OUT_SUFFIX):
    """change the standard log name to a time-stamped name to save each execution separately"""
    log_file = logname + '_' + timestamp + sfx
    print(F"finish logging to {log_file}")
    shutil.move(LOG_BASENAME, log_file)


ZERO:Decimal = Decimal(0)

# number of months
QTR_MONTHS:int = 3
YEAR_MONTHS:int = 12

ONE_DAY:timedelta = timedelta(days=1)


def get_current_time():
    return dt.now().strftime(CELL_DATE_STR + 'T' + FXN_TIME_STR)


def year_span(target_year:int, base_year:int, base_year_span:int, hdr_span:int, logger:lg.Logger=None) -> int:
    """
    calculate which row to update, factoring in the header row placed every so-many years
    :param    target_year: year to calculate for
    :param      base_year: starting year
    :param base_year_span: number of rows between equivalent positions in adjacent years, not including header rows
    :param       hdr_span: number of rows between header rows
    :param         logger
    """
    if logger: logger.debug(get_current_time())

    year_diff = int(target_year - base_year)
    hdr_adjustment = 0 if hdr_span <= 0 else (year_diff // int(hdr_span))
    return int(year_diff * base_year_span) + hdr_adjustment


def get_int_year(target_year:str, base_year:int, logger:lg.Logger=None) -> int:
    """
    convert the string representation of a year to an int
    :param target_year: to convert
    :param   base_year: earliest possible year
    :param      logger
    """
    if logger: logger.debug(get_current_time())

    if not target_year.isnumeric():
        msg = "Input MUST be the String representation of a Year, e.g. '2013'!"
        c_frame = inspect.currentframe().f_back
        if logger:
            logger.error(msg, c_frame)
        raise msg

    int_year = int(float(target_year))
    if int_year > now_dt.year or int_year < base_year:
        msg = F"Input MUST be the String representation of a Year between {now_dt.year} and {base_year}!"
        c_frame = inspect.currentframe().f_back
        if logger:
            logger.error(msg, c_frame)
        raise msg

    return int_year


def get_int_quarter(p_qtr:str, logger:lg.Logger=None) -> int:
    """
    convert the string representation of a quarter to an int
    :param   p_qtr: to convert
    :param  logger
    """
    if logger: logger.debug(get_current_time())
    msg = "Input MUST be a String of 0..4!"

    if not p_qtr.isnumeric():
        c_frame = inspect.currentframe().f_back
        if logger:
            logger.error(msg, c_frame)
        raise msg

    int_qtr = int(float(p_qtr))
    if int_qtr > 4 or int_qtr < 0:
        c_frame = inspect.currentframe().f_back
        if logger:
            logger.error(msg, c_frame)
        raise msg

    return int_qtr


def next_quarter_start(start_year:int, start_month:int, logger:lg.Logger=None) -> (int, int):
    """
    get the year and month that starts the FOLLOWING quarter
    :param  start_year
    :param start_month
    :param      logger
    """
    if logger: logger.debug(get_current_time())

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
    if logger: logger.info(get_current_time())

    end_year, end_month = next_quarter_start(start_year, start_month)

    # last step, the end date is one day back from the start of the next period
    # so we get a period end like 2010-03-31 instead of 2010-04-01
    return date(end_year, end_month, 1) - ONE_DAY


def generate_quarter_boundaries(start_year:int, start_month:int, num_qtrs:int,
                                logger:lg.Logger=None) -> (date, date):
    """
    get the start and end dates for the quarters in the submitted range
    :param  start_year
    :param start_month
    :param    num_qtrs: number of quarters to calculate
    :param      logger
    """
    if logger: logger.debug(get_current_time())

    for i in range(num_qtrs):
        yield date(start_year, start_month, 1), current_quarter_end(start_year, start_month)
        start_year, start_month = next_quarter_start(start_year, start_month)


def save_to_json(fname:str, json_data:object, ts:str=file_ts, indt:int=4) -> str:
    """
    print json data to a file -- add a timestamp to get a unique file name each run
    :param     fname: file name
    :param        ts: timestamp to use
    :param json_data: JSON compatible struct
    :param      indt: indentation amount
    :return: file name
    """
    out_file = 'json/' + fname + '_' + ts + '.json'
    fp = open(out_file, 'w')
    json.dump(json_data, fp, indent=indt)
    fp.close()
    return out_file
