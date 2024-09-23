##############################################################################################################################
# coding=utf-8
#
# mhsUtils.py -- useful constants & functions
#
# some code from gnucash examples by Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2019-04-07"
__updated__ = "2024-09-23"

import json
from decimal import Decimal
from datetime import date, timedelta, datetime as dt
import logging as lg
import os.path as osp

FXN_TIME_STR:str  = "%H:%M:%S:%f"
CELL_DATE_STR:str = "%Y-%m-%d"
CELL_TIME_STR:str = "%H:%M:%S"
FILE_DATE_STR:str = "D%Y-%m-%d"
FILE_TIME_STR:str = "T%H-%M-%S"
FILE_DATETIME_FORMAT:str = FILE_DATE_STR + FILE_TIME_STR
RUN_DATETIME_FORMAT:str  = CELL_DATE_STR + '_' + FXN_TIME_STR

UTF8_ENCODING:str = "utf-8"
JSON_LABEL:str    = "json"

# my file structure
HOME_FOLDER:str        = osp.sep + "home" + osp.sep + "marksa"
BASE_DEV_FOLDER:str    = osp.join(HOME_FOLDER, "dev")
BASE_GIT_FOLDER:str    = osp.join(BASE_DEV_FOLDER, "git")
BASE_PYTHON_FOLDER:str = osp.join(BASE_GIT_FOLDER, "Python")
PYTHON_UTIL_FOLDER:str = osp.join(BASE_PYTHON_FOLDER, "utils")

MAX_QUARTER:int = 4  # 1 to 4 = use this quarter of selected year"
MIN_QUARTER:int = 0  # Zero = "ALL four quarters"
QTR_MONTHS:int  = 3
YEAR_MONTHS:int = 12

ZERO:Decimal = Decimal(0)
ONE_DAY:timedelta = timedelta(days=1)
now_dt = dt.now()

def get_current_date(format_indicator:str = CELL_DATE_STR) -> str:
    return dt.now().strftime(format_indicator)

def get_current_time(format_indicator:str = RUN_DATETIME_FORMAT) -> str:
    return dt.now().strftime(format_indicator)

def get_current_year() -> int:
    return int( get_current_date("%Y") )

def get_base_fileparts(filename:str) -> (str,str):
    _, fname = osp.split(filename)
    return osp.splitext(fname)

def get_filepath(filename:str) -> str:
    fpath, _ = osp.split(filename)
    return fpath

def get_filename(filename:str) -> str:
    _, fname = osp.split(filename)
    return fname

def get_base_filename(filename:str) -> str:
    basename, _ = get_base_fileparts(filename)
    return basename

def get_filetype(filename:str) -> str:
    _, ftype = get_base_fileparts(filename)
    return ftype

def get_custom_base_filename(p_name:str, file_div:str = osp.sep, sfx_div:str = osp.extsep) -> str:
    spl1 = p_name.split(file_div)
    if spl1 and isinstance(spl1, list):
        spl2 = spl1[-1].split(sfx_div)
        if spl2 and isinstance(spl2, list):
            return spl2[0]
    return ""

