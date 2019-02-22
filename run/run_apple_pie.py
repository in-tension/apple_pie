import sys
import os

## append module root directory to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from apple_pie import *

e = dataset_paths.make_cur_exper()
