from django.shortcuts import render
from django.views.generic.edit import  FormView, CreateView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy
import requests
import pandas as pd
from pandas.io.json import json_normalize
from matplotlib import pyplot as plt
import json
from .forms import CustomLocationForm
import os
from django.conf import settings
import geocoder

import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime as dt

from django import forms
class LocationForm(forms.Form):
    location = forms.CharField(max_length=100)

class HomePageView(TemplateView):
    # print('==========> HomePageView ======================')
     template_name = 'search.html'

class SearchView(FormView):
    form_class = CustomLocationForm
    # success_url = reverse_lazy('hello')
    template_name = 'search.html'
    dark_sky = os.environ["DARK_SKY"]
    geocoder_key = os.environ["GOOGLE_GEOCODE_KEY"]

    def form_valid(self, form):
        print('----------- form_valid --------------')
        print(settings.MEDIA_ROOT + '/image.png')
 
        # return
        print(f'the key for darksky is: {self.dark_sky}')
        # form.got_it()
        print('--------------- form_valid internal start ------------')
        location = form.cleaned_data['location']
        result = geocoder.google(location, key=self.geocoder_key)
        print(f'full geocoder output: \n{dir(result)}')
        print('\n\naddress_components: ', result.geojson['features'][0]['properties']['address'])
        location = result.geojson['features'][0]['properties']['address']
        print(f'full geocoder output: \n{result.location}')
        print(f'lat is: {result.lat}  long is: {result.lng}')
        longitude = result.lng
        latitude = result.lat
        date = form.cleaned_data['date']
        print('date is: ', date)
        print('--------------- form_valid internal end ------------')
        print('context_data: ', self.get_context_data()['form'])
        context = {
            'location': location,
            'date': date,
        }
        # return render(self.request, 'result.html', self.get_context_data())
        df = pd.DataFrame()
        data_dict = {}
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.hit_weather_api_and_populate_dataframe(latitude, longitude, date, data_dict))
        loop.run_until_complete(future) 
        print('--------------------------******************--------------------------')
        print('keys only==> ', data_dict.keys())
        print('value for 1 only==> ', data_dict[1])
        print(data_dict)

        df = pd.DataFrame.from_dict(data_dict, orient='index')
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
            # 'windGustTime',
            'precipIntensity',
            'precipIntensityMax',
            'visibility',
            # 'sunriseTime',
            'sunsetTime',
            ], axis=1)
        print(df)
        print('--------------------------******************--------------------------')
        print(f'shape is: {df.shape}')
        print(f'columns (after cleanup) are: {df.columns}')
        print(f'description is: \n{df.describe()}')
        print(f'the "temperatureHigh" Series: \n{df["temperatureHigh"]}')

        print('----------------------dataframe start----------------------------------')
        print(df)
        print('----------------------dataframe end------------------------------------')

        print(f'after dataframe')

        # adjust wind speeds by 10 for scale
        df.loc[:,'windSpeed'] *= 10
        # adjust precipy by 100 for scale
        df.loc[:,'precipProbability'] *= 100
        # adjust cloudiness by 100 for scale
        df.loc[:,'cloudCover'] *= 100

        # high temp bar graph
        # print(df.groupby(['monthday'])['temperatureHigh'].mean())
        df2 = df.loc[:, ['monthday', 'temperatureHigh', 'humidity']]
        df2.loc[:,'humidity'] *= 100   # need to mulitply humidity * 100 for scale
        fig = df2.groupby(['monthday']).mean().plot(kind='bar').get_figure()
        # fig = df.groupby(['monthday'])['temperatureHigh'].mean().plot(kind='bar').get_figure()
        temp_image_filename = 'temp_image.png'
        temp_image_file = settings.MEDIA_ROOT + f'/{temp_image_filename}'
        plt.xlabel('Week Of');
        plt.ylabel('Temp/Humity %');
        plt.title('High Temp & Humidity');
        fig.savefig(temp_image_file, transparent=True)  # saves the current figure

        # wind line graph
        plt.clf()       # first need to clear the plot
        wind_image_filename = 'wind_image.png'
        wind_image_file = settings.MEDIA_ROOT + f'/{wind_image_filename}'
        fig2 = df.groupby(['monthday'])['windSpeed'].mean().plot(kind='line').get_figure()
        plt.xlabel('');
        plt.ylabel('Wind (mph)');
        plt.title('Wind Speed');
        fig2.savefig(wind_image_file, transparent=True)  # saves the current figure

        # precip bar graph
        plt.clf()       # first need to clear the plot
        precip_image_filename = 'precip_image.png'
        precip_image_file = settings.MEDIA_ROOT + f'/{precip_image_filename}'
        fig2 = df.groupby(['monthday'])['precipProbability'].mean().plot(kind='bar').get_figure()
        plt.xlabel('Week Of')
        plt.ylabel('Precipitation %')
        plt.title('Precipitation')
        fig2.savefig(precip_image_file, transparent=True)  # saves the current figure

        # cloudcover line graph
        plt.clf()       # first need to clear the plot
        cloudcover_image_filename = 'cloudcover_image.png'
        cloudcover_image_file = settings.MEDIA_ROOT + f'/{cloudcover_image_filename}'
        fig2 = df.groupby(['monthday'])['cloudCover'].mean().plot(kind='line').get_figure()
        plt.xlabel('')
        plt.ylabel('Cloud Cover %')
        plt.title('Cloudiness')
        fig2.savefig(cloudcover_image_file, transparent=True)  # saves the current figure

        # print('sunrise is: ', df.loc(1)['sunriseTime'])
        # sunrise = dt.fromtimestamp(df.loc(1)['sunriseTime']).isoformat()
        # context['sunrise'] = sunrise

        # f string format f'{value:{width}.{precision}}'
        context['predicted_temp'] = f"{df['temperatureHigh'].mean():3.0f}"
        context['temp_image'] = temp_image_filename
        context['wind_image'] = wind_image_filename
        context['precip_image'] = precip_image_filename
        context['cloudcover_image'] = cloudcover_image_filename
        return render(self.request, 'result.html', context)

    def fetch_from_weather_api(self, session, param, latitude, longitude):
        base_url = f'https://api.darksky.net/forecast/{self.dark_sky}/{latitude},{longitude},'
        with session.get(base_url + param) as response:
            if response.status_code != 200:
                print("FAILURE::{0}".format(base_url + param))
            try:
                data = response.json()['daily']['data'][0]
        
                # time_completed_at = "{:5.2f}s".format(elapsed)
                # print("{0:<30} {1:>20}".format(param, time_completed_at))
                year = param[:4]
                monthday = param[5:10]
                print(f'****************** >> year: {year} monthday: {monthday} << ******************')
                return (data, year, monthday)
            except Exception as e:
                print(f'..........EXCEPTION with {param} !!!!')
                print(e, type(e))
            # return (data, year, monthday)

    async def hit_weather_api_and_populate_dataframe(self, latitude, longitude, target_date, data_dict):
        print('=====================================')
        # print(f'original date is: {date}')
        # target_date = dt.strptime(date, '%Y-%m-%d')
        today = dt.now()
        print(f'******************* year is: {today.year} and the type is: {type(today.year)} ****************')
        from_year = today.year - 20
        to_year = today.year 
        print(f'******************* from year: {from_year} and to year: {to_year} ****************')
        print('dt is : ', target_date)
        date_minus_a_week = target_date - timedelta(days=7)
        date_minus_2_weeks = target_date - timedelta(days=14)
        date_plus_a_week = target_date + timedelta(days=7)
        date_plus_2_weeks = target_date + timedelta(days=14)
        print('original minus a week :', date_minus_a_week)
        print('the month is:', date_minus_a_week.month)
        print('the day is: ', date_minus_a_week.day)
        print('the year is: ', date_minus_a_week.year)  
        print('=====================================')
        # use a list comprehension to establish 20 years worth of query params for the target date
        params = [
            (
                str(year) + '-' + str(target_date.month).zfill(2) + '-' + str(target_date.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            # for year in range(from_year, to_year)
            for year in range(2014, 2017)
        ]
        # use a list comprehension to establish 20 years worth of query params for the target date minus a week
        minus_a_week = [
            (
                str(year) + '-' + str(date_minus_a_week.month).zfill(2) + '-' + str(date_minus_a_week.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            # for year in range(from_year, to_year)
            for year in range(2016, 2017)
        ]
        params.extend(minus_a_week)
        # use a list comprehension to establish 20 years worth of query params for the target date minus 2 weeks
        minus_2_weeks = [
            (
                str(year) + '-' + str(date_minus_2_weeks.month).zfill(2) + '-' + str(date_minus_2_weeks.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            # for year in range(from_year, to_year)
            for year in range(2016, 2017)
        ]
        params.extend(minus_2_weeks)
        # use a list comprehension to establish 20 years worth of query params for the target date plus a week
        plus_a_week = [
            (
                str(year) + '-' + str(date_plus_a_week.month).zfill(2) + '-' + str(date_plus_a_week.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            # for year in range(from_year, to_year)
            for year in range(2016, 2017)
        ]
        params.extend(plus_a_week)
        # use a list comprehension to establish 20 years worth of query params for the target date plus 2 weeks
        plus_2_weeks = [
            (
                str(year) + '-' + str(date_plus_2_weeks.month).zfill(2) + '-' + str(date_plus_2_weeks.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            # for year in range(from_year, to_year)
            for year in range(2016, 2017)
        ]
        params.extend(plus_2_weeks)
        print('*************************** params ************************')
        print(params)
        print('*************************** params ************************')
        print("{0:<30} {1:>20}".format("File", "Completed at"))
        with ThreadPoolExecutor(max_workers=20) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch_from_weather_api`
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.fetch_from_weather_api,
                        *(session, param, latitude, longitude) # Allows us to pass in multiple arguments to `fetch_from_weather_api`
                    )
                    for param in params
                ]
                for num, response in enumerate(await asyncio.gather(*tasks), start = 1):
                    try:
                        print(f'------------------ {num} --------------------')
                        resp_data, resp_year, resp_monthday = response
                        print(type(resp_data))
                        print(resp_year)
                        print(resp_monthday)
                        # need to add the response to the data_dict keyed by year...need monthday also for aggregation/mean functions later
                        resp_data['monthday'] = resp_monthday
                        data_dict[num] = resp_data
                    except Exception as e:
                        print('caught Exception on response from fetch!')
                        print(e, type(e))