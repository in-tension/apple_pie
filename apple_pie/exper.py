import os
import json
from typing import *

import matplotlib.pyplot as plt
import xlsxwriter

from .well import Well
from .condit import Condit
from .group import Group
# from .ap_utils import *
from brutils import *

# from pathlib import Path

class Exper :
    """
        * self.path
        * self.name
        * self.pm_file_path
        * self.csv_path
        * self.condit_dist_path
        * self.wells
        * self.condits
        * self.control
    """

    LOG_FILE_SUF = '_log.json'
    PLATE_MAP_SUF = '_plate-map.csv'
    CSV_DIR = 'Csv'
    CSV_EXT = '.csv'

    CONDIT_DIST_DIR = 'DistancesByCondition'
    CONDIT_DIST_PLOT_DIR = 'Plots'


    CONDIT_DIST_SUF = '_cell-distances.csv'

    EXPER_DIST_SUF = '_cell-distances_all-conditions.xlsx'
    EXPER_DIST_SUF2 = '_cell-distances_all-conditions3.xlsx'
    EXPER_DIST_SUF_MEDS = '_medians-by-drugs.xlsx'

    COLS_5 = ['x(Pixel Position)', 'y(Pixel Position)',
        'Area(pixels.^2)','Covariance','Pixels/Frame']
        ## Pixels/Frame = displacement

    COLS_5_DICT = {'x(Pixel Position)':'x', 'y(Pixel Position)':'y',
        'Area(pixels.^2)':'area','Covariance':'covariance','Pixels/Frame':'displacement'}

    COL_COUNT = 5

    NAME_DELIM = '_'

    CONTROL_PAT = 'dmso'    ## all lowercase


    def __init__(self, exper_path) :
        try :
            self.issue_log = {}

            all_t = ptic("all exper init")

            self.path = exper_path

            ### make it so this checks for / at end of path
            self.name = os.path.basename(self.path)
            self.init_paths_pm()

            well_t = ptic('reading in wells')
            self.init_wells()
            ptoc(well_t)

            self.init_condits()

            #self.dists_to_xlsx2()

            ptoc(all_t)

            #self.out_plot_a()


            self.init_groups()
            #self.out_meds_to_xlsx()

            #print(self.groups)
        finally :
            self.out_issue_log()


    def init_groups(self, tup_ind=0) :
        ## tup_ind -> tuple_index :
        ## make groups base on which element in condit.name tuple

        self.groups = {}

        for condit in self.condits.values() :
            if condit.name[tup_ind] in self.groups :
                self.groups[condit.name[tup_ind]].add_condit(condit)
            else :
                self.groups[condit.name[tup_ind]] = Group(self, condit.name[tup_ind], condits=[condit])



    def _init_groups(self) :
        ## will get rid of later
        ## right now only leaving it because I need to refactor other func o remove it
        self.group_names = []

        self.group_count = len(one_key(self.condits))

        ## double check true for all conditions
        # self.frame_count = one_value(self.condits).time_point_count




        #for condit_name in self.condits :
        #for i in range(len(one_value(self.condits))) :
        for i in range(self.group_count) :
            self.group_names.append({})

        for condit_name in self.condits :
            for i in range(self.group_count) :

                if condit_name[i] in self.group_names[i] :
                    self.group_names[i][condit_name[i]].append(condit_name)
                else :
                    self.group_names[i][condit_name[i]] = [condit_name]

        self.drug_groups = {}

        ## the 0 here probably shouldn't be hard coded
        for drug_name in self.group_names[0] :
            # self.drug_groups.append(Group(self, drug_name))
            self.drug_groups[drug_name] = Group(self, drug_name)
    # def make_no



    def out_meds_to_xlsx(self) :
        t_int = Exper.make_t_int(self.frame_count)

        ## too specific / hard-coded
        drug_groups = self.group_names[0]

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF_MEDS)

        with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :

            for drug in drug_groups :
                # col_count = 0
                w_sheet = w_book.add_worksheet(drug)
                temp_col_dict = {"Time":t_int,"Control(dmso)":self.control.dist_meds}
                for condit_name in drug_groups[drug] :
                    try :
                        temp_col_dict[condit_name] = self.condits[condit_name].dist_meds
                    except :
                        self.condits[condit_name].record_issue('exper.out_meds_to_xlsx',['condit.dist_meds is missing, could be caused by unmatching time points issue'])

                col_num = col_dict_to_sheet(temp_col_dict, w_sheet)


                # temp_col_dict[''] = ['','']
                ## control.cleaned_dist_meds?? instead of dist_meds
                temp_col_dict = {"Time":t_int,"Control(dmso)_dead-removed":self.control.dist_meds}
                for condit_name in drug_groups[drug] :


                    try :
                        temp_col_dict[condit_name + ('dead-removed',)] = self.condits[condit_name].cleaned_dist_meds
                    except :
                        self.condits[condit_name].record_issue('exper.out_meds_to_xlsx',['condit.cleaned_dist_meds is missing, could be caused by unmatching time points issue'])

                col_num = col_dict_to_sheet(temp_col_dict, w_sheet, col_num=col_num+1)
        # for condit_name in self.condits :

    def _meds_to_xlsx(self) :
        # pass

        ## too specific / hard-coded
        t_int = Exper.make_t_int(self.frame_count)

        drug_groups = self.group_names[0]

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF_MEDS)

        with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :


            for drug in drug_groups :
                # col_count = 0
                w_sheet = w_book.add_worksheet(drug)
                temp_col_dict = {"Time":t_int,"Control(dmso)":self.control.dist_meds}
                for condit_name in drug_groups[drug] :
                    try :
                        temp_col_dict[condit_name] = self.condits[condit_name].dist_meds
                    except :
                        self.condits[condit_name].record_issue('exper.out_meds_to_xlsx',['condit.dist_meds is missing, could be caused by unmatching time points issue'])

                col_num = col_dict_to_sheet(temp_col_dict, w_sheet)


                # temp_col_dict[''] = ['','']
                temp_col_dict = {"Time":t_int,"Control(dmso)_dead-removed":self.control.dist_meds}
                for condit_name in drug_groups[drug] :


                    try :
                        temp_col_dict[condit_name + ('dead-removed',)] = self.condits[condit_name].cleaned_dist_meds
                    except :
                        self.condits[condit_name].record_issue('exper.out_meds_to_xlsx',['condit.cleaned_dist_meds is missing, could be caused by unmatching time points issue'])

                col_num = col_dict_to_sheet(temp_col_dict, w_sheet, col_num=col_num+1)
        # for condit_name in self.condits :



    def out_plot_a(self) :
        for condit_name in self.condits :
            plt.close()
            f = plt.figure(figsize=(8,8))

            self.condits[condit_name].out_plot_a()
            #plt.ylim(top=20)
            #plt.ylim(0,20)
            #plt.pause(2)


            #plt.waitforbuttonpress()




            #print('poo')
            #plt.clf()
            #f.delaxes(plt.subplot(1,2,1))#.clear()
            #plt.gca()
            #f.delaxes(plt.subplot(1,2,2))#.clear()
            #plt.gca()
            pass



    def init_paths_pm(self) :
        self.pm_file_path = self.helper_find_file_easy(Exper.PLATE_MAP_SUF)
        table_types, well_dicts, self.condit_dict = Exper.in_plate_map(self.pm_file_path)

        self.csv_path = os.path.join(self.path,Exper.CSV_DIR)


        self.condit_dist_path = os.path.join(self.path, Exper.CONDIT_DIST_DIR)

        ensure_dir(self.condit_dist_path)

        self.condit_dist_plot_path = os.path.join(self.condit_dist_path, Exper.CONDIT_DIST_PLOT_DIR)

        ensure_dir(self.condit_dist_plot_path)


    def init_wells(self) :
        self.wells = {}

        for file_name in os.listdir(os.path.join(self.path,Exper.CSV_DIR)) :
            ## could make this more rigorous, check if filename fits a well format
            if file_name.endswith('.csv') and len(file_name) == 7 :
                well_name = file_name.split('.')[0]
                self.wells[well_name] = Well(self,well_name,os.path.join(self.path, Exper.CSV_DIR, file_name))


    def init_condits(self) :
        self.condits = {}
        for condit_name in self.condit_dict.keys() :
            self.condits[condit_name] = Condit(self,condit_name,self.condit_dict[condit_name])
        self.init_control()
        self.init_cstr_tup_dict()

    def init_cstr_tup_dict(self) :
        self.cstr_tup_dict = {}
        for condit in self.condits.values() :
            #condit_str = str(condit_tup)
            if condit.name_str in self.cstr_tup_dict :
                print('we has issue in exper.init_cstr_tup_dict()')
            else :
                self.cstr_tup_dict[condit.name_str] = condit.name

    def init_control(self) :
        """
        """
        control_name = self.helper_indentify_control()
        self.control = self.condits[control_name]
        del self.condits[control_name]

    def helper_indentify_control(self) :
        """
        """
        for condit_name in self.condits :
            condit_name_str = tuple_to_str(condit_name)
            temp = condit_name_str.lower()
            if Exper.CONTROL_PAT in temp :
                return condit_name
        return None



    def helper_xlsx_formats(self, w_book) :
        self.format_dicts = {}

        format_yellow = w_book.add_format()
        format_yellow.set_bg_color('#ffe98c')
        self.format_dicts['yellow'] = {
            'type':'cell',
            'criteria':'>',
            'value':50,
            'format':format_yellow}

        format_red = w_book.add_format()
        format_red.set_bg_color('#f7b29b')
        self.format_dicts['red'] = {
            'type':'cell',
            'criteria':'<',
            'value':Condit.DEAD_CUTOFF,
            'format':format_red}

        format_white = w_book.add_format()
        format_white.set_bg_color('#FFFFFF')
        self.format_dicts['white'] = {
            'type':'blanks',
            'format':format_white}


    def out_dists_to_xlsx(self) :
        """
        """
        wb_time = ptic('whole xlsx workbook')

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF)

        with xlsxwriter.Workbook(out_file) as w_book :
            self.helper_xlsx_formats(w_book)

            for condit_name in self.condits :
                self.condits[condit_name].out_dists_to_sheet(w_book)

        ptoc(wb_time)


    def out_smooth_dists_to_xlsx(self) :
        """
        """
        wb_time = ptic('whole xlsx workbook')

        out_file = os.path.join(self.condit_dist_path, self.name + Exper.EXPER_DIST_SUF)

        with xlsxwriter.Workbook(out_file) as w_book :
            self.helper_xlsx_formats(w_book)

            for condit_name in self.condits :
                pass
                # condit will make smooth_dists in func if they don't already exist
                self.condits[condit_name].out_smooth_dists_to_sheet(w_book)


        ptoc(wb_time)


    def out_issue_log(self) :

        log_file_path = os.path.join(self.path, self.name + Exper.LOG_FILE_SUF)

        # try :
        with open(log_file_path, 'a') as f :
            json.dump(self.issue_log,f,indent=4)
        # except FileNotFoundError :
        #     with open(log_file_path, 'w') as f :
        #         json.dump(self.issue_log,f,indent=4)


    def helper_find_file_easy(self, pattern, sub_dir='') :
        """
        """
        temp_path = os.path.join(self.path,sub_dir)
        return Exper.helper_find_file(temp_path,pattern)

    @staticmethod
    def helper_find_file(path, pattern) :
        """
        """
        for file_name in os.listdir(path) :
            if pattern in file_name :
                return os.path.join(path,file_name)

        ### fix this
        print("couldn't find file in {} with pattern {}".format(path, pattern))
        return None


    @staticmethod
    def in_plate_map(pm_file_path) :
        """
            assumes rows go from B-P, and cols from 2-24

            :param pm_file_path:
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
            table_type, well_dict = Exper.helper_process_table(table)
            well_dicts[table_type] = well_dict
            table_types.append(table_type)


        well_names = well_dicts[table_types[0]].keys()

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
            if condit_name in condit_dict :
                condit_dict[condit_name].append(well_name)
            else :
                condit_dict[condit_name] = [well_name]

        return table_types, well_dicts, condit_dict

    @staticmethod
    def helper_process_table(pm_table) :
        """
            | takes pm_table, a table from the plate-map file and
        """
        if not len(pm_table) == 16 :
            ### fix this
            print('crap, this shouldnt happen')
        elif not len(pm_table[0]) == 24 :
            ### fix this
            print('crap, this shouldnt happen')

        table_type = pm_table[0][0]

        col_names = pm_table[0][1:]

        pm_table = pm_table[1:]
        table_as_cols = rotate(pm_table)
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


    @staticmethod
    ## t_int -> time_intervals
    def make_t_int(count) :
        return [x/6 for x in range(1,count+1)]
