from brutils import *
# from .hdings import *
import pandas as pd
from termcolor import colored
import matplotlib as mpl
# from matplotlib import cm
from scipy.misc import imread
from os.path import join as pjoin



from . import hdings
from . import hdings as hs
class Well :
    def __init__slow(self, exper, well_name, csv_path) :
        self.exper = exper
        self.name = well_name
        print(self.name)
        self.path = csv_path
        # self.read_in_compare()

        #self.raw_data = Well.lever_csv_to_dict(csv_path)
        # try :
        self.cdf = pd.read_csv(csv_path)
        # except Exception as e :
        #     print("{} : ".format(self.name) + colored(str(e),'red'))


        self.cdf[hdings.WELL] = self.name
        self.cdf[hdings.DIST] = np.nan


        # print(self.name)
        # print(self.cdf.columns)
        #CELL_IDFYIER = 'Track ID'
        self.cell_count = len(set(self.cdf[hdings.T_ID]))
        self.create_dists_slow()


    def __init__(self, exper, well_name, csv_path) :
        self.exper = exper
        self.name = well_name
        print(self.name)
        self.path = csv_path

        self.read_in_compare()
        self.create_dists_compare()
        self.remake_df1()
        # print(self.cdf2)

    def __str__(self) :
        """
        """
        return("{}: well {}".format(self.condit.name_str,self.name))

    ## bad practice?
    def __repr__(self) :
        """
        """
        return("apple_pie.Well: {}".format(self.name))

    def set_condit(self, condit) :
        self.condit = condit

    def create_dists_slow(self) :
        at = dtic('call from well.create_dists')
        self.cdf = self.cdf.groupby(hdings.T_ID).apply(create_df_dists2,hdings.X,hdings.Y,hdings.DIST,hdings.FRAME)
        dtoc(at)
        bt = dtic('reset_index')
        self.cdf.reset_index(drop=True)
        dtoc(bt)
        return

    def read_in_compare(self) :
        self.cdf = pd.read_csv(self.path)
        self.cells = {}
        for g,group in self.cdf.groupby(hdings.T_ID) :
            temp = group.to_dict(orient='list')
            # print(temp[hdings.T_ID])
            self.cells[temp[hdings.T_ID][0]] = temp

    def remake_df1(self) :
        cell_keys = list(self.cells.keys())
        #self.cdf2 = pd.DataFrame(self.cells[cell_keys[0]])
        self.combined = self.cells[cell_keys[0]]
        keys = set(self.combined.keys())

        for cell_key in cell_keys[1:] :
            to_add = self.cells[cell_key]
            if not len(keys ^ set(to_add.keys())) == 0 :
                raise Exception
            else :
                for key in keys :
                    self.combined[key].extend(to_add[key])

        self.cdf2 = pd.DataFrame(self.combined)

        #self.cdf2.append(pd.DataFrame(self.cells[cell_key]))

    def remake_df2(self) :
        cell_keys = list(self.cells.keys())
        self.cdf2 = pd.DataFrame(self.cells[cell_keys[0]])
        for cell_key in cell_keys[1:] :
            #self.cdf2.concat(self.cells[cell_key])
            self.cdf2 = pd.concat([self.cdf2,pd.DataFrame(self.cells[cell_key])], ignore_index=True)
            # print(type(self.cells[cell_key]))
            # self.cdf2.append(self.cells[cell_key])
            # self.cdf2.merge(pd.DataFrame(self.cells[cell_key]))

    def create_dists_compare(self) :
        for cell in self.cells.values() :
            cell[hs.DIST] = [np.nan]*len(cell[hs.T_ID])
            # print('len(cell) : {}, len(cell[hs.x]) : {}'.format(len(cell),len(cell[hs.X])))
            for r in range(len(cell[hs.T_ID])-1) :
                if cell[hs.FRAME][r] + 1 == cell[hs.FRAME][r+1] :
                    # print(len(cell))
                    xs = cell[hs.X][r:r+2]
                    ys = cell[hs.Y][r:r+2]
                    # print(xs)
                    # print(ys)
                    # print(cell[hs.DIST])
                    # print(r)
                    cell[hs.DIST][r] = distance([xs[0],ys[0]],[xs[1],ys[1]])



    @staticmethod
    def lever_csv_to_dict_old(csv_path):
        """
            5 cols, not 4
        """
        rows = csv_to_rows(csv_path)
        cols = rotate(rows)
        col_dict = {}

        ## ce as in cell, co as in col
        for ce in range(0, len(cols), 5):
            for co in range(0, 5):
                col_tuple_key = (cols[ce][0], cols[ce + co][3])
                col_dict[col_tuple_key] = cols[ce + co][4:]

        return col_dict


    @staticmethod
    def some_condition(cur_group):
        if len(cur_group) <= 5:
            return False
        else:
            return True


    def plot_looper(self) :
        WellPlotLooper(self.cdf2,  hdings.T_ID, hdings.FRAME, hdings.DIST, hdings.X, hdings.Y, self.exper.path, self.name, title=str(self), some_condition=Well.some_condition)


