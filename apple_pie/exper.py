import os

import xlsxwriter

from .well import Well
from .condit import Condit
from .ap_utils import *


class Exper :
    PLATE_MAP_SUF = '_plate-map.csv'
    CSV_DIR = 'Csv'
    CSV_EXT = '.csv'

    CONDIT_DIST_DIR = 'DistancesByCondition'

    CONDIT_DIST_SUF = '_cell-distances.csv'

    EXPER_DIST_SUF = '_cell-distances_all-conditions.xlsx'
    EXPER_DIST_SUF2 = '_cell-distances_all-conditions3.xlsx'

    COLS_5 = ['x(Pixel Position)', 'y(Pixel Position)',
        'Area(pixels.^2)','Covariance','Pixels/Frame']
        ## Pixels/Frame = displacement

    COLS_5_DICT = {'x(Pixel Position)':'x', 'y(Pixel Position)':'y',
        'Area(pixels.^2)':'area','Covariance':'covariance','Pixels/Frame':'displacement'}

    COL_COUNT = 5

    NAME_DELIM = '_'






    def __init__(self, exper_path) :
        """
        """
        all_t = ptic("all exper init")

        self.path = exper_path

        ### make it so this checks for / at end of path
        self.name = os.path.basename(self.path)

        self.wells = {}
        ## could make this more rigorous, check if filename fits a well format
        well_t = ptic('reading in wells')
        for file_name in os.listdir(os.path.join(self.path,Exper.CSV_DIR)) :
            if file_name.endswith('.csv') and len(file_name) == 7 :
                well_name = file_name.split('.')[0]
                self.wells[well_name] = Well(self,well_name,os.path.join(self.path,Exper.CSV_DIR,file_name))
        ptoc(well_t)

        self.pm_file_path = self.find_file_easy(Exper.PLATE_MAP_SUF)
        table_types, well_dicts, self.condit_dict = Exper.read_plate_map(self.pm_file_path)

        self.csv_path = os.path.join(self.path,Exper.CSV_DIR)


        self.condit_dist_path = os.path.join(self.path, Exper.CONDIT_DIST_DIR)

        ensure_dir(self.condit_dist_path)







        self.condits = {}
        for condit_name in self.condit_dict.keys() :
            #print(condit_name)
            self.condits[condit_name] = Condit(self,condit_name,self.condit_dict[condit_name])



        self.dists_to_xlsx2()

        ptoc(all_t)



    def dists_to_xlsx(self) :
        """
            .. note:: assumes ``self.condits`` and ``self.condit_dist_path`` already exists

        """


        wb_time = ptic('whole xlsx workbook')

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF)


        with xlsxwriter.Workbook(out_file) as w_book :

            self.format_yellow = w_book.add_format()
            self.format_yellow.set_bg_color('#ffe98c')

            self.format_red = w_book.add_format()
            self.format_red.set_bg_color('#f7b29b')

            self.format_white = w_book.add_format()
            self.format_white.set_bg_color('#FFFFFF')

            for condit_name in self.condits :
                self.condits[condit_name].dist_to_sheet(w_book)

        ptoc(wb_time)

    def dists_to_xlsx2(self) :
        """
            .. note:: assumes ``self.condits`` and ``self.condit_dist_path`` already exists

        """


        wb_time = ptic('whole xlsx workbook')

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF2)


        with xlsxwriter.Workbook(out_file) as w_book :

            self.format_yellow = w_book.add_format()
            self.format_yellow.set_bg_color('#ffe98c')

            self.format_red = w_book.add_format()
            self.format_red.set_bg_color('#f7b29b')

            self.format_white = w_book.add_format()
            self.format_white.set_bg_color('#FFFFFF')

            for condit_name in self.condits :
                self.condits[condit_name].dist_to_sheet2(w_book)

        ptoc(wb_time)

    def find_file_easy(self,pattern,sub_dir='') :
        """
        """
        temp_path = os.path.join(self.path,sub_dir)
        return Exper.find_file(temp_path,pattern)



    @staticmethod
    def find_file(path,pattern) :
        """
        """
        for file_name in os.listdir(path) :
            if pattern in file_name :
                return os.path.join(path,file_name)

        ### fix this
        print("couldn't find file in {} with pattern {}".format(path, pattern))
        return None


    @staticmethod
    def read_plate_map(pm_file_path) :
        """
            assumes rows go from B-P, and cols from 2-24
        """
        pm_rows = csv_to_rows(pm_file_path)

        row_ranges = []
        for i in range(len(pm_rows)) :
            if pm_rows[i][0] == 'B' :
                row_ranges.append([i])
            elif pm_rows[i][0] == 'P' :
                row_ranges[-1].append(i)



        tables = []


        for start, stop in row_ranges :
            tables.append(pm_rows[start-1:stop+1])

        well_dicts = {}
        table_types = []
        for table in tables :
            table_type, well_dict = Exper.process_table(table)
            well_dicts[table_type] = well_dict
            table_types.append(table_type)



        well_names = well_dicts[table_types[0]].keys()

        #well_keys = set()

        condit_table_names = []
        for table_type in table_types :


            if well_dicts[table_type].keys() != well_names :
                ### improve this
                print("shit, some tables in plate-map have data in more wells than other tables\ncode assumes that this isn't the case and will likely cause issues if not\n\twill only look at wells that are in the very first table\n\twill crash if later table does not have a well in first table")


            ## could use startswith('condit') or split('_')[0] == 'condit'
            if table_type.startswith('condit') :
                 condit_table_names.append(table_type)

        condit_dict = {}

        for well_name in well_names :
            condit_name = ()
            for condit_table_name in condit_table_names :
                name_part = well_dicts[condit_table_name][well_name]
                if 'num' in condit_table_name :
                    try :
                        name_part = float(name_part)
                    except :
                        pass
                        ### improve this
                        #print("poop, issue in plate-map, table supposed to contain numbers\nbut well {0} can't be converted to a number, well {0} = {1}".format(well_name,name_part))

                condit_name = condit_name + (name_part,)
            # print(condit_name)
            if condit_name in condit_dict :
                condit_dict[condit_name].append(well_name)
            else :
                condit_dict[condit_name] = [well_name]


        return table_types, well_dicts, condit_dict

        # for key in condit_dict.keys() :
        #     print('{} : {}'.format(key,condit_dict[key]))




    @staticmethod
    def process_table(table) :
        """
        """
        if not len(table) == 16 :
            ### fix this
            print('crap, this shouldnt happen')
        elif not len(table[0]) == 24 :
            ### fix this
            print('crap, this shouldnt happen')

        table_type = table[0][0]

        col_names = table[0][1:]

        table = table[1:]
        table_as_cols = rotate(table)
        row_names = table_as_cols[0]

        table_as_cols = table_as_cols[1:]


        well_dict = {}
        for c in range(len(table_as_cols)) :
            for r in range(len(table_as_cols[c])) :
                col_name = col_names[c]
                while len(col_name) < 2 :
                    col_name = '0' + col_name

                well_name = row_names[r] + col_name

                well_value = table_as_cols[c][r]
                if well_value != '' :
                    well_dict[well_name] = well_value

        return table_type, well_dict
