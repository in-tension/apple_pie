
#import os
import csv

def csv_to_rows(csv_path) :
    rows = []
    with open(csv_path,'r') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows

def is_rec(arrs) :
    length = len(arrs[0])
    for arr in arrs :
        if len(arr) != length :
            return False
    return True

def make_rec(arrs, blank=None) :
    """
        changes original arrs
        blank = value added to end of arr if not long enough

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
        blank used in make_rec
    """

    make_rec(arrs,blank=blank)


    rotated_arrs = [[arr[i] for arr in arrs] for i in range(len(arrs[0]))]
    return rotated_arrs


def csv_to_dict(csv_path) :
    """
        assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)

    col_dict = {}
    for col in cols :
        col_dict[col[0]] = col[1:]

    return col_dict

def arr_cast(arr, cast_type) :
    """
        cast_type = str, float, int...
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except e :
            new_arr.append(element)






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


path = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)/RH30/20181106/'

csvFolder = 'Csv/'
well = 'B02.csv'

my_csv_path = path + csvFolder + well

cols = lever_csv_to_dict(my_csv_path)

print(cols.keys())

#print(csv_to_rows(path+csvFolder+well))
#
# with open(path+csvFolder+well,'r') as f :
#     print(f.readlines())






#print(os.listdir(path))
# for f in os.listdir(path) :
#     if os.path.isdir(path + '/' + f) :
#         print(f)
#
#
