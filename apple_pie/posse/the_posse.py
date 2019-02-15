import os



class ThePosse :
    """ """

    EXT = ".ap"
    """pseudo extension for folder containing ex"""

    def __init__(self,root_path) :
        """ """
        self.path = root_path
        #contents = os.list_dir(root_path)
        self.expers = {}
        with os.scandir(self.path) as it :
            for entry in it :
                if entry.is_dir() and entry.name.endswith(ThePosse.EXT) :
                    self.expers[entry.name] = os.path.join(self.path,entry.name)

        print(self.expers.keys())
