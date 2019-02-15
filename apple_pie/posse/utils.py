from os.path import join as pjoin

RHABDO_ROOT = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'       ## mac only

RH30_PATH = pjoin(RHABDO_ROOT, 'RH30')      ## mac only

RHABDO_LOC = '/Users/baylieslab/Documents/Amelia/data/rhabdo'


def make_loc_posse() :
    from .the_posse import ThePosse
    return ThePosse(RHABDO_LOC)


def make_rh30_posse() :
    from .the_posse import ThePosse
    return ThePosse(RH30_PATH)


def project_root_to_path() :
    
