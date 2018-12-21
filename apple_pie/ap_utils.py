import os
import csv
import time
import pathlib

import numpy as np
import xlsxwriter

from typing import *

class RecordedIssue(Exception) :
    pass

class Types :
    """
    """
    Arr = List[Any]
    Arrs = List[Arr]

    File = os.PathLike

    SpecKey = Union[str, tuple]
    ColDict = Dict[Union[SpecKey], Arr]


def one_key(some_dict) :
    for key in some_dict :
        return key

def one_value(some_dict) :
    for value in some_dict.values() :
        return value




## <arrs_to_spreadsheets>
def csv_to_rows(csv_path: Types.File) :
    """
    """
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows

def csv_to_dict(csv_path: Types.File) :
    """
        reads a csv file and creates a dict of rows
        assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)

    col_dict = {}
    for col in cols :
        col_dict[col[0]] = col[1:]

    return col_dict

def rows_to_csv(rows: Types.Arrs, csv_path: Types.File) :
    """
        writes a 2D list of rows to a csv
    """
    with open(csv_path, 'w', newline='') as csv_file :
        csv_writer = csv.writer(csv_file)
        for row in rows :
            csv_writer.writerow(row)

def col_dict_to_csv(col_dict, csv_path) :
    """
        writes a dict of columns to a csv
    """
    cols = []
    for col_key in col_dict :
        temp_col = [col_key] + col_dict[col_key]
        cols.append(temp_col)
    rows = rotate(cols)
    rows_to_csv(rows, csv_path)

def col_dict_to_sheet(col_dict,w_sheet,col_num=0) :
    """
    """
    # col_num = 0
    for key in col_dict :
        if(type(key) == tuple) :
            key_str = tuple_to_str(key)
        elif(type(key) == str) :
            key_str = key
        else :
            key_str = str(key)



        w_sheet.write_string(0, col_num, key_str)
        w_sheet.write_column(1, col_num, col_dict[key])

        col_num += 1
    return col_num


def col_dict_to_xlsx(out_file,col_dict,col_num=0) :
    with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :
        w_sheet = w_book.add_worksheet('')
        col_dict_to_sheet(col_dict, w_sheet)

def lever_csv_to_dict(csv_path) :
    """
        5 cols, not 4
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)
    col_dict = {}

    ## ce as in cell, co as in col
    for ce in range(0,len(cols),5) :
        for co in range(0,5) :
            col_tuple_key = (cols[ce][0], cols[ce+co][3])
            col_dict[col_tuple_key] = cols[ce+co][4:]

    return col_dict
## </arrs_to_spreadsheets>

## <arrs manip>
def is_rec(arrs: Types.Arrs) :
    """
        | checks whether 2D list ``arrs`` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    length = len(arrs[0])
    for arr in arrs :
        if len(arr) != length :
            return False
    return True

def is_rec_col_dict(col_dict) :
    """
        | checks whether 2D list ``arrs`` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    length = len(one_value(col_dict))
    for col in col_dict.values() :
        if len(col) != length :
            return False
    return True

def make_rec(arrs: Types.Arrs, blank=None) :
    """
        | takes a 2D list ``arrs`` and makes sure it's a rectangle -
        | makes sures all inner lists are the same length

        | changes original ``arrs``
        | ``blank`` = value added to end of inner arrays if not long enough

    """
    if not is_rec(arrs) :
        longest = 0
        for arr in arrs :
            if len(arr) > longest :
                longest = len(arr)

        for arr in arrs :
            while(len(arr) < longest) :
                arr.append(blank)

def rotate(arrs: Types.Arrs, blank=None) :
    """
        | takes a 2D list ``arrs`` and switches the inner and outer arrays
        | i.e. rows_to_cols or cols_to_rows

        makes ``arrs`` a rectangle using make_rec - which changes oringinal ``arrs``)

        blank is used in make_rec
    """
    make_rec(arrs,blank=blank)

    rotated_arrs = [[arr[i] for arr in arrs] for i in range(len(arrs[0]))]
    return rotated_arrs
## </arrs_manip>


def ensure_dir(dir) :
    """
        if dir doensn't exist, creates it
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

def arr_cast(arr, cast_type) :
    """
        cast_type = str, float, int...
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(element)
    return new_arr

## arr_cast assumed from str
## where '' is set to None
def arr_cast_spec(arr, cast_type) :
    """
        cast_type = float, int...
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(None)
    return new_arr

def avg(arr) :
    """
        | returns the average of a given array
        | skips None values
    """
    sum = 0.0
    count = 0
    for element in arr :
        if element != None :
            sum += element
            count += 1

    if count == 0 :
        return None
    return sum/count

def mov_avg(arr,above_below=5) :
    """
    """
    new_arr = []
    for i in range(len(arr)) :

        below = i - above_below
        if below < 0 : below = 0
        above = i + above_below
        if above >= len(arr) : above = len(arr) - 1

        new_element = avg(arr[below:above])
        new_arr.append(new_element)
    return new_arr

def arr_np_nan(arr) :
    for i in range(len(arr)) :
        if arr[i] == None :
            arr[i] = np.nan


def col_dict_np_nan(col_dict) :
    for col_name in col_dict :
        arr_np_nan(col_dict[col_name])

def col_dict_row_nanmed(col_dict) :
    """
        .. note: asumes col_dict is rec
    """
    for col_name in col_dict :
        h = len(col_dict[col_name])
        break

    med_col = []
    for r in range(h) :
        temp_row = []
        for col_name in col_dict :
            temp_row.append(col_dict[col_name][r])
        med = np.nanmedian(temp_row)
        med_col.append(med)



    return med_col



## this can't be the right way to do this
## assumes list does not contain commas
## only finds first instance
def pattern_in_list(some_list, pattern) :
    """
    """
    split_char = ','

    str_list = ''
    for element in some_list :
        str_list += str(element) + split_char

    str_pattern = ''
    for element in pattern :
        str_pattern += str(element) + split_char

    str_index = str_list.find(str_pattern)
    if str_index != -1 :
        index = str_list[:str_index].count(split_char)
        return index
    else :
        return -1

def tuple_to_str(tup,delim='_') :
    """
    """
    temp = []
    for term in tup :
        temp.append(str(term))
    return delim.join(temp)

## <tic_toc>
def tic() :
    """
    """
    return time.time()

def toc(start_time) :
    """
    """
    end_time = time.time()
    return (end_time-start_time)

## ptoc = print_toc
def toc2(start_time,descrip='') :
    """
    """
    elapsed_time = toc(start_time)
    print('{} : {} seconds'.format(descrip, elapsed_time))

def ptic(descrip) :
    """
    """
    return [descrip,time.time()]

def ptoc(descrip_n_time) :
    """
    """
    elapsed_time = time.time() - descrip_n_time[1]
    print('{} : {:.2f} seconds'.format(descrip_n_time[0], elapsed_time))
## </tic_toc>
