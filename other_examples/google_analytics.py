#!/usr/bin/env python3

"""
Authenticate with Google Analytics API and return desired metrics
Requires oauth2client v2.0 or greater

To get the service account JSON go to the Google API manager, click
on the "Credentials" menu item. Under OAuth 2.0 client IDs find the
Service account client type, and click the download button on the right.

Owen Littlejohns, 2016 April 29th
"""

import datetime
from apiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
# NOTE: This requires oauth2client v2.0 or greater to work
from oauth2client.service_account import ServiceAccountCredentials


def ga_authenticate(key_file_input):
    """
    Authenticate with the Google Analytics service using a service account
    JSON key file
    """
    ga_scopes      = ['https://www.googleapis.com/auth/analytics.readonly']
    ga_credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_input, ga_scopes)
    ga_auth        = ga_credentials.authorize(Http())
    ga_service     = ga_service = build('analytics', 'v3', http = ga_auth)

    return ga_service


def ga_api_request(start_str, end_str, metrics_str, dims_str, ga_service):
    """
    Send request to Google Analytics API and return the results
    """
    try:
        results = ga_service.data().ga().get(
            ids         = 'ga:XXXXXXXXX',
            start_date  = start_str,
            end_date    = end_str,
            metrics     = metrics_str,
            dimensions  = dims_str,
            sort        = '-ga:users,-ga:newUsers',
            #filter='',
            max_results = '25'
            ).execute()
    except TypeError as error:
        # Handle error from query construction:
        print('Badly formated API query: %s' % error)
        results = {}
    except HttpError as error:
        print('404 Error - Error connecting to GA API: %s:%s' % 
              (error.resp.status, error._get_reason))
        results = {}
    except:
        print('Unknown error: %s' % sys.exc_info()[0])
        results = {}
        
    return results


if __name__ == "__main__":
    """
    Connect to Google Analytics API and return metrics
    In practice, probably would input service account file name, dates 
    and metrics as an argument, using the sys package
    """
    # See doc string at top for instructions on where this file can be obtained:
    key_file_name = '/path/to/json/services_account_information.json'

    # Authenticate with the view (each has an individual ID):
    ga_service = ga_authenticate(key_file_name)

    # Define dates (in this example the start of the month until today)    
    date_today       = datetime.datetime.today()
    start_this_month = date_today.replace(day = 1)

    # Convert dates into strings:
    date_today_str = date_today.strftime('%Y-%m-%d')
    date_first_str = start_this_month.strftime('%Y-%m-%d')

    # Define metrics:
    metrics_list = ['ga:users', 'ga:newUsers']
    metrics_str  = (',').join(metrics_list)

    # Example calls:

    # Get metrics by region
    region_metrics = ga_api_request(date_first_str, date_today_str, 
                                    metrics_str, 'ga:region', ga_service)

    # Get metrics by country
    country_metrics = ga_api_request(date_first_str, date_today_str, 
                                     metric_str, 'ga:country', ga_service)

    # Get metrics by deviceCategory
    device_metrics = ga_api_request(date_first_str, date_today_str, 
                                    metrics_str, 'ga:deviceCategory', 
                                    ga_service)

    # Get metrics by browser
    browser_metrics = ga_api_request(date_first_str, date_today_str, 
                                     metrics_str, 'ga:browser', ga_service)

    # Output results:
    output_obj = {
        'region_metrics' : region_metrics,
        'country_metrics': country_metrics,
        'device_metrics' : device_metrics,
        'browser_metrics': browser_metrics}

    return output_obj
