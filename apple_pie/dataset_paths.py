from os.path import join as pjoin

RHABDO_ROOT = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'       ## mac only

RH30_PATH = pjoin(RHABDO_ROOT, 'RH30')      ## mac only


RHABDO_LOC = '/Users/baylieslab/Documents/Amelia/data/rhabdo'
EXP18_18_11_09_DIR = '18-11-09.ap'


cur_dataset_path = pjoin(RHABDO_LOC, EXP18_18_11_09_DIR)




from .exper import Exper

def make_cur_exper() :
    return Exper(cur_dataset_path)
