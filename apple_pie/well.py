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
        self.cdf[hdings.DIST] = np.nan



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

        self.cdf = self.cdf.groupby(hdings.T_ID).apply(create_df_dists2,hdings.X,hdings.Y,hdings.DIST,hdings.FRAME)

        self.cdf.reset_index(drop=True)



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


