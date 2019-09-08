##############################################################################################################################
# coding=utf-8
#
# python_utilities.py -- useful classes, functions & constants
#
# some code from account_analysis.py by Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
#
# Copyright (c) 2019 Mark Sattolo <epistemik@gmail.com>
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = 3.6
__created__ = '2019-04-07'
__updated__ = '2019-09-08'

import inspect
import json
from decimal import Decimal
from datetime import date, timedelta, datetime as dt
from types import FrameType

CELL_TIME_STR:str = "%H:%M:%S"
FILE_DATE_STR:str = "%Y-%m-%d"
FILE_TIME_STR:str = "T%H-%M-%S"
today:dt = dt.now()
now:str  = today.strftime(FILE_DATE_STR + FILE_TIME_STR)

DATE_STR_FORMAT = "\u0023%Y-%m-%d\u0025\u0025%H-%M-%S"
dtnow  = dt.now()
strnow = dtnow.strftime(DATE_STR_FORMAT)

ZERO:Decimal = Decimal(0)

# number of months
QTR_MONTHS:int = 3
YEAR_MONTHS:int = 12

ONE_DAY:timedelta = timedelta(days=1)

COLOR_FLAG:str = '\x1b['
RED:str     = COLOR_FLAG + '31m'
GREEN:str   = COLOR_FLAG + '32m'
BROWN:str   = COLOR_FLAG + '33m'
BLUE:str    = COLOR_FLAG + '34m'
MAGENTA:str = COLOR_FLAG + '35m'
CYAN:str    = COLOR_FLAG + '36m'
BR_RED:str   = COLOR_FLAG + '91m'
BR_GREEN:str = COLOR_FLAG + '92m'
YELLOW:str   = COLOR_FLAG + '93m'
BR_BLUE:str  = COLOR_FLAG + '94m'
PINK:str     = COLOR_FLAG + '95m'
BR_CYAN:str  = COLOR_FLAG + '96m'
BLACK:str     = COLOR_FLAG + '30m'
GREY:str      = COLOR_FLAG + '90m'
WHITE:str     = COLOR_FLAG + '37m'
COLOR_OFF:str = COLOR_FLAG + '0m'


class SattoLog:
    def __init__(self, my_color:str=BLACK, do_logging:bool=False):
        self.debug = do_logging
        self.color = my_color
        self.log_text = []

    def append(self, obj:object):
        if isinstance(obj, str):
            self.log_text.append(obj)
        else:
            self.log_text.append(repr(obj))

    def clear_log(self):
        self.log_text = []

    def get_log(self) -> list :
        return self.log_text

    def print_info(self, info:object, p_color:str='', inspector:bool=True, newline:bool=True) -> str :
        """
        Print and/or save text information with choices of color, inspection info, newline
        """
        text = str(info)
        color = p_color if p_color else self.color
        if self.debug:
            calling_frame = inspect.currentframe().f_back
            self.print_text(info, color, inspector, newline, calling_frame)

        self.append(text)
        return text

    def print_error(self, info:object) -> str :
        """
        Print Error information in RED with inspection info
        """
        text = str(info)
        if self.debug:
            calling_frame = inspect.currentframe().f_back
            self.print_warning(info, calling_frame)
        return text

    @staticmethod
    def print_warning(info:object, p_frame:FrameType=None) -> str :
        calling_frame = p_frame if isinstance(p_frame, FrameType) else inspect.currentframe().f_back
        return SattoLog.print_text(info, BR_RED, p_frame=calling_frame)

    @staticmethod
    def print_text(info:object, color:str=BLACK, inspector:bool=True, newline:bool=True, p_frame:FrameType=None) -> str :
        """
        Print information with choices of color, inspection info, newline
        """
        inspect_line = ''
        if not info:
            info = '==========================================================================================================='
            inspector = False
        text = str(info)
        if inspector:
            calling_frame = p_frame if isinstance(p_frame, FrameType) else inspect.currentframe().f_back
            parent_frame  = calling_frame.f_back
            calling_file  = inspect.getfile(calling_frame).split('/')[-1]
            parent_file   = inspect.getfile(parent_frame).split('/')[-1] if parent_frame else ''
            calling_line  = str(inspect.getlineno(calling_frame))
            parent_line   = str(inspect.getlineno(parent_frame)) if parent_frame else ''
            inspect_line  = '[' + parent_file + '@' + parent_line + '->' + calling_file + '@' + calling_line + ']: '
        print(inspect_line + color + text + COLOR_OFF, end=('\n' if newline else ''))
        return text

