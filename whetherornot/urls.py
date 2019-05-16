
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import HomePageView, hello, SearchView


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
    # path('users/', include('django.contrib.auth.urls')),
    path('', HomePageView.as_view(template_name='signup.html'), name='signup'),
    path('search', SearchView.as_view(template_name='search.html'), name='search'),
    path('hello', hello, name='hello'),
] 