def year_span(target_year:int, base_year:int, yr_span:int, hdr_span:int, logger:lg.Logger = None) -> int:
    """
    Calculate which row to update, factoring in the header row placed every $hdr_span years.
    :param   target_year: year to calculate for
    :param   base_year: starting year in the sheet
    :param   yr_span: number of rows between equivalent positions in adjacent years, not including header rows
    :param   hdr_span: number of rows between header rows
    :param   logger: optional
    :return  span as int
    """
    if logger:
        logger.debug(F"target year = {target_year}; base year = {base_year}; year span = {yr_span}; header span = {hdr_span}")
    year_diff = target_year - base_year
    hdr_adjustment = 0 if hdr_span <= 0 else (year_diff // hdr_span)
    return (year_diff * yr_span) + hdr_adjustment

def get_int_year(target_year:str, base_year:int, logger:lg.Logger = None) -> int:
    """
    Convert the string representation of a year to an int.
    :param   target_year: to convert
    :param   base_year: earliest possible year
    :param   logger: optional
    :return  year as int
    """
    if logger:
        logger.debug(F"year = {target_year}; base year = {base_year}")

    if not ( target_year.isnumeric() and len(target_year) == 4 ):
        msg = "Input MUST be the String representation of a RECENT year, e.g. '2013'!"
        if logger:
            logger.error(msg)
        raise Exception(msg)

    int_year = int( float(target_year) )
    if int_year > now_dt.year or int_year < base_year:
        msg = F"Input MUST be a Year between {base_year} and {now_dt.year}!"
        if logger:
            logger.error(msg)
        raise Exception(msg)

    return int_year

def get_int_quarter(p_qtr:str, logger:lg.Logger = None) -> int:
    """
    Convert the string representation of a quarter to an int.
    :param   p_qtr: string to convert
    :param   logger: optional
    :return  quarter as int
    """
    if logger:
        logger.debug(F"quarter to convert = {p_qtr}")

    msg = "Input MUST be a String of 0..4!"
    if not p_qtr.isnumeric() or len(p_qtr) != 1:
        if logger:
            logger.error(msg)
        raise Exception(msg)

    int_qtr = int( float(p_qtr) )
    if int_qtr > MAX_QUARTER or int_qtr < MIN_QUARTER:
        if logger:
            logger.error(msg)
        raise Exception(msg)

    return int_qtr

def next_quarter_start(start_year:int, start_month:int, logger:lg.Logger = None) -> (int, int):
    """
    Get the year and month that start the FOLLOWING quarter.
    :param   start_year
    :param   start_month
    :param   logger: optional
    :return  year as int, month as int
    """
    if logger:
        logger.debug(F"start year = {start_year}; start month = {start_month}")
    # add number of months for a Quarter
    next_month = start_month + QTR_MONTHS
    # use integer division to find out if the new end month is in a different year,
    # what year it is, and what the end month number should be changed to.
    next_year = start_year + ( (next_month - 1) // YEAR_MONTHS )
    next_month = ( (next_month - 1) % YEAR_MONTHS ) + 1

    return next_year, next_month

def current_quarter_end(start_year:int, start_month:int, logger:lg.Logger = None) -> date:
    """
    Get the date that ends the CURRENT quarter.
    :param   start_year
    :param   start_month
    :param   logger: optional
    :return  end date
    """
    if logger:
        logger.debug(F"start year = {start_year}; start month = {start_month}")
    end_year, end_month = next_quarter_start(start_year, start_month)
    # end date is one day back from the start of the next period
    return date(end_year, end_month, 1) - ONE_DAY

def generate_quarter_boundaries(start_year:int, start_month:int, num_qtrs:int, logger:lg.Logger = None) -> (date, date):
    """
    Generate the start and end dates for the quarters in the submitted range.
    :param   start_year
    :param   start_month
    :param   num_qtrs: number of quarters to calculate
    :param   logger: optional
    :return  start date, end date
    """
    if logger:
        logger.debug(F"start year = {start_year}; start month = {start_month}; num quarters = {num_qtrs}")
    for i in range(num_qtrs):
        yield date(start_year, start_month, 1), current_quarter_end(start_year, start_month)
        start_year, start_month = next_quarter_start(start_year, start_month)

def save_to_json(fname:str, json_data:object, ts:str = get_current_time(FILE_DATETIME_FORMAT),
                 indt:int = 4, logger:lg.Logger = None, folder_name:str = JSON_LABEL) -> str:
    """
    Print json data to a file -- add a timestamp to get a unique file name each run.
    :param   fname: base file name to use
    :param   json_data: JSON compatible struct
    :param   ts: timestamp to use
    :param   indt: indentation amount
    :param   logger: optional
    :param   folder_name: location to save file
    :return  saved file name
    """
    try:
        save_subdir = folder_name if ( osp.isdir(folder_name) ) else '.'
        outfile_name = osp.join(save_subdir, fname + '_' + ts + osp.extsep + JSON_LABEL)
        if logger:
            logger.info(F"Write to {JSON_LABEL.upper()} file: {outfile_name}")
        with open(outfile_name, 'w') as jfp:
            json.dump(json_data, jfp, indent=indt)
        return outfile_name
    except Exception as sjex:
        if logger:
            logger.exception(sjex)
        raise sjex
