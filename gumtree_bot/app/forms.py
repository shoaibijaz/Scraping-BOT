from django import forms
from .models import *

class SearchForm(forms.Form):
    id = forms.IntegerField(widget = forms.HiddenInput, required=False)
    keywords = forms.CharField(max_length=200,required=True,initial='')
    category = forms.CharField(max_length=200,required=False,initial='')
    negative = forms.CharField(max_length=200,required=True,initial='')
    start_time = forms.CharField(max_length=50,required=False, initial='')
    end_time = forms.CharField(max_length=50,required=False, initial='')

    website = forms.ModelChoiceField(
        queryset=Websites.objects.all() ,
        empty_label='Select a website',
        required=True
    )

    proxy = forms.ModelChoiceField(
        queryset=Proxies.objects.all() ,
        empty_label='Default',
        required=False
    )