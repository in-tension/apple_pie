from os.path import join as pjoin

RHABDO_ROOT = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'       ## mac only

RH30_PATH = pjoin(RHABDO_ROOT, 'RH30')      ## mac only


RHABDO_LOC = '/Users/baylieslab/Documents/Amelia/data/rhabdo/rht'
EXP18_18_11_09_DIR = '18-11-09.rht'
EXP18_18_11_06_DIR = '18-11-06.rht'
EXP18_18_11_07_DIR = '18-11-07.rht'
EXP18_18_11_30_LOC_DIR = 'RH30_18-11-30.rht'
EXP18_18_11_07_LOC_DIR = 'RH30_18-11-07.rht'
EXP18_18_09_27_LOC_DIR = 'RH30_18-09-27.rht'


cur_dataset_path = pjoin(RH30_PATH, EXP18_18_11_07_DIR)
cur_dataset_path = pjoin(RHABDO_LOC, EXP18_18_11_07_LOC_DIR)




from .exper import Exper

def make_cur_exper() :
    return Exper(cur_dataset_path)
