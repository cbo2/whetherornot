# whetherornot
In a nutshell, this app will allow the user a clean interface to check weather for a future dated vacation.
The idea here is that if you are planning a significant vacation in advance and knew the weather stats,
you may wish you had planned your trip at another date.  This app will help you predict the weather for your
desired destination in advance and then change the date to better align with your weather desires.  So, the 
idea is __**whether or not**__ you shoud go to that destination on a given date __or switch it to another date__.  A little play on words.....yes, we know the difference between weather and whether ;-)

# NOTE
__While I a plan to deploy to heroku and have a url available to use the app, until that happens if you would like to run it localhost you can clone the project and then run:__

    python manage.py runserver


# technologies
- python
- django
- APIs
  - Google Geocoder to translate city location to long/lat 
  - Dark Sky (Time Machine) historical data
- pandas

# Python features utilized
- list comprehensions to supply muliple parameters as variables to the weather API
- mulitthreading so we can hit the weather API in parallel dramatically improving overall response time
- datetime module to both subtract and add weeks from the target date
- pandas and plotting 
- json module to work with the returned weather data  
- django's templating and filtering 
- requests module to hit the geocoder and weather APIs
- async methods and await in conjuction with ThreadPoolExecutor to facilitate multithreading 
- private methods 
- exception handling (try/except blocks)
