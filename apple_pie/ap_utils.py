
import os
import csv
import time


def csv_to_rows(csv_path) :
    """
    """
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows

def is_rec(arrs) :
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

def make_rec(arrs, blank=None) :
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

def rotate(arrs,blank=None) :
    """
        | takes a 2D list ``arrs`` and switches the inner and outer arrays
        | i.e. rows_to_cols or cols_to_rows

        makes ``arrs`` a rectangle using make_rec - which changes oringinal ``arrs``)

        blank is used in make_rec

    """

    make_rec(arrs,blank=blank)


    rotated_arrs = [[arr[i] for arr in arrs] for i in range(len(arrs[0]))]
    return rotated_arrs


def csv_to_dict(csv_path) :
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


def rows_to_csv(rows, csv_path) :
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
        # if element == '' :
        #     new_arr.append(None)
        # else :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(None)
    return new_arr





def lever_csv_to_dict(csv_path) :
    """
        5 cols, not 4
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)
    col_dict = {}

    #for col in cols :
    # ce as in cell, co as in col
    for ce in range(0,len(cols),5) :
        for co in range(0,5) :
            col_tuple_key = (cols[ce][0], cols[ce+co][3])
            col_dict[col_tuple_key] = cols[ce+co][4:]

        #col_dict[col[0]] = col[3:]



    return col_dict



def avg(arr) :
    """
        | returns the average of a given array
        | skips None values
    """
    sum = 0.0
    count = 0
    # print('avg.arr = {}'.format(arr))
    for element in arr :
        # print(element)
        if element != None :
            sum += element
            count += 1

    # input()
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

        # print(below)
        #
        # print(above)

        new_element = avg(arr[below:above])
        new_arr.append(new_element)
    return new_arr










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
def ptoc2(start_time,descrip='') :
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
