
import xlsxwriter
import matplotlib.pyplot as plt

from .ap_utils import *


class Condit :
    DEAD_CUTOFF = 3
    DEAD_FRAME_COUNT = 10
    UPPER_CUTOFF = 50

    def __init__(self, exper, name: tuple, well_names) :
        """
            self.exper
            self.name
            self.wells


            self.dists

            self.smooth_dists
            self.cleaned_dists

            self.dist_meds
            self.cleaned_dist_meds

            self.t_init
            self.cell_count
            self.dist_len
            self.name_str


        """
        self.exper = exper
        self.name = name
        self.make_name_str()

        self.wells = {}
        for well_name in well_names :
            self.wells[well_name] = self.exper.wells[well_name]

        self.make_dists()
        self.make_cleaned_dists()

        col_dict_np_nan(self.dists)
        col_dict_np_nan(self.cleaned_dists)

        self.dist_meds = col_dict_row_nanmed(self.dists)
        self.cleaned_dist_meds = col_dict_row_nanmed(self.cleaned_dists)

        self.t_int = [x/6 for x in range(1,self.dist_len+1)]


        #self.make_coords()

        #self.dists_to_csv()
        pass



    def plot_a(self) :
        """
            plots control and condit dist_med and cleaned_dist_med
            and a chart of live/dead/no data cells per time point
        """


        plt.subplot(2,2,1)
        ax = plt.gca()

        ax.scatter(self.t_int,self.exper.control.dist_meds,label='control orig median')
        ax.scatter(self.t_int,self.exper.control.cleaned_dist_meds,label='control removed dead median')
        ax.set_ylim((0,20))

        ax.legend()


        plt.subplot(2,2,2)
        ax = plt.gca()

        ax.scatter(self.t_int,self.dist_meds,label=self.name_str+' orig median')
        ax.scatter(self.t_int,self.cleaned_dist_meds,label=self.name_str+' removed dead median')

        ax.set_ylim((0,20))

        ax.legend()

        plot_file = os.path.join(self.exper.condit_dist_plot_path, self.name_str + '_plot.png')


        plt.subplot(2,1,2)
        ax = plt.gca()

        temp_dead_col = [l+d for l,d in zip(self.live_col,self.dead_col)]
        temp_none_col = [d+n for d,n in zip(temp_dead_col,self.none_col)]

        ax.fill_between(self.t_int, self.live_col,label = 'live cells', step='mid', color='#846cfc')
        ax.fill_between(self.t_int, temp_dead_col, y2=self.live_col, label = 'dead cells', step='mid', color='#87ffad')
        ax.fill_between(self.t_int, temp_none_col, y2=temp_dead_col, label='no data', step='mid', color='#ffa0ce')

        ax.set_ylim((0,60))
        ax.legend()


        plt.savefig(plot_file)






    def make_name_str(self) :
        """
            takes ``self.name``, a ``tuple`` and returns a ``str`` with each term joined by ``Exper.NAME_DELIM``
        """
        temp = []
        for term in self.name :
            temp.append(str(term))
        self.name_str = self.exper.NAME_DELIM.join(temp)


    def dists_to_csv(self) :
        """
            writes ``self.dists`` to a csv file
        """
        try :
            self.dists
        except AttributeError :
            self.make_dists()



        out_file = os.path.join(self.exper.condit_dist_path, self.name_str + self.exper.CONDIT_DIST_SUF)

        col_dict_to_csv(self.dists,out_file)

    def dists_to_sheet(self, w_book: xlsxwriter.Workbook) :
        """
            writes ``self.dists`` to a excel add_worksheet added to w_book
        """
        try :
            self.dists
        except AttributeError :
            self.make_dists()


        w_sheet = w_book.add_worksheet(self.name_str)

        col_dict_to_sheet(self.dists, w_sheet)
        self.set_xlsx_formats(w_sheet,1,0,self.dist_len,self.cell_count)


    def smooth_dists_to_sheet(self, w_book: xlsxwriter.Workbook) :
        """
            writes ``self.smooth_dists`` to a excel add_worksheet
            .. note: assumes ``self.smooth_dists`` already exists
        """
        try :
            self.smooth_dists
        except AttributeError :
            self.make_dists()


        w_sheet = w_book.add_worksheet(self.name_str)

        col_dict_to_sheet(self.smooth_dists, w_sheet)
        self.set_xlsx_formats(w_sheet,1,0,self.dist_len,self.cell_count)




    def set_xlsx_formats(self,w_sheet,r1,c1,r2,c2) :
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['yellow'])
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['red'])
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['white'])


    ## this function could probably be more efficient
    ## this function could probably more compact w/ less steps but I don't know if it would increase or decrease readability
    def make_coords(self) :
        """
            | goes through ``self.wells`` and creates ``self.coords``
            | a ``Types.ColDict`` of the coordinates of cells in condit

            .. note: assumes every x has a y before the next x
        """
        self.coord_cols = {}

        ## change this to for well_name in self.wells
        ## so as consistent through out
        for well in self.wells.values() :
            for key in well.raw_data.keys() :
                if key[1] == self.exper.COLS_5[0] :    ## COLS_5[0] -> x
                    col = arr_cast_spec(well.raw_data[key],float)
                    self.coord_cols[(well.name, 'cell {}'.format(key[0]))] = [col]
                if key[1] == self.exper.COLS_5[1] :    ## COLS_5[1] -> y
                    col = arr_cast_spec(well.raw_data[key],float)

                    self.coord_cols[(well.name, 'cell {}'.format(key[0]))].append(col)

        self.coords = {}

        for cell_name in self.coord_cols :

            xs = self.coord_cols[cell_name][0]
            ys = self.coord_cols[cell_name][1]


            temp_cell_coords = []
            for x,y in zip(xs,ys) :
                temp_cell_coords.append([x,y])
            self.coords[cell_name] = temp_cell_coords




    def make_dists(self) :
        """
            | gets distance columns from wells
            | removes weird zeros and leading and trailing blank rows
        """
        self.dists = {}
        for well in self.wells.values() :
            for key in well.raw_data.keys() :
                if key[1] == self.exper.COLS_5[4] :
                    self.dists[(well.name,'cell {}'.format(key[0]))] = well.raw_data[key]

        for col in self.dists.values() :
            for i in range(len(col)) :
                if col[i] == '' :
                    col[i] = None
                else :
                    try :
                        col[i] = float(col[i])
                    except :
                        print("oh no, well csv value not a number")

        self.cell_count = len(self.dists.keys())

        check_count = 0
        for well in self.wells.values() :
            check_count += well.cell_count
        if check_count != self.cell_count :
            print('fuck, condit cell_count wrong')

        self.fix_dists_zeros()
        self.trim_dists()
        self.remove_upper_outliers()


    def make_cleaned_dists(self) :
        """
            creates ``self.cleaned_dists`` with "dead" cells removed
            .. note: assumes ``self.dists`` already exists
        """


        self.make_smooth_dists()
        self.make_cell_counts()

        self.cleaned_dists = {}


        for cell_name in self.smooth_dists :
            temp_col = []

            for r in range(len(self.smooth_dists[cell_name])) :
                if self.smooth_dists[cell_name][r] == None :
                    temp_col.append(None)
                elif self.smooth_dists[cell_name][r] < Condit.DEAD_CUTOFF :
                    temp_col.append(None)
                else :
                    temp_col.append(self.dists[cell_name][r])

            self.cleaned_dists[cell_name] = temp_col
            # print(cell_name)
            # print(self.smooth_dists[cell_name])
            # print(self.dists[cell_name])
            # print(self.cleaned_dists[cell_name])
            # input()


    def make_cell_counts(self) :
        """
            .. note: assumes ``self.smooth_dists`` already exists
        """
        self.dead_col = []
        self.live_col = []
        self.none_col = []

        for r in range(self.dist_len) :
            dead = 0
            live = 0
            none = 0
            for cell_name in self.smooth_dists :
                if self.smooth_dists[cell_name][r] == None :
                    none += 1

                elif self.smooth_dists[cell_name][r] < Condit.DEAD_CUTOFF :
                    dead += 1

                else :
                    live += 1
            self.dead_col.append(dead)
            self.live_col.append(live)
            self.none_col.append(none)



    def make_smooth_dists(self) :
        """
        """
        try :
            self.dists
        except AttributeError :
            self.make_dists()

        self.smooth_dists = {}
        for cell_name in self.dists :
            self.smooth_dists[cell_name] = mov_avg(self.dists[cell_name])

    def remove_upper_outliers(self) :
        for cell_name in self.dists :
            for i in range(len(self.dists[cell_name])) :
                if not self.dists[cell_name][i] == None :
                    if self.dists[cell_name][i] > Condit.UPPER_CUTOFF :
                        self.dists[cell_name][i] = None

    def trim_dists(self) :
        """
        """
        self.trim_dist_ends()
        self.trim_dist_starts()
        for cell_name in self.dists :
            self.dist_len = len(self.dists[cell_name])
            break

    def trim_dist_ends(self) :
        """
        """
        ## use break instead of return??
        while(True) :
            for col in self.dists.values() :
                if col[-1] != None :
                    return
            for col_key in self.dists :
                self.dists[col_key] = self.dists[col_key][:-1]

    def trim_dist_starts(self) :
        """
        """
        ## use break instead of return??
        while(True) :
            for col in self.dists.values() :
                if col[0] != None :
                    return
            for col_key in self.dists :
                self.dists[col_key] = self.dists[col_key][1:]

    def fix_dists_zeros(self) :
        """
        """

        pattern = [None, 0.0]
        for col_key in self.dists:
            index = pattern_in_list(self.dists[col_key], pattern)

            if index == -1 :
                if self.dists[col_key][0] == 0 :
                    self.dists[col_key][0] = None
            else :
                self.dists[col_key][index + 1] = None


    def __str__(self) :
        """
        """

        return "{}: {}".format(self.name, list(self.wells.keys()))

    ## bad practice
    def __repr__(self) :
        """
        """
        return self.__str__()
