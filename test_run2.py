


import os
import time

from matplotlib import pyplot as plt
import matplotlib.colors

import apple_pie as ap



path = '/Users/baylieslab/Documents/Amelia/ap/data/18-11-06'



my_exper = ap.Exper(path)

# condit_keys = sorted(list(my_exper.condits.keys()))
# condit = my_exper.condits[condit_keys[18]]
# print(condit.name)
# dists = condit.distances
# cks = sorted(list(dists.keys()))     ## ck = cell_keys
# coords = condit.coords_as_cols
# ccks = sorted(list(coords.keys()))     ## ck = coord_cell_keys
#
#
# t_int = [x/6 for x in range(1,97)]
#
# col1 = dists[cks[0]]
#
# # ap.col_dict_to_csv(condit.coords, 'testing.csv')
# ap.col_dict_to_csv(condit.distances, 'testing.csv')
# #print(condit.coords)
#
# i = 0
# for ck in coords :
#     #print(condit.coords[cell_name])
#     #break
#     if i == 10 :
#         i = 0
#         plt.clf()
#     print(coords[ck][0])
#     print(coords[ck][1])
#
#     plt.scatter(coords[ck][0],coords[ck][1], c=[x for x in range(len(coords[ck][0]))], cmap='viridis')
#
#     plt.ylim((0,1024))
#     plt.xlim((1,1024))
#
#     plt.pause(1)
#     i+= 1



# for ck in cks :
#     plt.clf()
#     plt.scatter(t_int,dists[ck])#, c=t_int, cmap='viridis')
#
#     plt.plot(t_int,dists[ck])
#     plt.ylim(top=50)
#
#     plt.pause(1)
