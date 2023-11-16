import pandas as pd
"""
Created on Fri Apr 14 10:33:28 2023

@author: Nick Panetta
"""

class Sheet:
    def __init__(self, filename=''): # want to use class methods on dataframes: can make filename parameter optional and have it make an empty dataframe if nothing is given, then can append a df to it
        if filename == '':
            self.df = pd.DataFrame()
        else:
            self.df = pd.read_csv(filename)
        
    def __repr__(self):
        return(self.df.to_string())
    
    def delete_var(self, varlist, obslist=[]): #unused obslist so can use generic button function in GUI. could make it optional here but can't in following func
        self.df = self.df.drop(varlist, axis = 1)
        
    def delete_obs(self, varlist, obslist): #varlist is unused here, just pass an empty list. necessary for button function in GUI
        #gui program wasn't working w GUI because it was feeding the function strings instead of ints, now convert obslist to ints then run 
        for i in range(len(obslist)):
            obslist[i] = int(obslist[i])
        self.df = self.df.drop(obslist, axis = 0)
        
    def delete_obs_by_var(self, var, obs): # inputs in lists must be str
        obs = obs[0] # because obs and var are given as a list, take obs to be first element in the list
        var = var[0]
        obslist = []
        for index, contents in self.df.iterrows(): # was previously getting error when contents were int
            contents = contents[var] # so make contents just the target variable part
            contents = str(contents) # and make it to a string
            if obs in contents:
                obslist.append(index)
        self.delete_obs([], obslist)
        
    def delete_obs_by_var_multi(self, varlist, obslist): # this must use an integer as argument if the df has an integer in it
        # create var_obs dictionary from varlist and obslist 
        # current issue: if trying to use this after using delete obs or delete_obs_by_var, won't work. delete obs looks at pandas df index, this just looks at which column it is in existing columns. need to find pandas df index.
        var_obs = {}
        for i in range(len(varlist)):
            var_obs[varlist[i]] = obslist[i] 
        indices = {}
        for variable, value in var_obs.items(): # iteratr thru target variables and variable values
            try:
                value = int(value)
            except:
                pass
            variable = str(variable)
            # old implementation in comment below, new implementation should take care of current issue
            index = []
            for ind, row in self.df.iterrows():
                if row[variable] == value:
                    index.append(ind)
            #index = list(np.where(self.df[variable] == value)) # index = a list of where the variable == string version of value. below, set(index) was set(index[0])
            indices[variable] = (set(index)) # construct a dictionary with the key being the variable and the value being a set containing the list above
        # for loop thru dictionary, find intersect of each value set
        inter = list(indices.values())[0]
        for value in indices.values():
            inter = inter.intersection(value)
        inter= list(inter) # turn the set into a list so it can be converted to int in delete_obs()
        self.delete_obs([], inter)
    def keep_var(self, varlist, obslist=[]): # run delete var and find the difference
        all_vars = list(self.df.head())
        to_drop = [var for var in all_vars if var not in varlist]
        self.delete_var(to_drop)
        
    def keep_obs(self, varlist, obslist): # run delete obs and find difference
        obslist = [int(obs) for obs in obslist]
        all_obs = self.df.index.tolist()
        to_drop = [obs for obs in all_obs if obs not in obslist]
        self.delete_obs([], to_drop)
    
    def keep_obs_by_var(self, var, obs):
        obs = obs[0] # because obs and var are given as a list, take obs to be first element in the list
        var = var[0]
        obslist = []
        for index, contents in self.df.iterrows(): # was previously getting error when contents were int
            contents = contents[var] # so make contents just the target variable part
            contents = str(contents) # and make it to a string
            if obs in contents:
                obslist.append(index)
        self.keep_obs([], obslist)
        
    def keep_obs_by_var_or(self, var, obs): # give one variable and a list of obs. if any of the obs match the variable, keep the row
        obs = obs # because obs and var are given as a list, take obs to be first element in the list
        var = var[0]
        obslist = []
        for index, contents in self.df.iterrows(): # was previously getting error when contents were int
            contents = contents[var] # so make contents just the target variable part
            contents = str(contents) # and make it to a string
            for o in obs:
                if o in contents:
                    obslist.append(index)
        self.keep_obs([], obslist)
    
    def keep_obs_by_var_multi(self, varlist, obslist): 
        var_obs = {}
        for i in range(len(varlist)):
            var_obs[varlist[i]] = obslist[i] 
        indices = {}
        for variable, value in var_obs.items(): # iteratr thru target variables and variable values
            try:
                value = int(value)
            except:
                pass
            variable = str(variable)
            # old implementation in comment below, new implementation should take care of current issue
            index = []
            for ind, row in self.df.iterrows():
                if row[variable] == value:
                    index.append(ind)
            #index = list(np.where(self.df[variable] == value)) # index = a list of where the variable == string version of value. below, set(index) was set(index[0])
            indices[variable] = (set(index)) # construct a dictionary with the key being the variable and the value being a set containing the list above
        # for loop thru dictionary, find intersect of each value set
        inter = list(indices.values())[0]
        for value in indices.values():
            inter = inter.intersection(value)
        inter= list(inter) # turn the set into a list so it can be converted to int in delete_obs()
        self.keep_obs([], inter)
    
    def sort(self, varlist, reverse=False): # sort by given variable, if second arg is True sorts reverse
        if reverse == ['True'] or reverse == ['true']:
            reverse = True
        if reverse == True:
            self.df = self.df.sort_values(by=varlist, ascending=False)
        else:
            self.df = self.df.sort_values(by=varlist, ascending=True)
    
    def delete_dupes(self, varlist, obslist): # delete duplicates given vars. running just a var deletes dupes of that var (keep first). passing nothing deletes perfect duplicates. multiple vars deletes only obs that are duplicates in all vars
        if varlist == [] or varlist == ['']: # if varlist is empty, want to only delete perfect duplicates. 
            varlist = None # set varlist = None so subset will = None so only perfect duplicates will be deleted
        self.df.drop_duplicates(subset = varlist, inplace=True)
    
    def append(self, appendfrom, indices = 0): # arg is file path of csv to append from. open new window in GUI
        appendfrom = pd.read_csv(appendfrom)
        self.df = pd.concat([self.df, appendfrom])
        
    def rename_var(self, var, newname):
        self.df.rename(inplace=True, columns = {var[0]: newname[0]})
        
    def save_df_to_csv(self, target_filename):
        return(self.df.to_csv(target_filename, index = False))
        

if __name__ == '__main__': # does not execute this part if importing from another file
    df = Sheet('example.csv')
    print(df)
    print()
    df.sort(['Location'], ['true'])
    print(df)
    input("en")
    
    
    
