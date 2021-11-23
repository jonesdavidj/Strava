#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module that gets all of the efforts from a user's Starred Strava segments
   Saves them to a csv file called strava_efforts.csv
"""

from strava_mod import getAccessToken, getMyStarredSegments, getMyEffortsForSegment
import pandas as pd
from pandas.io.json import json_normalize
import requests

pageEff = 1

myEfforts = pd.DataFrame(
    columns = [
            "segment_id",
            "effort_id",
            "name",
            "start_date_local",
            "elapsed_time",
            "moving_time",
            "average_watts",
            "pr_rank"
    ]
)
# Get the access token for strava from strava_mod
access_token = getAccessToken()
# print ('Setup complete')

# get my starred segments from Strava
mySegments = getMyStarredSegments(access_token)
mySegments.to_csv('strava_starredsegments.csv')

print ('Number of starred segments: ' + str(len(mySegments)))

for index, row in mySegments.iterrows():
    try:
        # get the efforts for the next starred segment
        efforts = getMyEffortsForSegment(access_token, str(row['segment_id']))
    except:
        print('something went wrong getting efforts')
    try:
        myEfforts = pd.concat([efforts, myEfforts],sort=False)
    except:
        print ('something went wrong merging')
    print ('getting data for ' + str(row['name']))

myEfforts.to_csv('strava_efforts.csv')
