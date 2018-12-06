

#from .Exper import Exper
#from apple_pie import Exper
#from .exper import Exper
#import exper
#from .exper import Exper.COLS_5
from .ap_utils import *

class Condit :
    DEAD_CUTOFF = 3
    DEAD_FRAME_COUNT = 10

    def __init__(self,exper,name,well_names) :
        """
        """
        self.exper = exper
        self.name = name
        self.make_name_str()

        self.wells = {}
        for well_name in well_names :
            self.wells[well_name] = self.exper.wells[well_name]

        self.get_all_distances()
        self.get_all_coords()

        self.dist_to_csv()

    def make_name_str(self) :
        """
        """
        temp = []
        for term in self.name :
            temp.append(str(term))
        self.name_str = self.exper.NAME_DELIM.join(temp)
        #for term in self.name :
            #self.



    def dist_to_csv(self) :
        out_file = os.path.join(self.exper.condit_dist_path, self.name_str + self.exper.CONDIT_DIST_SUF)

        col_dict_to_csv(self.distances,out_file)


    

    ## assumes self.distances already exists
    def _find_dead(self) :

        logi_col = []
        for cell_name in self.distances :
            for dist in self.distances[cell_name] :
                if dist == None :
                    loci_col.append(None)
                elif dist < Condit.DEAD_CUTOFF :
                    logi_col.append(0)
                else :
                    loci_col.append(1)

            ## can't be the most efficient way to do this
            #pattern_in_list()


    def find_dead(self) :
        """
        idk
        """
        for cell_name in self.distances :

            logi_col = []
            mbd = False ## mbd = might_be_dead
            mbd_count

            for dist in self.distances[cell_name] :

                ## != None because I think error if you try None < 3
                if dist != None and dist < 3 :
                    pass

                # if dist == None :
                #     loci_col.append(None)
                # elif dist < Condit.DEAD_CUTOFF :
                #     logi_col.append(0)
                # else :
                #     loci_col.append(1)


    ## assumes every x has a y before the next x
    ## this function could probably be more efficient
    ## this function could probably more compact w/ less steps but I don't know if it would increase or decrease readability
    def get_all_coords(self) :
        """
        """
        self.coords_as_cols = {}
        for well in self.wells.values() :
            for key in well.raw_data.keys() :
                #if key[1]
                #(key)
                if key[1] == self.exper.COLS_5[0] :    ## COLS_5[0] -> x
                    col = arr_cast_spec(well.raw_data[key],float)
                    #col = well.raw_data[key]
                    self.coords_as_cols[(well.name, 'cell {}'.format(key[0]))] = [col]
                if key[1] == self.exper.COLS_5[1] :    ## COLS_5[1] -> y
                    col = arr_cast_spec(well.raw_data[key],float)
                    #col = well.raw_data[key]

                    self.coords_as_cols[(well.name, 'cell {}'.format(key[0]))].append(col)


        self.coords = {}

        for cell_name in self.coords_as_cols :
            """
            """
            xs = self.coords_as_cols[cell_name][0]
            ys = self.coords_as_cols[cell_name][1]
            #print('len(xs) = {}'.format(len(xs)))
            #print('len(ys) = {}'.format(len(ys)))

            temp_cell_coords = []
            for x,y in zip(xs,ys) :
                #print('x = {}, y = {}'.format(x,y))
                # if x == '' :
                #     x = None
                # else :
                #     try :
                #         x = float(x)
                #     except :
                #         pass
                #
                #
                # if y == '' :
                #     y = None
                # else :
                #     try :
                #         y = float(y)
                #     except :
                #         pass

                temp_cell_coords.append([x,y])
            self.coords[cell_name] = temp_cell_coords





    def get_all_distances(self) :
        """
        """
        #from .exper import Exper

        self.distances = {}
        for well in self.wells.values() :
            for key in well.raw_data.keys() :
                if key[1] == self.exper.COLS_5[4] :
                    self.distances[(well.name,'cell {}'.format(key[0]))] = well.raw_data[key]

        for col in self.distances.values() :
            for i in range(len(col)) :
                if col[i] == '' :
                    col[i] = None
                else :
                    try :
                        col[i] = float(col[i])
                    except :
                        print("oh no, well csv value not a number")

        self.cell_count = len(self.distances.keys())

        check_count = 0
        for well in self.wells.values() :
            check_count += well.cell_count
        if check_count != self.cell_count :
            print('fuck, condit cell_count wrong')

        self.fix_distances_zeros()
        self.trim_distances()
                    #print(key)


    def trim_distances(self) :
        """
        """
        #print("trimming")
        self.trim_dist_ends()
        self.trim_dist_starts()

    def trim_dist_ends(self) :
        """
        """
        ## use break instead of return??
        while(True) :
            for col in self.distances.values() :
                if col[-1] != None :
                    return
            for col_key in self.distances :
                self.distances[col_key] = self.distances[col_key][:-1]

    def trim_dist_starts(self) :
        """
        """
        ## use break instead of return??
        while(True) :
            for col in self.distances.values() :
                if col[0] != None :
                    return
            for col_key in self.distances :
                self.distances[col_key] = self.distances[col_key][1:]



    def fix_distances_zeros(self) :
        """
        """
        show = self.name == ('BYL ', 0.009765625)

        pattern = [None, 0.0]
        for col_key in self.distances:
            index = pattern_in_list(self.distances[col_key], pattern)
            # if show :
            #     print(self.distances[col_key])
            #     print(index)
            #     input()
            if index == -1 :
                if self.distances[col_key][0] == 0 :
                    self.distances[col_key][0] = None
            else :
                self.distances[col_key][index + 1] = None




    def __str__(self) :
        """
        """
        #return "apple_pie.Condit: {} {}".format(self.name, list(self.wells.keys()))
        return "{}: {}".format(self.name, list(self.wells.keys()))

    ## bad practice
    def __repr__(self) :
        """
        """
        return self.__str__()
