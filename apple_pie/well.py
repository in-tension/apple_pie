
from .ap_utils import *

class Well :
    def __init__(self, exper, well_name, csv_path) :
        self.exper = exper
        self.name = well_name
        self.path = csv_path

        self.raw_data = lever_csv_to_dict(csv_path)

        ## fix distance columns

        self.cell_count = len(self.raw_data.keys())/self.exper.COL_COUNT


    def __str__(self) :
        """
        """
        return("apple_pie.Well: {}".format(self.name))

    ## bad practice
    def __repr__(self) :
        """
        """
        return self.__str__()
