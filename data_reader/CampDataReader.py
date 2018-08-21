"""
 Script reads the csv file describing the details of people requiring help.
"""

__author__ = "Shameer Sathar"
__license__ = "MIT"
__version__ = "1.0.1"

# imports
import pandas as pd
import numpy as np

class CampDataReader:
    def __init__(self, filename):
        self.filename = filename
        self.df  = self._read_file()
        self.df_filtered = pd.DataFrame()

    def _process_column(self, val):
        if val == 'None':
            return np.nan
        else:
            return int(val)

    def _read_file(self):
        df = pd.read_excel(self.filename)
        df['Total Infants'] = df['Total Infants'].apply(self._process_column)
        df['Total Males'] = df['Total Males'].apply(self._process_column)
        df['Total Females'] = df['Total Females'].apply(self._process_column)
        df['Total People'] = df['Total People'].apply(self._process_column)
        df = df[['Camp Name', 'District', 'Taluk', 'Village', 'Total People',
       'Total Males', 'Total Females', 'Total Infants',]]
        # We are ignoring the location information more than 1000 meters
        return df

    def get_districts(self):
        return self.df['District'].unique()

    def get_plot_data(self,list_requirements):
        df = self.df
        return df.groupby('District').sum()['Total People']
    #
    # def getLastEntry(self):
    #     time = self.df.datetime.max()
    #     return "{:%B %d, %Y}".format(time) + " at %s:%s" % (time.hour, time.minute)
    #
    #
    def get_plot_per_dist(self,list_requirements, dist):
        df = self.df
        df = df[df.District == dist]
        return df.groupby('Taluk').sum()['Total People']

    def get_all_dist_data(self,dist):
        df = self.df
        df = df[df.District == dist]
        return df
    #
    # def get_plot_per_loc(self,list_requirements, rad_value, loc):
    #     df = self.df_filtered
    #     df = df[df.location == loc]
    #     return df

if __name__ == '__main__':
    main()
