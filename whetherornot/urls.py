
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import HomePageView, hello, SignUpView


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
    # path('users/', include('django.contrib.auth.urls')),
    path('', SignUpView.as_view(template_name='home.html'), name='home'),
    # path('', HomePageView.as_view(template_name='home.html'), name='home'),
    path('hello', hello, name='hello'),
] 
