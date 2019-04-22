import pandas as pd



import sys
import os


import apple_pie as ap
import brutils as br


from matplotlib import pyplot as plt
import numpy as np


from IPython import get_ipython
ipy = get_ipython()
ipy.magic('matplotlib osx')


from matplotlib.widgets import Button

well_file = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)/RH30/18-11-07.rht/Csv/B17.csv'

well_name = 'B17'

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
        self.ax = plt.gca()
        self.plot()


    def plot(self) :
        self.ax.cla()
        self.ax.set_title('Cell {}'.format(self.groups[self.ind]))
        self.cur_group().plot(x, y, kind='scatter', ax=self.ax)
        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-10, 100)
        plt.draw()

    def on_key_press(self,event):
        if event.key == "left" :
            self.decr()
            self.plot()
        elif event.key == "right" :
            self.incr()
            self.plot()

    def __str__(self) :
        return(str(self.groups))

    def incr(self):
        self.ind += 1
        while len(self.cur_group()) < 5 :
            self.ind += 1


    def decr(self) :
        self.ind -= 1
        while len(self.cur_group()) < 5 :
            self.ind -= 1


    def next(self, event):
        self.incr()
        self.plot()

    def prev(self, event):
        self.decr()
        self.plot()



    def cur_group(self):
        return self.grouped.get_group(self.groups[self.ind])




gb = Butts(grouped,x,y)

axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Prev')
bnext.on_clicked(gb.next)
bprev.on_clicked(gb.prev)

plt.gcf().canvas.mpl_connect("key_press_event", gb.on_key_press)


