from django import forms
from django.views.generic.edit import FormView

# from .models import CustomUser


class CustomLocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100)

    # class Meta():
    #     # model = CustomUser
    # fields = ('location')