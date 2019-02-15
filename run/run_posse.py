# from ..apple_pie import posse
import sys
import os

# append module root directory to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
# print(os.path.abspath(__file__))
from apple_pie.posse import *
# p = ThePosse()
p = make_rh30_posse()
# p = make_loc_posse()
