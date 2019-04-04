import os
from os.path import join as pjoin
import time

def recurs_dir(path) :

    subdirs = os.listdir(path)

    dir_list = []
    for subdir in subdirs :
        subpath = pjoin(path,subdir)
        if os.path.isdir(subpath) :
            dir_list.append(subpath)
            dir_list.extend(recurs_dir(subpath))
    return dir_list

root = ('/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/' + 
    'Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/' +
    'Post-mycoplasma data (starting 9:18:18)')

start_time = time.time()
print(recurs_dir(root))

elapsed_time = time.time() - start_time
print(elapsed_time)

