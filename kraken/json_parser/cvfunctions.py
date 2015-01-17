class Parameter:
    def __init__(self):
        self.type = None
        self.name = None
        self.description = None

class Function:
    def __init__(self, name):
        self.name = name
        self.fname = None
        self.pars = []
        self.description = 'non-description'
        self.return_type = 'non-return-type'
   
    def add_fname(self,fname):
        self.fname = fname

    def add_description(self,des):
            self.description = des

    def add_return_type(self, return_type):
        self.return_type = return_type

    def get_parameter(self, name):
        par = None
        for sublist in self.pars:
            if name == sublist.name:
                par = sublist
                break
            elif (len(name) < len(sublist.name)) and (name == sublist.name[:len(name)]):
                par = sublist
                break
        if par is None:
            par = Parameter()
            par.name = name
            self.pars.append(par)
        return par

    def update_parameter(self,par):
        for sublist in self.pars:
            if sublist.name == par.name:
                sublist.name = par.name
                sublist.type = par.type
                sublist.description = par.description

    def add_parameter_des(self, name, des):
        par = self.get_parameter(name)
        par.description = des
        self.update_parameter(par)

    def add_parameter_type(self, name, type_):
        par = self.get_parameter(name)
        par.type = type_
        self.update_parameter(par)

    def __str__(self):
        return 'Function name : ' + self.name + '\nFunction Description: ' + self.description + '\n Function Parameter : \n' + ''.join(["\n\t%s %s \n\t\tDescription: %s, "%(p.type,p.name,p.description) for p in self.pars])
