import os
import time
import tkinter
from tkinter import ttk


import matplotlib
matplotlib.use("TkAgg")


from matplotlib import pyplot as plt
import matplotlib.colors

import apple_pie as ap

# import .apple_pie.dir_gui


#path = '/Users/baylieslab/Documents/Amelia/ap/data/18-11-06'
#
# root_path = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'
#
# ## /RH30/20181106'
#
#
# rh30_root_path = os.path.join(root_path, 'RH30')
# # print(rh30_root_path)
# # rh30_runs = os.listdir(rh30_root_path)
#
# # print(rh30_runs)
#
#
# rh30_runs = []
# with os.scandir(rh30_root_path) as scan :
#     for entry in scan :
#         if entry.is_dir() and entry.name.startswith('20') :
#             rh30_runs.append(entry.name)
#
# rh30_runs = sorted(rh30_runs)
#
#
# exper_path = os.path.join(rh30_root_path,rh30_runs[-1])
# print(exper_path)
e = ap.Exper(ap.cur_dataset_path)
# print(exper_path)
#
#
# print(rh30_runs)

# ap.dir_gui(rh30_root_path)
# dir_gui(rh30_root_path)
# ap.dir_gui('.')
