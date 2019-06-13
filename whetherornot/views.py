from django.shortcuts import render
from django.views.generic.edit import  FormView, CreateView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from django import forms
import pandas as pd
from pandas.io.json import json_normalize
from matplotlib import pyplot as plt
import json
from .forms import CustomLocationForm
import os
import geocoder
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime as dt

class LocationForm(forms.Form):
    location = forms.CharField(max_length=100)

class HomePageView(TemplateView):
     template_name = 'search.html'

class SearchView(FormView):
    form_class = CustomLocationForm
    # success_url = reverse_lazy('hello')
    template_name = 'search.html'
    dark_sky = os.environ["DARK_SKY"]
    geocoder_key = os.environ["GOOGLE_GEOCODE_KEY"]

    def form_valid(self, form):
        print('----------- form_valid --------------')
 
        location = form.cleaned_data['location']
        result = geocoder.google(location, key=self.geocoder_key)
        # get the probably location from Google since the user may have given an abbreviated location
        location = result.geojson['features'][0]['properties']['address']
        print(f'lat is: {result.lat}  long is: {result.lng}')
        longitude = result.lng
        latitude = result.lat
        date = form.cleaned_data['date']
        print('date is: ', date)
        context = {
            'location': location,
            'date': date,
        }
        data_dict = {}
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.__hit_weather_api_and_populate_dataframe(latitude, longitude, date, data_dict))
        loop.run_until_complete(future) 

        self.__gen_dataframe_and_plots(data_dict, context)

        return render(self.request, 'result.html', context)

    def __gen_dataframe_and_plots(self, data_dict, context):
        df = pd.DataFrame()
        df = pd.DataFrame.from_dict(data_dict, orient='index')
        # drop the columns from the dataframe that won't be useful here
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
            'precipIntensity',
            'precipIntensityMax',
            'visibility',
            # 'sunriseTime',
            'sunsetTime',
            ], axis=1)
        print(df)
        print(f'shape is: {df.shape}')
        print(f'columns (after cleanup) are: {df.columns}')
        print('----------------------dataframe start----------------------------------')
        print(df)
        print('----------------------dataframe end------------------------------------')

        # adjust wind speeds by 10 for scale
        # df.loc[:,'windSpeed'] *= 10
        # adjust precipy by 100 for scale
        df.loc[:,'precipProbability'] *= 100
        # adjust cloudiness by 100 for scale
        df.loc[:,'cloudCover'] *= 100

        # high temp bar graph
        try: 
            df2 = df.loc[:, ['monthday', 'temperatureHigh', 'humidity']]
            df2.loc[:,'humidity'] *= 100   # need to mulitply humidity * 100 for scale
            fig = df2.groupby(['monthday']).mean().plot(kind='bar').get_figure()
            temp_image_filename = 'temp_image.png'
            temp_image_file = settings.MEDIA_ROOT + f'/{temp_image_filename}'
            plt.xlabel('Week Of');
            plt.ylabel('Temp/Humity %');
            plt.title('High Temp & Humidity');
            fig.savefig(temp_image_file, transparent=True)  # saves the current figure
        except Exception as e:
            temp_image_filename = "default_temp.jpg"


        # wind line graph
        plt.clf()       # first need to clear the plot
        wind_image_filename = 'wind_image.png'
        wind_image_file = settings.MEDIA_ROOT + f'/{wind_image_filename}'
        try: 
            fig2 = df.groupby(['monthday'])['windGust'].mean().plot(kind='line').get_figure()
            plt.xlabel('');
            plt.ylabel('Wind (mph)');
            plt.title('Wind Speed');
            fig2.savefig(wind_image_file, transparent=True)  # saves the current figure
        except Exception as e:
            wind_image_filename = "default_wind.jpg"

        # precip bar graph
        try: 
            plt.clf()       # first need to clear the plot
            precip_image_filename = 'precip_image.png'
            precip_image_file = settings.MEDIA_ROOT + f'/{precip_image_filename}'
            fig2 = df.groupby(['monthday'])['precipProbability'].mean().plot(kind='bar').get_figure()
            plt.xlabel('Week Of')
            plt.ylabel('Precipitation %')
            plt.title('Precipitation')
            fig2.savefig(precip_image_file, transparent=True)  # saves the current figure
        except Exception as e:
            wind_image_filename = "default_precip.jpg"

        # cloudcover line graph
        try:
            plt.clf()       # first need to clear the plot
            cloudcover_image_filename = 'cloudcover_image.png'
            cloudcover_image_file = settings.MEDIA_ROOT + f'/{cloudcover_image_filename}'
            fig2 = df.groupby(['monthday'])['cloudCover'].mean().plot(kind='line').get_figure()
            plt.xlabel('')
            plt.ylabel('Cloud Cover %')
            plt.title('Cloudiness')
            fig2.savefig(cloudcover_image_file, transparent=True)  # saves the current figure
        except Exception as e:
            cloudcover_image_filename = "default_cloud_cover.jpg"

        # print('sunrise is: ', df.loc(1)['sunriseTime'])
        # sunrise = dt.fromtimestamp(df.loc(1)['sunriseTime']).isoformat()
        # context['sunrise'] = sunrise

        # f string format f'{value:{width}.{precision}}'
        context['predicted_temp'] = f"{df['temperatureHigh'].mean():3.0f}"
        context['temp_image'] = temp_image_filename
        context['wind_image'] = wind_image_filename
        context['precip_image'] = precip_image_filename
        context['cloudcover_image'] = cloudcover_image_filename

    def __fetch_from_weather_api(self, session, param, latitude, longitude):
        base_url = f'https://api.darksky.net/forecast/{self.dark_sky}/{latitude},{longitude},'
        with session.get(base_url + param) as response:
            if response.status_code != 200:
                print("FAILURE::{0}".format(base_url + param))
            try:
                data = response.json()['daily']['data'][0]
                year = param[:4]
                monthday = param[5:10]
                return (data, year, monthday)
            except Exception as e:
                print(f'..........EXCEPTION with {param} !!!!')
                print(e, type(e))

    async def __hit_weather_api_and_populate_dataframe(self, latitude, longitude, target_date, data_dict):
        today = dt.now()
        from_year = today.year - 20
        to_year = today.year 
        date_minus_a_week = target_date - timedelta(days=7)
        date_minus_2_weeks = target_date - timedelta(days=14)
        date_plus_a_week = target_date + timedelta(days=7)
        date_plus_2_weeks = target_date + timedelta(days=14)
        # use a list comprehension to establish 20 years worth of query params for the target date
        params = [
            (
                str(year) + '-' + str(target_date.month).zfill(2) + '-' + str(target_date.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            for year in range(from_year, to_year)
            # for year in range(2014, 2017)
        ]
        # use a list comprehension to establish 20 years worth of query params for the target date minus a week
        minus_a_week = [
            (
                str(year) + '-' + str(date_minus_a_week.month).zfill(2) + '-' + str(date_minus_a_week.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            for year in range(from_year, to_year)
            # for year in range(2016, 2017)
        ]
        params.extend(minus_a_week)
        # use a list comprehension to establish 20 years worth of query params for the target date minus 2 weeks
        minus_2_weeks = [
            (
                str(year) + '-' + str(date_minus_2_weeks.month).zfill(2) + '-' + str(date_minus_2_weeks.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            for year in range(from_year, to_year)
            # for year in range(2016, 2017)
        ]
        params.extend(minus_2_weeks)
        # use a list comprehension to establish 20 years worth of query params for the target date plus a week
        plus_a_week = [
            (
                str(year) + '-' + str(date_plus_a_week.month).zfill(2) + '-' + str(date_plus_a_week.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            for year in range(from_year, to_year)
            # for year in range(2016, 2017)
        ]
        params.extend(plus_a_week)
        # use a list comprehension to establish 20 years worth of query params for the target date plus 2 weeks
        plus_2_weeks = [
            (
                str(year) + '-' + str(date_plus_2_weeks.month).zfill(2) + '-' + str(date_plus_2_weeks.day).zfill(2) + 'T15:00:00?units=us&exclude=currently,flags'
            )
            for year in range(from_year, to_year)
            # for year in range(2016, 2017)
        ]
        params.extend(plus_2_weeks)
        with ThreadPoolExecutor(max_workers=20) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `__fetch_from_weather_api`
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.__fetch_from_weather_api,
                        *(session, param, latitude, longitude) # Allows us to pass in multiple arguments to `__fetch_from_weather_api`
                    )
                    for param in params
                ]
                for num, response in enumerate(await asyncio.gather(*tasks), start = 1):
                    try:
                        resp_data, resp_year, resp_monthday = response
                        # need to add the response to the data_dict keyed by year...need monthday also for aggregation/mean functions later
                        resp_data['monthday'] = resp_monthday
                        data_dict[num] = resp_data
                    except Exception as e:
                        print('caught Exception on response from fetch!')
                        print(e, type(e))