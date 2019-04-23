
import os


def create_exper_label(experPath) :
    return '_'.join(experPath.split(os.sep)[-2:])



ROOT = ('/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/' +
    'Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/' +
    'Post-mycoplasma data (starting 9:18:18)')

RHT_EXT = '.rht'
CZI_DIR = 'Czi'



rhts = []
for root, dirs, files in os.walk(ROOT) :
    if root.endswith(RHT_EXT) :
        rhts.append(root)

# for rht in rhts :
#     print(create_exper_label(rht))

for r in range(len(rhts)) :
    print("{}. {}".format(r,rhts[r]))




