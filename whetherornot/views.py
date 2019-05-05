from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
class HomePageView(TemplateView):
    print('==========> HomePageView ======================')
    template_name = 'home.html'

def hello(request):
    print('------------->>>> hit the hello function again!!')
    return HttpResponse('<h1>gotcha!!!</h1>')