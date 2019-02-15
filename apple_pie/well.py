
# from .ap_utils import *
# from brutils import *

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

    @staticmethod
    def lever_csv_to_dict(csv_path) :
        """
            5 cols, not 4
        """
        rows = csv_to_rows(csv_path)
        cols = rotate(rows)
        col_dict = {}

        ## ce as in cell, co as in col
        for ce in range(0,len(cols),5) :
            for co in range(0,5) :
                col_tuple_key = (cols[ce][0], cols[ce+co][3])
                col_dict[col_tuple_key] = cols[ce+co][4:]

        return col_dict
