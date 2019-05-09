from django import forms
from django.views.generic.edit import FormView

# from .models import CustomUser


class CustomLocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100)
    date = forms.DateField(label='Desired Date')

    # def got_it(self):
    #     print('--------------- got it called ------------')
    #     print('date is: ', self.cleaned_data['date'])
    #     print('--------------- got it called ------------')

    # class Meta():
    #     # model = CustomUser
    # fields = ('location')