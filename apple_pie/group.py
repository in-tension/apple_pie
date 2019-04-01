class Group :
    def __init__(self, exper, name, condits=None) :
        self.exper = exper
        self.name = name

        self.condits = None
        for condit in condits :
            self.add_condit(condit)



    def add_condit(self, condit) :
        if self.condits is None :
            self.condits = {condit.name:condit}
        elif condit.name in self.condits :
            print('uh oh, issue in Group.add_condit()')
        else :
            self.condits[condit.name] = condit




    def __str__(self) :
        return self.name

    def __repr__(self) :
        ## bad practice?
        return str(self)

    @property
    def condit_strs(self) :
        self._condit_strs = []
        for condit in self.condits :
            self._condit_strs.append(condit.name_str)

        return self._condit_strs
    @condit_strs.setter
    def condit_strs(self, value) :
        self._condit_strs = value

        #

    # @condit_strs.setter
