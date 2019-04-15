
# from .ap_utils import *
from brutils import *
import pandas as pd

from . import hdings
class Well :
    def __init__(self, exper, well_name, csv_path) :
        self.exper = exper
        self.name = well_name
        self.path = csv_path

        #self.raw_data = Well.lever_csv_to_dict(csv_path)
        self.cdf = pd.read_csv(csv_path)
        self.cdf[hdings.WELL] = self.name


        ## fix distance columns

        # self.cell_count = len(self.raw_data.keys())/self.exper.COL_COUNT
        # self.cell_count = len(self.raw_data)
        CELL_IDFYIER = 'Track ID'
        self.cell_count = set(self.cdf[CELL_IDFYIER])


    def __str__(self) :
        """
        """
        return("apple_pie.Well: {}".format(self.name))

    ## bad practice?
    def __repr__(self) :
        """
        """
        return self.__str__()

    def create_dists(self) :
        pass



    # TODO deal with old/new function in a reasonable way

    @staticmethod
    def lever_csv_to_dict_old(csv_path):
        """
            5 cols, not 4
        """
        rows = csv_to_rows(csv_path)
        cols = rotate(rows)
        col_dict = {}

        ## ce as in cell, co as in col
        for ce in range(0, len(cols), 5):
            for co in range(0, 5):
                col_tuple_key = (cols[ce][0], cols[ce + co][3])
                col_dict[col_tuple_key] = cols[ce + co][4:]

        return col_dict

    @staticmethod
    def lever_csv_to_dict(csv_path):
        """
            output with all cells in same columns, labelled with track id
            returns cells -> {cell_id : pd.df}
        """
        CELL_IDFYIER = 'Track ID'

        df = pd.read_csv(csv_path)

        cell_ids = set(df[CELL_IDFYIER])
        cells = {}
        for cell_id in cell_ids:
            cells[cell_id] = df[df[CELL_IDFYIER] == cell_id]

        return cells


