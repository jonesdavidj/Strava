#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module that gets all of the activities a user has ever created on Strava.
   Saves them to a csv file called strava_activities.csv
"""
import pandas as pd
from strava_mod import getAccessToken
import requests
import json
import time
import os

# get the access token for accessing Strava from strava_mod
access_token = getAccessToken()

# Loop through all activities
page = 1
url = "https://www.strava.com/api/v3/activities"
# Create the dataframe ready for the API call to store your activity data
activities = pd.DataFrame(
    columns = [
            "id",
            "name",
            "start_date_local",
            "type",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "average_heartrate",
            "max_heartrate",
            "average_speed",
            "max_speed",
            "average_watts",
            "max_watts",
            "weighted_average_watts",
            "suffer_score",
            "average_cadence",
            "end_latlng",
            "external_id"
    ]
)
while True:

    # get page of activities from Strava
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()

    # if no results then exit loop
    if (not r):
        break

    # otherwise add new data to dataframe
    for x in range(len(r)):
        activities.loc[x + (page-1)*200,'id'] = r[x]['id']
        activities.loc[x + (page-1)*200,'name'] = r[x]['name'].encode("ascii","ignore").decode()
        activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local'].rstrip('Z')
        activities.loc[x + (page-1)*200,'type'] = r[x]['type']
        activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
        activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
        activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
        activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
        # Maybe no HR....
        try:
            activities.loc[x + (page-1)*200,'average_heartrate'] = r[x]['average_heartrate']
            activities.loc[x + (page-1)*200,'max_heartrate'] = r[x]['max_heartrate']
        except KeyError:
            activities.loc[x + (page-1)*200,'average_heartrate'] = ''
            activities.loc[x + (page-1)*200,'max_heartrate'] = ''
        activities.loc[x + (page-1)*200,'average_speed'] = r[x]['average_speed']
        activities.loc[x + (page-1)*200,'max_speed'] = r[x]['max_speed']
        # Maybe no Watts
        try:
            activities.loc[x + (page-1)*200,'average_watts'] = r[x]['average_watts']
            activities.loc[x + (page-1)*200,'max_watts'] = r[x]['max_watts']
            activities.loc[x + (page-1)*200,'weighted_average_watts'] = r[x]['weighted_average_watts']
            activities.loc[x + (page-1)*200,'average_cadence'] = r[x]['average_cadence']
        except KeyError:
            activities.loc[x + (page-1)*200,'average_watts'] = ''
            activities.loc[x + (page-1)*200,'max_watts'] = ''
            activities.loc[x + (page-1)*200,'weighted_average_watts'] = ''
            activities.loc[x + (page-1)*200,'average_cadence'] = ''
        activities.loc[x + (page-1)*200,'suffer_score'] = r[x]['suffer_score']
        activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
        activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']
    # increment page
    page += 1
# Export your activities file as a csv
# to the folder you're running this script in
try:
    os.mkdir('outputs')
except OSError as error:
    print ('Warning Only:' + str(error))
activities.to_csv('outputs/strava_activities.csv')
