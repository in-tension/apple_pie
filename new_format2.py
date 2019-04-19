import pandas as pd
import brutils as br
import numpy as np
import apple_pie as ap
import brutils as br

import sys
import os
# sys.path.insert(0, "../")
import apple_pie as ap

import apple_pie as ap
import brutils as br


from matplotlib import pyplot as plt
import numpy as np
from IPython.display import display as idisp
# %matplotlib notebook
from IPython import get_ipython
ipy = get_ipython()
ipy.magic('matplotlib osx')


from matplotlib.widgets import Button

well_file = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)/RH30/18-11-07.rht/Csv/B02.csv'

well_name = 'B02'

w = ap.Well('exper',well_name,well_file)

cd_tic = br.dtic('create_dists one well')
w.create_dists()

grouped = w.cdf.groupby(ap.hdings.T_ID)
groups = list(grouped.groups.keys())

x = ap.hdings.FRAME
y = ap.hdings.DIST


import matplotlib as mpl


class Butts(object):

    def __init__(self, grouped,x,y):
        self.grouped = grouped
        self.groups = list(grouped.groups.keys())
        self.ind = 0
        plt.figure(figsize=(10, 5))
        #self.fig = plt.figure()
        #plt.plot()
        #self.cur_group().plot(x, y)
        plt.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
        self.ax = plt.gca()
        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-10, 100)
        plt.show()

        #         self.l, = self.cur_group().plot(x=ap.hdings.FRAME,y=ap.hdings.DIST, kind="scatter")
        # self.l, = plt.plot(self.cur_group()[ap.hdings.FRAME],self.cur_group()[ap.hdings.DIST], 'bo')
        # self.ax = plt.gca()
        # plt.plot(self.cur_group()[ap.hdings.FRAME], self.cur_group()[ap.hdings.DIST], 'bo')

    #@staticmethod
    def on_key_press(self,event):
        # print('butts')
        # print(event.key)
        print(self)
        if event.key == "left" :
            print('l')
            self.ind -= 1

            # # for i, line in enumerate(self.ax.lines):
            # # self.ax.lines.pop(i)
            # # line.remove()
            # # self.ax.lines.pop(0).remove()
            # self.ax.cla()
            # self.ax.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
            # self.ax.set_xlim(0, 120)
            # self.ax.set_ylim(-10, 100)
            # plt.draw()
            self.plot()

        elif event.key == "right" :
            print('r')
            self.ind += 1
            self.ax.cla()
            self.ax.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
            self.ax.set_xlim(0, 120)
            self.ax.set_ylim(-10, 100)
            plt.draw()


    def __str__(self) :
        return(str(self.groups))
    def next(self, event):
        #         print('next')
        self.ind += 1


        #for i, line in enumerate(self.ax.lines):
            #self.ax.lines.pop(i)
            #line.remove()
        #self.ax.lines.pop(0).remove()
        self.ax.cla()
        #self.ax.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
        self.cur_group().plot(x,y,kind='scatter', ax=self.ax)
        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-10, 100)

        # l = lines[0]
        # l.remove()
        # del l
        # del lines
        # # not releasing memory
        # ax.cla()  # this does release the memory, but also wipes out all other lines.

        # self.plot()
        # for i, line in enumerate(self.ax.lines):
        #     self.ax.lines.pop(i)
        #     line.remove()
        # self.ax.plot(self.cur_group()[ap.hdings.FRAME], self.cur_group()[ap.hdings.DIST], 'bo')

    #         self.plot2()
    def plot(self) :
        self.ax.cla()
        # self.ax.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
        self.cur_group().plot(x, y, kind='scatter', ax=self.ax)
        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-10, 100)

        plt.draw()


    def prev(self, event):
        #         print('prev')
        self.ind -= 1
        self.ax.cla()
        self.ax.plot(self.cur_group()[x], self.cur_group()[y], 'bo')
        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-10, 100)
        # self.plot()
        # self.ax.plot(self.cur_group()[ap.hdings.FRAME], self.cur_group()[ap.hdings.DIST], 'bo')
        #
        # self.plot2()

    # def plot(self):
    #     self.cur_group().plot(x,y)
    #     plt.show()
        #         self.ax.set_ylim(0,10)
        # self.ax.plot(self.cur_group()[ap.hdings.FRAME], self.cur_group()[ap.hdings.DIST], 'bo')

    #         plt.draw()
    # self.l.set_xdata(self.cur_group()[ap.hdings.FRAME])
    # self.l.set_ydata(self.cur_group()[ap.hdings.DISTANCE])
    # plt.draw()
    # self.fig.canvas.draw()
    # self.fig.canvas.flush_events()

    def cur_group(self):
        # print(self.groups[self.ind])
        return self.grouped.get_group(self.groups[self.ind])



# grouped = w.cdf.groupby(ap.hdings.T_ID)

gb = Butts(grouped,x,y)


# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.2)

axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Prev')
bnext.on_clicked(gb.next)
bprev.on_clicked(gb.prev)

plt.gcf().canvas.mpl_connect("key_press_event", gb.on_key_press)

# plt.figure()
#
#
# def get_g(grouped,groups,i) :
#     return grouped.get_group(groups[i])
# br.loc_print()
#
#
# inputt = None
# output = None
#
# for i,g in w.cdf.groupby(ap.hdings.T_ID) :
#     inputt = g
#     # print(type(g))
#     # ouptut =
#     br.create_df_dists2(g.copy(),ap.hdings.X,ap.hdings.Y,ap.hdings.DIST,ap.hdings.FRAME)
#     #print(g)
#
#     # output = sum([10,10])
#
#     print(output)
#
#
#     # ln = 24
#     # fn = 'new_format.py'
#     # if output is None:
#     #     print('(new_format.py) {}: output is None'.format(ln))
#     # else:
#     #     print('(new_format.py) {}: output is something'.format(ln))
#     break
#
#
# print(br.rotate([[1]]))
#
# print(br.create_df_dists2(w.cdf,ap.hdings.X,ap.hdings.Y,ap.hdings.DIST,ap.hdings.FRAME))
# # w.cdf.groupby(ap.hdings.T_ID).apply(br.create_df_dists2,ap.hdings.X,ap.hdings.Y,ap.hdings.DIST,ap.hdings.FRAME)
# print(output)


# br.dtoc(cd_tic)

