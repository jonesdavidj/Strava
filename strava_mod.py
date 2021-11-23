#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module provides a set of standard, reusable classes for accessing Strava.
   Requires installation of pandas (pip install pandas) to work.
"""

import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
import time


"""Function getAccessToken
   Returns: str() 'access_token'

   Includes the refresh token concept so you don't need to reauthenticate.
"""

def getAccessToken ():

    # Get the tokens from file to connect to Strava
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)

    # If access_token has expired then
    # use the refresh_token to get the new access_token
    if strava_tokens['expires_at'] < time.time():

        # Make Strava auth API call with current refresh token
        response = requests.post(
                            url = 'https://www.strava.com/oauth/token',
                            data = {
                                    'client_id': 74225,
                                    'client_secret': 'b723870f73b5620c550b24f146097cff8a31b2f5',
                                    'grant_type': 'refresh_token',
                                    'refresh_token': strava_tokens['refresh_token']
                                    }
                                )
        # Save response as json in new variable
        new_strava_tokens = response.json()

        # Save new tokens to file
        with open('strava_tokens.json', 'w') as outfile:
            json.dump(new_strava_tokens, outfile)

        # Use new Strava tokens from now
        strava_tokens = new_strava_tokens

        # Open the new JSON file and print the file contents
        # to check it's worked properly
    with open('strava_tokens.json') as check:
        data = json.load(check)

    print('Secured Strava token')
    return strava_tokens['access_token']


"""Function getMyStarredSegments
   Returns: pd.DataFrame

   Generates a list of all the user account's starred segments in Strava.
"""

def getMyStarredSegments(access_token):
    pageSeg = 1
    url_segments = "https://www.strava.com/api/v3/segments/starred"

    # Create the dataframe ready for the API call to store your activity data
    segments = pd.DataFrame(
        columns = [
                "segment_id",
                "name",
                "activity_type",
                "distance",
                "average_grade",
                "maximum_grade",
                "elevation_low",
                "elevation_high"
                ]
        )

    while True:
        # get page of activities from Strava
        r = requests.get(url_segments + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(pageSeg))
        r = r.json()

        # if no results then exit loop
        if (not r):
            break

        # otherwise add new data to dataframe
        for x in range(len(r)):
            try:
                segments.loc[x + (pageSeg-1)*200,'segment_id'] = r[x]['id']
                segments.loc[x + (pageSeg-1)*200,'name'] = r[x]['name'].encode("ascii","ignore").decode()
                segments.loc[x + (pageSeg-1)*200,'activity_type'] = r[x]['activity_type']
                segments.loc[x + (pageSeg-1)*200,'distance'] = r[x]['distance']
                segments.loc[x + (pageSeg-1)*200,'average_grade'] = r[x]['average_grade']
                segments.loc[x + (pageSeg-1)*200,'maximum_grade'] = r[x]['maximum_grade']
                segments.loc[x + (pageSeg-1)*200,'elevation_low'] = r[x]['elevation_low']
                segments.loc[x + (pageSeg-1)*200,'elevation_high'] = r[x]['elevation_high']
            except KeyError:
                segments.loc[x + (pageSeg-1)*200,'id'] = str(x)
                print ('Page error: '+ str(x))
        # increment page
        pageSeg += 1

    return segments


"""Function getSegmentDetails
   Returns: pd.DataFrame

   Generates a DataFrame of segments Details based on a segment_id
