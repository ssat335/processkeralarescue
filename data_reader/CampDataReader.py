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

    def _read_file(self):
        df = pd.read_csv(self.filename)
        df.drop_duplicates(inplace=True)
        df = df[['district', 'name', 'location', 'taluk', 'village', 'total_people', 'total_males',
       'total_females', 'total_infants']]
        # We are ignoring the location information more than 1000 meters
        return df

    def get_districts(self):
        return self.df['district'].unique()

    def get_plot_data(self,list_requirements):
        df = self.df
        return df.groupby('district').sum()['total_people']

    def get_plot_per_dist(self,list_requirements, dist):
        df = self.df
        df = df[df.district == dist]
        return df.groupby('taluk').sum()['total_people']

    def get_all_dist_data(self,dist):
        df = self.df
        df = df[df.district == dist]
        return df

    def get_all_taluk_data(self,dist, taluk):
        df = self.df
        df = df[df.district == dist]
        df = df[df.taluk == taluk]
        return df

if __name__ == '__main__':
    main()