# END class SattoLog


def year_span(target_year:int, base_year:int, base_year_span:int, hdr_span:int, logger:SattoLog=None) -> int :
    """
    calculate which row to update, factoring in the header row placed every so-many years
    :param    target_year: year to calculate for
    :param      base_year: starting year
    :param base_year_span: number of rows between equivalent positions in adjacent years, not including header rows
    :param       hdr_span: number of rows between header rows
    :param         logger: debug printing
    """
    if logger: logger.print_info("python_utilities.year_span()")

    year_diff = int(target_year - base_year)
    hdr_adjustment = 0 if hdr_span <= 0 else (year_diff // int(hdr_span))
    return int(year_diff * base_year_span) + hdr_adjustment


def get_int_year(target_year:str, base_year:int, logger:SattoLog=None) -> int :
    """
    convert the string representation of a year to an int
    :param target_year: to convert
    :param   base_year: earliest possible year
    :param      logger: debug printing
    """
    if logger: logger.print_info("python_utilities.get_int_year()")

    if not target_year.isnumeric():
        SattoLog.print_warning("Input MUST be the String representation of a Year, e.g. '2013'!")
        exit(156)
    int_year = int(float(target_year))
    if int_year > today.year or int_year < base_year:
        SattoLog.print_warning("Input MUST be the String representation of a Year between {} and {}!"
                               .format(today.year, base_year))
        exit(161)

    return int_year


def get_int_quarter(p_qtr:str, logger:SattoLog=None) -> int :
    """
    convert the string representation of a quarter to an int
    :param   p_qtr: to convert
    :param logger: debug printing
    """
    if logger: logger.print_info("python_utilities.get_int_quarter()")

    if not p_qtr.isnumeric():
        SattoLog.print_warning("Input MUST be a String of 0..4!")
        exit(176)
    int_qtr = int(float(p_qtr))
    if int_qtr > 4 or int_qtr < 0:
        SattoLog.print_warning("Input MUST be a String of 0..4!")
        exit(180)

    return int_qtr


def next_quarter_start(start_year:int, start_month:int, logger:SattoLog=None) -> (int, int) :
    """
    get the year and month that starts the FOLLOWING quarter
    :param  start_year
    :param start_month
    :param      logger: debug printing
    """
    if logger: logger.print_info("python_utilities.next_quarter_start()")

    # add number of months for a Quarter
    next_month = start_month + QTR_MONTHS

    # use integer division to find out if the new end month is in a different year,
    # what year it is, and what the end month number should be changed to.
    next_year = start_year + ((next_month - 1) // YEAR_MONTHS)
    next_month = ((next_month - 1) % YEAR_MONTHS) + 1

    return next_year, next_month


def current_quarter_end(start_year:int, start_month:int, logger:SattoLog=None) -> date :
    """
    get the date that ends the CURRENT quarter
    :param  start_year
    :param start_month
    :param     logger: debug printing
    """
    if logger: logger.print_info("python_utilities.current_quarter_end()")

    end_year, end_month = next_quarter_start(start_year, start_month)

    # last step, the end date is one day back from the start of the next period
    # so we get a period end like 2010-03-31 instead of 2010-04-01
    return date(end_year, end_month, 1) - ONE_DAY


def generate_quarter_boundaries(start_year:int, start_month:int, num_qtrs:int, logger:SattoLog=None) -> (date, date) :
    """
    get the start and end dates for the quarters in the submitted range
    :param  start_year
    :param start_month
    :param    num_qtrs: number of quarters to calculate
    :param     logger: debug printing
    """
    if logger: logger.print_info("python_utilities.generate_quarter_boundaries()")

    for i in range(num_qtrs):
        yield(date(start_year, start_month, 1), current_quarter_end(start_year, start_month))
        start_year, start_month = next_quarter_start(start_year, start_month)


def save_to_json(fname:str, ts:str, json_data, indt:int=4, p_color:str=BLACK) -> str:
    """
    print json data to a file -- add a time string to get a unique file name each run
    :param     fname: file path and name
    :param        ts: timestamp to use
    :param json_data: JSON compatible struct
    :param      indt: indentation amount
    :param   p_color: for printing
    :return: file name
    """
    out_file = fname + '_' + ts + ".json"
    SattoLog.print_text("JSON file is '{}'\n".format(out_file), p_color)
    fp = open(out_file, 'w')
    json.dump(json_data, fp, indent=indt)
    fp.close()
    return out_file
