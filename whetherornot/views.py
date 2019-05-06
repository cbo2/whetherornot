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
    result = requests.get('https://api.darksky.net/forecast/93d657f3bdf48bc91d9977b8e970f9dc/37.4467,25.3289,2017-07-01T15:00:00?units=us&exclude=currently,flags')
    print(type(result.json()['daily']['data']))
    print(result.json()['daily']['data'][0]['summary'])
    # print(type(result.json()))
    # json_result = json.loads(result.json())
    # print("json result object: ", type(json_result), json_result)
    
    print(result.json())
    print(type(result.json()))
    # df = pd.DataFrame(data=(result.json())['daily']['data'])
    df = pd.read_json(json.dumps(result.json()['daily']['data']), orient='records')
    print(df.shape)
    # print(df.columns)
    # print(df.dtypes)
    # df = pd.DataFrame(data=json_normalize(result.json()['daily']['data'][0]))
    print('----------------------dataframe start----------------------------------')
    print(df)
    print('----------------------dataframe end------------------------------------')
    return HttpResponse('\
        <h1>gotcha!!!</h1>\
        <p>{}</p>\
    '.format(df))