from datetime import datetime


import xlsxwriter
import matplotlib.pyplot as plt
import numpy as np

# from .ap_utils import *
from brutils import *


from . import hdings

class RecordedIssue(Exception) :
    pass


class Condit :

    """
    """

    DEAD_CUTOFF = 3
    DEAD_FRAME_COUNT = 10
    UPPER_CUTOFF = 50




    def __init__(self, exper, name, well_names) :
        """
        """
        try :

            self.exper = exper
            """ """
            self.name = name
            self.name_str = tuple_to_str(self.name)

            self.data = self.exper.wells[well_names[0]]
            self.wells = {}
            for well_name in well_names[1:] :
                try :
                    self.wells[well_name] = self.exper.wells[well_name]
                    # self.wells.append(self.exper.wells[well_name])
                    self.wells[well_name].set_condit(self)
                except :
                    self.record_issue('cell.__init__(...)',['missing well'],well=[well_name])

            # self.init_dists()

            # {self.make_cleaned_dists()
            #
            # col_dict_np_nan(self.dists)
            # col_dict_np_nan(self.cleaned_dists)
            #
            # try :
            #     self.dist_meds = col_dict_row_nanmed(self.dists)
            #     self.dist_means = col_dict_row_nanmean(self.dists)
            #     self.cleaned_dist_meds = col_dict_row_nanmed(self.cleaned_dists)
            #     self.cleaned_dist_means = col_dict_row_nanmean(self.cleaned_dists)
            # except :
            #     self.record_issue('cell.__init__ calling col_dict_row_nan<med>(self.<>dists)',['this can be caused by some columns having more time points than other columns'])
            #self.dists = {}
            # }""" dists """


        except RecordedIssue :
            pass
        #{

        self._smooth_dists = None
        self._cleaned_dists = None

        self._dist_meds = None
        self._dist_means = None

        self._cleaned_dist_meds = None
        self._cleaned_dist_means = None

        self._coords = None
        self._coord_cols = None



        self._dead_col = None
        self._live_col = None
        self._none_col = None

        self._dist_mean_mean = None

        self._norm_dist_means = None
        self._norm_mean_mean = None
        #}

    # def make_normalized(self) :

    def __getitem__(self, term) :
        return self.wells[term]

    @property

    def norm_dist_means(self) :
        """ """
        if self._norm_dist_means is None :

            if self.time_point_count != self.exper.control.time_point_count :
                print('issue in condit.normalized')
                raise Exception

            self.norm_dist_means = []
            for t in range(self.time_point_count) :
                self.norm_dist_means.append(self.cleaned_dist_means[t]/self.exper.control.cleaned_dist_means[t])
        return self._norm_dist_means
    @norm_dist_means.setter
    def norm_dist_means(self,value) :
        self._norm_dist_means = value


    @property
    def norm_mean_mean(self) :
        if self._norm_mean_mean is None :
            self._norm_mean_mean = np.nanmean(self.norm_dist_means)
        return self._norm_mean_mean

    @norm_mean_mean.setter
    def norm_mean_mean(self, value) :
        self._norm_mean_mean = value

        # print('i hate everything')






    @property
    def dist_mean_mean(self) :

        if self._dist_mean_mean is None :
        # takes mean of each time point, and not of every cell velocity
        # a cell velocity in a time point with less data
            self._dist_mean_mean = np.nanmean(self.dist_means)
        return self._dist_mean_mean
    @dist_mean_mean.setter
    def dist_mean_mean(self, value) :
        self._dist_mean_mean = value


    # def make_cen_tens(self) :
    #     self._dist_meds = col_dict_row_nanmed(self.dists)
    #     self._dist_means = col_dict_row_nanmean(self.dists)
    #
    #
    #     self._cleaned_dist_meds = col_dict_row_nanmed(self.cleaned_dists)
    #     self._cleaned_dist_means = col_dict_row_nanmean(self.cleaned_dists)



    def out_plot_a(self) :
        """
            plots control and condit dist_med and cleaned_dist_med
            and a chart of live/dead/no data cells per time point

            uses self.
            * t_int
            * (exper.control.dist_meds)
            * (exper.conttrol.cleaned_dist_meds)
            * dist_meds
            * cleaned_dist_meds
            * name_str
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

        ax.fill_between(self.t_int, self.live_col,label = 'live cells', step='mid', color='#B47C45')
        ax.fill_between(self.t_int, temp_dead_col, y2=self.live_col, label = 'dead cells', step='mid', color='#1F77B4')
        ax.fill_between(self.t_int, temp_none_col, y2=temp_dead_col, label='no data', step='mid', color='#dbdbdb')

        ax.set_ylim((0,60))
        ax.legend()


        plt.savefig(plot_file)

    def out_dists_to_csv(self) :
        """
            writes ``self.dists`` to a csv file
        """



        out_file = os.path.join(self.exper.condit_dist_path, self.name_str + self.exper.CONDIT_DIST_SUF)

        col_dict_to_csv(self.dists,out_file)


    def out_to_sheet(self, w_book, col_dict) :
        w_sheet = w_book.add_worksheet(self.name_str)
        col_dict_to_sheet(col_dict, w_sheet)
        self.helper_xlsx_formats(w_sheet,1,0,self.time_point_count,self.cell_count)

    def out_dists_to_sheet(self, w_book) :
        """
            writes distances to an xlsx worksheet
        """
        self.out_to_sheet(w_book,self.dists)

    def out_cleaned_dists_to_sheet(self, w_book) :
        """
            writes cleaned distances to an xlsx worksheet
        """

        self.out_to_sheet(w_book,self.cleaned_dists)


    def helper_xlsx_formats(self, w_sheet, r1, c1, r2, c2) :
        """

        """
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['yellow'])
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['red'])
        w_sheet.conditional_format(r1,c1,r2,c2, self.exper.format_dicts['white'])


    ## this function could probably be more efficient
    ## this function could probably more compact w/ less steps but I don't know if it would increase or decrease readability
    def make_coords(self) :
        """
            | goes through ``self.wells`` and creates ``self._coords``
            | a ``ColDict`` of the coordinates of cells in condit

            .. note: assumes every x has a y before the next x
        """
        self._coord_cols = {}

        ## change this to for well_name in self.wells
        ## so as consistent through out
        for well in self.wells.values() :
            for key in well.raw_data.keys() :
                if key[1] == self.exper.COLS_5[0] :    ## COLS_5[0] -> x
                    col = arr_cast_spec(well.raw_data[key],float)
                    self._coord_cols[(well.name, 'cell {}'.format(key[0]))] = [col]
                if key[1] == self.exper.COLS_5[1] :    ## COLS_5[1] -> y
                    col = arr_cast_spec(well.raw_data[key],float)

                    self._coord_cols[(well.name, 'cell {}'.format(key[0]))].append(col)

        self._coords = {}

        for cell_name in self._coord_cols :

            xs = self._coord_cols[cell_name][0]
            ys = self._coord_cols[cell_name][1]


            temp_cell_coords = []
            for x,y in zip(xs,ys) :
                temp_cell_coords.append([x,y])
            self._coords[cell_name] = temp_cell_coords


    #{ def make_cleaned_dists(self) :
    #     """
    #         creates ``self.cleaned_dists`` with "dead" cells removed
    #     """
    #
    #     # try :
    #     #     self.dead_col
    #     # except :
    #     #     self.make_death_counts()
    #
    #     self._cleaned_dists = {}
    #
    #     for cell_name in self.smooth_dists :
    #         temp_col = []
    #
    #         for r in range(len(self.smooth_dists[cell_name])) :
    #             if self.smooth_dists[cell_name][r] is None :
    #                 temp_col.append(None)
    #             elif self.smooth_dists[cell_name][r] < Condit.DEAD_CUTOFF :
    #                 temp_col.append(None)
    #             else :
    #                 temp_col.append(self.dists[cell_name][r])
    #
    # }        self._cleaned_dists[cell_name] = temp_col


    def make_death_counts(self) :
        """
            for each timepoint
            makes self.
            * _dead_col
            * _live_col
            * _none_col
        """


        self._dead_col = []
        self._live_col = []
        self._none_col = []


        for r in range(self.time_point_count) :
            dead = 0
            live = 0
            none = 0
            for cell_name in self.smooth_dists :

                try :
                    if self.smooth_dists[cell_name][r] is None :
                        none += 1

                    elif self.smooth_dists[cell_name][r] < Condit.DEAD_CUTOFF :
                        dead += 1

                    else :
                        live += 1
                except :
                    self.record_issue('condit.make_death_counts(self)', ['some distance columns have less time points than other columns'], well=cell_name)
                    raise RecordedIssue
            self._dead_col.append(dead)
            self._live_col.append(live)
            self._none_col.append(none)


    # {def make_smooth_dists(self) :
    #     """
    #     """
    #     # try :
    #     #     self.dists
    #     # except AttributeError :
    #     #     self.init_dists()
    #
    #     self._smooth_dists = {}
    #     for cell_name in self.dists :
    #   }      self._smooth_dists[cell_name] = mov_avg(self.dists[cell_name])



    def record_issue(self, method_name, msg, well=None, cell=None, assoc_files=None) :

        info_list = [(datetime.datetime.today().strftime('%y-%m-%d %H:%M'))]
        #info_list = [(datetime.datetime.today().strftime('%y-%m-%d %H:%M'))]
        # info_list = [(datetime.datetime.today().isoformat())]

        if well != None :
            info_list.extend(well)

            if cell != None :
                info_list.append(': '.format(cell))

        info_list.append(method_name)
        info_list.extend(msg)
        if assoc_files != None :
            info_list.append('associated output files:{}'.format(assoc_files))

        #self.exper.issue_log[self.name_str] = info_list
        if self.name_str in self.exper.issue_log :
            self.exper.issue_log[self.name_str].append(info_list)
        else :
            self.exper.issue_log[self.name_str] = [info_list]


    ## <all functions called inside __init__>
    def init_dists_old(self) :
        """
            | gets distance columns from wells
            | removes weird zeros and leading and trailing blank rows

            creates

            * dists
            * cell_count
            * time_point_count (init_trim_dists)
            * t_int
        """

        self.dists = {}
        """ dists """

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

        self.init_fix_dists_zeros()
        self.init_trim_dists()
        self.init_remove_upper_outliers()
        #self.t_int = [x/6 for x in range(1,self.time_point_count+1)]
        self.t_int = self.exper.make_t_int(self.time_point_count)

    def init_dists_old2(self):
        # {
        """
            | gets distance columns from wells
            | removes weird zeros and leading and trailing blank rows

            creates

            * dists
            * cell_count
            * time_point_count (init_trim_dists)
            * t_int
        """
        # }

        self.dists = {}
        """ dists """

        for well in self.wells.values():
            for key in well.raw_data.keys():
                if key[1] == self.exper.COLS_5[4]:
                    self.dists[(well.name, 'cell {}'.format(key[0]))] = well.raw_data[key]

        for col in self.dists.values():
            for i in range(len(col)):
                if col[i] == '':
                    col[i] = None
                else:
                    try:
                        col[i] = float(col[i])
                    except:
                        print("oh no, well csv value not a number")

        self.cell_count = len(self.dists.keys())

        check_count = 0
        for well in self.wells.values():
            check_count += well.cell_count
        if check_count != self.cell_count:
            print('fuck, condit cell_count wrong')

        self.init_fix_dists_zeros()
        self.init_trim_dists()
        self.init_remove_upper_outliers()
        # self.t_int = [x/6 for x in range(1,self.time_point_count+1)]
        self.t_int = self.exper.make_t_int(self.time_point_count)

    def init_dists(self) :
        # {
        """
            | gets distance columns from wells
            | removes weird zeros and leading and trailing blank rows

            creates

            * dists
            * cell_count
            * time_point_count (init_trim_dists)
            * t_int
        """
        # }

        self.dists = {}
        """ dists """
        well_keys = self.wells.keys()

        self.dists = self.wells[well_keys[0]]
        for well_key in well_keys[1:] :
            self.dists.append(self.wells[well_key])
        self.frame_count = self.dists[hdings.FRAME].max()


        self.t_int = self.exper.make_t_int(self.frame_count-1)

    def init_fix_dists_zeros(self) :
        pattern = [None, 0.0]
        for col_key in self.dists:
            index = pattern_in_list(self.dists[col_key], pattern)

            if index == -1 :
                if self.dists[col_key][0] == 0 :
                    self.dists[col_key][0] = None
            else :
                self.dists[col_key][index + 1] = None

    def init_trim_dists(self) :
        self.init_trim_dist_ends()
        self.init_trim_dist_starts()
        for cell_name in self.dists :
            self.time_point_count = len(self.dists[cell_name])
            break

    def init_trim_dist_ends(self) :
        ## use break instead of return??
        while(True) :
            for col in self.dists.values() :
                if col[-1] is not None :
                    return
            for col_key in self.dists :
                self.dists[col_key] = self.dists[col_key][:-1]

    def init_trim_dist_starts(self) :
        ## use break instead of return??
        while(True) :
            for col in self.dists.values() :
                if col[0] is not None :
                    return
            for col_key in self.dists :
                self.dists[col_key] = self.dists[col_key][1:]

    def init_remove_upper_outliers(self) :
        for cell_name in self.dists :
            for i in range(len(self.dists[cell_name])) :
                if not self.dists[cell_name][i] is None :
                    if self.dists[cell_name][i] > Condit.UPPER_CUTOFF :
                        self.dists[cell_name][i] = None
    ## </all functions called inside __init__>


    def __str__(self) :
        """
        """

        return "{}: {}".format(self.name, list(self.wells.keys()))

    def __repr__(self) :
        """
        """
        ## bad practice?
        return self.__str__()

    ## <getters and setters>
    @property
    def smooth_dists(self) :
        if self._smooth_dists is None :
            self._smooth_dists = {}
            for cell_name in self.dists :
                self._smooth_dists[cell_name] = mov_avg(self.dists[cell_name])
        return self._smooth_dists


    @smooth_dists.setter
    def smooth_dists(self, value) :
        self._smooth_dists = value

    @property
    def cleaned_dists(self) :
        if self._cleaned_dists is None :
            self._cleaned_dists = {}

            for cell_name in self.smooth_dists :
                temp_col = []

                for r in range(len(self.smooth_dists[cell_name])) :
                    if self.smooth_dists[cell_name][r] is None :
                        temp_col.append(None)
                    elif self.smooth_dists[cell_name][r] < Condit.DEAD_CUTOFF :
                        temp_col.append(None)
                    else :
                        temp_col.append(self.dists[cell_name][r])

                self._cleaned_dists[cell_name] = temp_col

        return self._cleaned_dists

    @cleaned_dists.setter
    def cleaned_dists(self, value) :
        self._cleaned_dists = value


    @property
    def dist_meds(self) :
        if self._dist_meds is None :

            self._dist_meds = col_dict_row_nanmed(self.dists)
        return self._dist_meds
    @dist_meds.setter
    def dist_meds(self, value) :
        self._dist_meds = value

    @property
    def dist_means(self) :
        if self._dist_means is None :
            self._dist_means = col_dict_row_nanmean(self.dists)
        return self._dist_means
    @dist_means.setter
    def dist_means(self, value) :
        self._dist_means = value

    @property
    def cleaned_dist_meds(self) :
        if self._cleaned_dist_meds is None :
            self._cleaned_dist_meds = col_dict_row_nanmed(self.cleaned_dists)
        return self._cleaned_dist_meds
    @cleaned_dist_meds.setter
    def cleaned_dist_meds(self, value) :
        self._cleaned_dist_meds = value

    @property
    def cleaned_dist_means(self) :
        if self._cleaned_dist_means is None :
            self._cleaned_dist_means = col_dict_row_nanmean(self.cleaned_dists)
        return self._cleaned_dist_means
    @cleaned_dist_means.setter
    def cleaned_dist_means(self, value) :
        self._cleaned_dist_means = value


    @property
    def coords(self) :
        if self._coords is None :
            self.make_coords()
        return self._coords
    @coords.setter
    def coords(self, value) :
        self._coords = value

    @property
    def coord_cols(self) :
        if self._coord_cols is None :
            self.make_coords()
        return self._coord_cols
    @coord_cols.setter
    def coord_cols(self, value) :
        self._coord_cols = value



    @property
    def dead_col(self) :
        if self._dead_col is None :
            self.make_death_counts()
        return self._dead_col
    @dead_col.setter
    def dead_col(self, value) :
        self._dead_col = value

    @property
    def live_col(self) :
        if self._live_col is None :
            self.make_death_counts()
        return self._live_col
    @live_col.setter
    def live_col(self, value) :
        self._live_col = value

    @property
    def none_col(self) :
        if self._none_col is None :
            self.make_death_counts()
        return self._none_col
    @none_col.setter
    def none_col(self, value) :
        self._none_col = value




    ## </getters and setters>