"""
def getSegmentDetails(access_token, segment_id):

    pageSeg = 1
    url = "https://www.strava.com/api/v3/segments/"

    # Create the dataframe ready for the API call to store your activity data
    segment = pd.DataFrame(
        columns = [
                "id",
                "name",
                "activity_type",
                "distance",
                "average_grade",
                "maximum_grade",
                "elevation_low",
                "elevation_high",
                "end_latlng",
                "total_elevation_gain"
                ]
        )

    while True:
        # get page of activities from Strava
        r = requests.get(url + segment_id + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(pageSeg))
        r = r.json()

        # if no results then exit loop
        if (not r):
            break

        # otherwise add new data to dataframe
        for x in range(len(r)):
            try:
                # Basic details
                segment.loc[x + (pageSeg-1)*200,'id'] = r[x]['id']
                segment.loc[x + (pageSeg-1)*200,'name'] = r[x]['name'].encode("ascii","ignore").decode()
                segment.loc[x + (pageSeg-1)*200,'activity_type'] = r[x]['activity_type'].encode("ascii","ignore").decode()
                segment.loc[x + (pageSeg-1)*200,'distance'] = r[x]['distance']
            except KeyError:
                segment.loc[x + (pageSeg-1)*200,'id'] = str(x)
            try:
                # Ride & Run
                segment.loc[x + (pageSeg-1)*200,'average_grade'] = r[x]['average_grade']
                segment.loc[x + (pageSeg-1)*200,'maximum_grade'] = r[x]['maximum_grade']
                segment.loc[x + (pageSeg-1)*200,'elevation_low'] = r[x]['elevation_low']
                segment.loc[x + (pageSeg-1)*200,'elevation_high'] = r[x]['elevation_high']
                segment.loc[x + (pageSeg-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            except KeyError:
                segment.loc[x + (pageSeg-1)*200,'average_grade'] = '0'
                segment.loc[x + (pageSeg-1)*200,'maximum_grade'] = '0'
                segment.loc[x + (pageSeg-1)*200,'elevation_low'] = '0'
                segment.loc[x + (pageSeg-1)*200,'elevation_high'] = '0'
                segment.loc[x + (pageSeg-1)*200,'total_elevation_gain'] = '0'
            try:
                segment.loc[x + (pageSeg-1)*200,'end_latlng'] = r[x]['end_latlng']
            except KeyError:
                segment.loc[x + (pageSeg-1)*200,'end_latlng'] = ''
        # increment page
        pageSeg += 1

    return segment

"""Function getMyEffortsForSegment
   Returns: pd.DataFrame

   Returns a DataFrame of segment efforts based on a segment id
"""

def getMyEffortsForSegment (access_token, segment_id):
    page = 1
    url_efforts  = "https://www.strava.com/api/v3/segment_efforts"

    efforts = pd.DataFrame(
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

    r = requests.get(url_efforts + '?segment_id=' + str(segment_id) + '&access_token=' + str(access_token) + '&per_page=200' + '&page=' + str(page))
    r = r.json()

    # clear the efforts DataFrame object, else the previous loop results will remain
    efforts = efforts.iloc[0:0]

    for x in range(len(r)):
        try:
            # print ('item: ' + str(x) + ' segment_id: ' + str(segment_id) + ' name: ' + r[x]['name'].encode("ascii","ignore").decode())
            efforts.loc[x + (page-1)*200,'segment_id'] = segment_id
            efforts.loc[x + (page-1)*200,'effort_id'] = r[x]['id']
            efforts.loc[x + (page-1)*200,'name'] = r[x]['name'].encode("ascii","ignore").decode()
        except KeyError:
            print('id or name not correct')
        try:
            efforts.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
            efforts.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
            efforts.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
        except KeyError:
            print ('Date / time error')
            efforts.loc[x + (page-1)*200,'start_date_local'] = ''
            efforts.loc[x + (page-1)*200,'elapsed_time'] = ''
            efforts.loc[x + (page-1)*200,'moving_time'] = ''
        try:
            efforts.loc[x + (page-1)*200,'average_watts'] = r[x]['average_watts']
        except KeyError:
            # not on a bike
            efforts.loc[x + (page-1)*200,'average_watts'] = '0'
        try:
            efforts.loc[x + (page-1)*200,'pr_rank'] = r[x]['pr_rank']
        except KeyError:
            # something really has gone wrong.
            print ('pr_rank error - last field')

    return efforts

if __name__ == "__main__":
    import sys
    getAccessToken()