class WellPlotLooper(DfPlotLooper2) :
    MAX_PROJECT_DIR = 'Czi/max_projection_gifs'
    def __init__old(self, x_name2, y_name2, *args, **kwargs) :
        self.x_name2 = x_name2
        # print(self.x_name2)
        self.y_name2 = y_name2
        self.ax1 = None
        self.ax2 = None
        # self.ax1 = plt.subplot(1,2,1)
        # self.ax2 = plt.subplot(1,2,2)
        super(WellPlotLooper, self).__init__(*args, **kwargs)
        # self.ax1 =
        # self.ax2 = self.fig.add_subplot(1,2,2)

    def __init__(self, well_df, group_by_col, frame_col, dist_col, x_col, y_col, exper_path, well_name, title=None, override_defaults=None, some_condition=None) :
        """
            | :param: override_defaults : `dict` with keys of settings to override and the desired values
            | :param: some_condition : a function which takes the `cur_group()` and returns False if it should not be plotted and `incr`/`decr` should be called again,
            | when equal None, doesn't do the test and plots every group
        """
        #
        # self.exper_path = exper_path
        # self.well_name = well_name

        out_folder = pjoin(exper_path, WellPlotLooper.MAX_PROJECT_DIR)
        self.out_path = self.helper_find_file(out_folder, well_name)
        # return out_path

        self.settings = DfPlotLooper2.DEFAULTS
        if override_defaults != None:
            for key in override_defaults:
                self.settings[key] = override_defaults[key]

        self.grouped_df = well_df.groupby(group_by_col)
        self.group_by_col = group_by_col
        self.group_names = list(self.grouped_df.groups.keys())
        self.ind = 0
        self.max_ind = len(self.group_names)

        self.frame_col = frame_col
        self.dist_col = dist_col
        self.x_col = x_col
        self.y_col = y_col

        self.title = title
        self.some_condition = some_condition

        # self.fig = plt.figure(figsize=self.settings['figsize'],tight_layout=True)
        self.fig = plt.figure(figsize=self.settings['figsize'])  # ,tight_layout=True)
        if self.title != None:
            self.fig.suptitle(self.title)
        self.fig.show()



        self.cmap_array = mpl.cm.get_cmap('viridis',self.settings['xlim'][1]).colors

        self.ax_prev = plt.axes(self.settings['next_button_loc'])
        self.ax_next = plt.axes(self.settings['prev_button_loc'])
        self.b_next = Button(self.ax_next, 'Next')
        self.b_prev = Button(self.ax_prev, 'Prev')
        self.b_next.on_clicked(self.next)
        self.b_prev.on_clicked(self.prev)

        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.ax2 = self.fig.add_subplot(1, 2, 2)

        try:
            matplotlib.rcParams['keymap.back'].remove('left')
            matplotlib.rcParams['keymap.forward'].remove('right')
        except Exception:
            pass
        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)

        self.plot()

        # plt.show()      # I think this might prevent python interpreter from closing
                        # also prevents interactive interpreter from continuing
                        # comment out if using -i




    def plot(self) :

        self.ax1.cla()

        cur_colors = self.cur_cmap()

        self.ax1.set_title("{} : {}".format(self.group_by_col, self.group_names[self.ind]))
        self.cur_group().plot(self.frame_col, self.dist_col, kind='scatter', ax=self.ax1, c=cur_colors)#,colormap=cm.get_cmap('viridis'))
        # self.cur_group().plot(self.x_name, self.y_name, kind='scatter', ax=self.ax1)

        self.ax1.set_xlim(self.settings['xlim'])
        self.ax1.set_ylim(self.settings['ylim'])


        # plt.subplot(1,2,2)
        # ax2 = plt.gca()
        self.ax2.cla()

        self.ax2.set_title("{} : {}".format(self.group_by_col, self.group_names[self.ind]))
        # colormap = mpl.cm.get_cmap('viridis',len(self.cur_group()))
        # colormap.set_array(self.cur_group_col(self.x).get_values)
        img = imread(self.out_path)
        plt.imshow(img,zorder=0)
        self.cur_group().plot(self.x_col, self.y_col, kind='scatter', ax=self.ax2, c=cur_colors,zorder=1)
        # self.cur_group().plot(self.x_name2, self.y_name2, kind='scatter', ax=self.ax2)

        self.ax2.set_xlim([0,1024])
        self.ax2.set_ylim([0,1024])
        self.ax2.invert_yaxis()
        # self.ax2.xaxis.tick_top()

        plt.draw()
        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)

    def cur_cmap(self) :
        cur_frames = self.cur_group_col(self.frame_col).values
        cur_colors = []

        for f in cur_frames :
            cur_colors.append(self.cmap_array[f])
        return cur_colors

    @staticmethod
    def helper_find_file(path, pattern):
        """
        """
        for file_name in os.listdir(path):
            if pattern in file_name:
                return os.path.join(path, file_name)