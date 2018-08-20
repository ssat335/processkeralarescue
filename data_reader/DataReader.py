"""
 Script reads the csv file describing the details of people requiring help.
"""

__author__ = "Shameer Sathar"
__license__ = "MIT"
__version__ = "1.0.1"

# imports
import pandas as pd
import numpy as np

import os
import re

class DataReader:
    def __init__(self, filename):
        self.filename = filename
        self.df  = self._read_file()
        self.df_filtered = pd.DataFrame()

    def _read_file(self):
        df = pd.read_json(self.filename)
        df['latlng'].replace('', np.nan, inplace=True)
        df.dropna(subset=['latlng'], inplace=True)
        df['LatValid'] = df['latlng'].apply(self._getLat)
        df['LonValid'] = df['latlng'].apply(self._getLon)
        df = df[df['LonValid'] != False]
        df['datetime'] = pd.to_datetime(df['dateadded'])
        df['locError'] = df['latlng_accuracy'].apply(self._getLocError)
        # We are ignoring the location information more than 1000 meters
        return df[df.locError < 1000]

    def _getLat(self, data):
        if ((data[0] == '(')):
            data = data[1:-1]
        if re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', data) is not None:
            lat, long = [float(x) for x in data.split(',')]
        else:
            lat, long = False, False
        return lat

    def _getLon(self, data):
        if ((data[0] == '(')):
            data = data[1:-1]
        if re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', data) is not None:
            lat, long = [float(x) for x in data.split(',')]
        else:
            lat, long = False, False
        return long

    def _getLocError(self, data):
        if data == 'accurate':
            return 0
        elif (' Meters' in data):
            return float(data.split()[0])
        else:
            ## a huge value
            return 10000

    def get_plot_data(self,list_requirements, rad_value):
        print(self.df)
        df = self.df
        # we check based on the dropdown
        list_requirements = list_requirements
        init_df = pd.DataFrame()
        for requirement in list_requirements:
            if requirement == 'needfoodandwater':
                t_df = df[(df['needfood'] == True)]
            else:
                t_df = df[df[requirement] == True]
            init_df = pd.concat([init_df,t_df]).drop_duplicates().reset_index(drop=True)
        df = init_df

        # here we filter based on the radion inputs
        if (rad_value == 'requested_within_3_hours'):
            df = df[df.datetime > df.datetime.max() -  pd.Timedelta(hours=3)]
        elif (rad_value == 'requested_today'):
            df = df[df.datetime > df.datetime.max() -  pd.Timedelta(hours=24)]
        elif (rad_value == 'requested_yesterday'):
            df = df[(df.datetime > (df.datetime.max() -  pd.Timedelta(hours=48)))]
        elif (rad_value == '2_days_back'):
            df = df[(df.datetime <= (df.datetime.max() -  pd.Timedelta(hours=48)))]
        else:
            df = df
        self.df_filtered = df
        return df

    def getLastEntry(self):
        time = self.df.datetime.max()
        return "{:%B %d, %Y}".format(time) + " at %s:%s" % (time.hour, time.minute)


    def get_plot_per_dist(self,list_requirements, rad_value, dist):
        df = self.df_filtered
        df = df[df.district == dist]
        return df

    def get_plot_per_loc(self,list_requirements, rad_value, loc):
        df = self.df_filtered
        df = df[df.location == loc]
        return df

if __name__ == '__main__':
    main()
