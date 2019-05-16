
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import HomePageView, SearchView


urlpatterns = [
    # path('', HomePageView.as_view(template_name='signup.html'), name='signup'),
    path('', SearchView.as_view(template_name='search.html'), name='search'),
    path('search', SearchView.as_view(template_name='search.html'), name='search'),
] 
