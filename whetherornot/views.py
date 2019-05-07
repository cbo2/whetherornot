from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import requests
import pandas as pd
from pandas.io.json import json_normalize
import json

# Create your views here.
class HomePageView(TemplateView):
    print('==========> HomePageView ======================')
    template_name = 'home.html'

def hello(request):
    print('------------->>>> hit the hello function again!!')
    # result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,255657600?units=us&exclude=currently,flags')
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,1998-06-30T15:00:00?units=us&exclude=currently,flags')
    # print(type(result.json()['daily']['data']))
    # print(result.json()['daily']['data'][0]['summary'])
    # print(type(result.json()))
    # json_result = json.loads(result.json())
    # print("json result object: ", type(json_result), json_result)
    
    print(result.json())
    print(type(result.json()))
    # df = pd.DataFrame(data=(result.json())['daily']['data'])
    df = pd.read_json(json.dumps(result.json()['daily']['data']), orient='records')
    print(f'shape is: {df.shape}')
    print(f'description is: \n{df.describe()}')
    print(f'dataframe: \n{df}')


    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,1999-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)

    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2000-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)

    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2001-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2002-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2003-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2004-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2005-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2006-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2007-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2008-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2009-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2010-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2011-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2012-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2013-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2014-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2015-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2016-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2017-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    # get second day worth of data from dark sky weather api
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2018-07-01T15:00:00?units=us&exclude=currently,flags')
    # now append to the existing dataframe
    df = df.append(pd.read_json(json.dumps(result.json()['daily']['data']), orient='records'), sort=False)
    print(f'shape is: {df.shape}')
    print(f'columns are: {df.columns}')
    print(f'description is: \n{df.describe()}')
    print(f'info is: \n{df.info()}')
    # print(f'values: \n{df.values}')


    # print(df.columns)
    # print(df.dtypes)
    # df = pd.DataFrame(data=json_normalize(result.json()['daily']['data'][0]))

    # let's drop some irrelevant columnss 
    df = df.drop(
        ['apparentTemperatureMaxTime', 
        'apparentTemperatureMinTime',
        'dewPoint',
        'icon',
        'moonPhase',
        'pressure',
        'summary',
        'temperatureMaxTime',
        'temperatureMinTime',
        'time',
        'uvIndex',
        'uvIndexTime',
        'windBearing',
        'apparentTemperatureHighTime',
        'apparentTemperatureLowTime',
        'temperatureHighTime',
        'temperatureLowTime',
        'windGustTime',
        'precipIntensity',
        'precipIntensityMax',
        'visibility'
        ], axis=1)
    print(f'shape is: {df.shape}')
    print(f'columns (after cleanup) are: {df.columns}')
    print(f'description is: \n{df.describe()}')
    print(f'the "temperatureHigh" Series: \n{df["temperatureHigh"]}')

    print('----------------------dataframe start----------------------------------')
    print(df)
    print('----------------------dataframe end------------------------------------')
    return HttpResponse(f'\
        <h1>gotcha!!!</h1>\
        <p>high temp average over 20 years:  {df["temperatureHigh"].mean()}</p>\
    ')